import re, datetime, subprocess, sys, json

FORM = sys.argv[1]
xml = open(FORM, encoding='utf8').read()
binds = re.findall(r'<bind nodeset="([^"]+)"([^>]*)/?>', xml)
P = {}

for path, attrs in binds:
    t = re.search(r'type="([^"]+)"', attrs)
    P[path.split('/')[-1]] = (path, t.group(1) if t else 'string')

ORDER = [p.split('/')[-1] for p, _ in binds]
TMAP = {'int': 'int', 'decimal': 'decimal', 'date': 'date', 'string': 'string'}

def ftype(n):
    t = P[n][1]
    if t in ('select1', 'string', 'int', 'decimal', 'date'): pass
    # select_one/multiple are typed 'string' in binds for pyxform>=? -> infer from xml body
    if re.search(r'<select1 [^>]*ref="%s"' % re.escape(P[n][0]), xml): return 'select1'
    if re.search(r'<select [^>]*ref="%s"' % re.escape(P[n][0]), xml): return 'select'
    return TMAP.get(t, 'string')

def c2f(c): return round(c * 9 / 5 + 32, 1)

def case(cid, age_days=None, years=None, months=None, sex='male', pregnant='no', danger='none', tc=None, tf=None,
         hist=None, fever7=None, systemic='none', one_week=None, two_weeks=None, cough='no', two_weeks_cough=None, blood=None,
         intestinal='none', d14=None, h12=None, h24=None, d2=None, ddur=None, vlong=None, headache7=None, fatigue7=None, sweats14=None, rash='no', bleeding=None, rdt=None, weight=None, bf=None, head_rf='no', chest_rf='no'):
    A = {'sex': sex}
    if age_days is not None:
        A['dob_known'] = 'yes'; A['dob'] = (datetime.date.today() - datetime.timedelta(days=age_days)).isoformat()
    else:
        A['dob_known'] = 'no'; A['age_years'] = str(years)
        if years == 0: A['age_months'] = str(months)
    A['pregnant'] = pregnant
    A['danger_signs'] = danger
    t = tf if tf is not None else c2f(tc if tc is not None else 36.8)
    A['temperature'] = f'{t:.1f}'
    if hist: A['history_fever'] = hist
    if fever7: A['fever_7_days'] = fever7
    A['systemic_symptoms'] = systemic
    sy = systemic.split()
    if one_week and 'headache' in sy: A['headache_7d'] = one_week
    if one_week and 'fatigue' in sy: A['fatigue_7d'] = one_week
    if two_weeks and 'sweats' in sy: A['sweats_14d'] = two_weeks
    if headache7: A['headache_7d'] = headache7
    if fatigue7: A['fatigue_7d'] = fatigue7
    if sweats14: A['sweats_14d'] = sweats14
    A['persistent_cough'] = cough
    if two_weeks_cough: A['more_two_weeks'] = two_weeks_cough
    if blood: A['any_blood'] = blood
    A['intestinal'] = intestinal
    ay = (age_days / 365.25) if age_days is not None else (years if years else (months or 0) / 12)
    band = 'u1' if ay < 1 else ('1to2' if ay < 2 else '2plus')
    gi = intestinal.split(); short_yes = 'yes' in (h12, h24, d2)
    if 'diarrhea' in gi and 'blood_stool' not in gi:
        A[f'diarrhoea_dur_{band}'] = ddur or ('long' if d14 == 'yes' else ('medium' if short_yes else 'short'))
    if 'vomiting' in gi and 'blood_stool' not in gi:
        A[f'vomiting_long_{band}'] = vlong or ('yes' if short_yes else 'no')
    A['rash'] = rash
    if rdt: A['malaria_RDT'] = rdt
    if weight is not None: A['weight'] = str(weight)
    if bf: A['breastfeeding_u6m'] = bf
    return cid, A

OUTS = ['recommendation', 'emergency_level_calc', 'young_infant', 'temp_danger', 'is_fever', 'rdt_group', 'all_symptoms',
        'dosage_act', 'dosage_chloroquine', 'dosage_chloroquine_day_3', 'dosage_primaquine', 'artesunate_dosage', 'artesunate_im_dosage',
        'severe_illness', 'severe_malaria', 'severe_malaria_less_6a', 'severe_malaria_less_6b', 'severe_malaria_more_6a',
        'uncomplicated_malaria', 'vivax_infection', 'falciparum', 'mixed_infection', 'primaquine', 'primaquine_pf', 'primaquine_mix',
        'caution_primaquine', 'caution_primaquine_pf', 'followup_vivax', 'followup_falciparum', 'followup_mixed', 'TB_clinic',
        'referral', 'rest', 'suspected_tb', 'fever_7_days', 'history_fever', 'breastfeeding_u6m',
        'reasons_urgent', 'reasons_referral', 'reasons_severe_malaria', 'r_ds_difficult_breathing', 'r_ds_severe_abdominal_pain', 'r_ds_confusion', 'r_ds_loss_of_consciousness', 'r_ds_convulsions', 'r_ds_not_drinking', 'r_ds_extreme_weakness', 'r_ds_vomits_everything', 'r_ds_jaundice_pallor', 'r_ds_urine_bleeding', 'r_ds_severe_headache', 'r_ds_fast_breathing', 'r_ds_chest_indrawing', 'r_ds_movement_stimulated', 'sm_ds_convulsions', 'sm_ds_jaundice_pallor', 'r_temp_high', 'r_temp_low', 'r_blood_stool', 'r_diarrhoea_14d', 'r_malaria_pf', 'r_malaria_pv', 'r_malaria_mixed', 'r_prolonged', 'r_infant', 'r_pregnant', 'm_pregnant', 'm_prolonged', 'm_infant', 'r_tb', 'r_tb_urgent', 'm_tb', 'mn_weight_loss', 'm_weight_loss', 'TB_clinic', 'sm_preg', 'r_muscle_joints', 'r_chest', 'r_headache_7d', 'r_fatigue_7d', 'r_weight_loss', 'r_sweats_14d', 'r_diarrhoea_u1', 'r_diarrhoea_1to2', 'r_diarrhoea_2plus', 'r_vomiting_u1', 'r_vomiting_1to2', 'r_vomiting_2plus', 'r_rash', 'diarrhoea_dur_u1', 'diarrhoea_dur_1to2', 'diarrhoea_dur_2plus', 'vomiting_long_2plus', 'headache_7d', 'fatigue_7d', 'sweats_14d', 'malaria_also_refer', 'malaria_refer_now_txt', 'malaria_refer_later_txt', 'm_rash', 'm_chest', 'm_vomiting_2plus', 'm_weight_loss', 'm_sweats_14d', 'r_rdt_na', 'r_rdt_na_urgent', 'rest_fever_txt', 'referral_reasons', 'weight', 'g_pregnant', 'dosage_act', 'r_preg_urgent', 'r_preg_info', 'danger_present']

def run(cases):
    lines = []
    
    for cid, A in cases:
        lines.append(f'CASE {cid}')
        for n in ORDER:
            if n in A: lines.append(f'SET {P[n][0]}|{ftype(n)}|{A[n]}')
        for o in OUTS:
            path = P[o][0] if o in P else None
            if path is None:
                m = re.search(r'ref="(/data/[^"]*/%s)"' % o, xml) or re.search(r'<group [^>]*ref="(/data/(?:[^"/]+/)*%s)"' % o, xml)
                path = m.group(1)
            lines.append(f'OUT {path}')
        lines.append('END')
    
    open('in.txt', 'w', encoding='utf8').write('\n'.join(lines))
    import pyxform, os
    J = os.path.join(os.path.dirname(pyxform.__file__), 'validators/odk_validate/bin/ODK_Validate.jar')
    r = subprocess.run(['java', '-cp', J + ':.', 'Run', FORM, 'in.txt'], capture_output=True, text=True)
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
    res = {}
    for l in r.stdout.splitlines():
        if l.startswith('WARN'): print(l)
        if l.startswith('RESULT'):
            parts = l.split('\t'); cid = parts[0][7:]; d = {}
            for p in parts[1:]:
                k, rest = p.split('=', 1); v, rel = rest.rsplit('|rel=', 1); d[k] = (v, rel == 'true')
            res[cid] = d
    return res
