"""Builds S1 File (test cases with automated results) from tests.py. Usage: python3 make_s1.py DAISY_v4.xml OUT.xlsx"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
FORM, OUT = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], FORM]
import tests  # runs all cases
T, res = tests.T, tests.res

MOD = {'T': 'Temperature and age', 'D': 'Danger signs', 'G': 'Gastrointestinal', 'S': 'Other symptoms', 'R': 'Referral reasons',
       'N': 'Symptom durations', 'A': 'Malaria with additional referral', 'C': 'Combined findings', 'B': 'TB symptoms with other findings',
       'V': 'Low temperature, young infants, prolonged fever, pregnancy age', 'O': 'No test available, rest advice, saved reasons',
       'P': 'Pregnancy on referral screens', 'M': 'Malaria – uncomplicated', 'H': 'Malaria – severe', 'U': 'Usability scenarios', 'K': 'Symptom assessment unless urgently referred'}
DESC = {
 'T01': 'Young infant, just below fever cut-off', 'T02': 'Young infant, fever cut-off (37.5 °C)', 'T03': 'Young infant, at hypothermia cut-off (35.5 °C)',
 'T04': 'Young infant, hypothermia', 'T05': 'Last day of young-infant band (59 days)', 'T06': 'First day of child band (60 days)',
 'T07': 'Child, high-temperature safety threshold (39.0 °C)', 'T08': 'Child, fever every day >7 days', 'T09': 'Child, fever ≤7 days',
 'T10': 'Child, hypothermia', 'T11': 'Child, at hypothermia cut-off (35.0 °C)', 'T12': 'Age 5 years: prolonged-fever question asked',
 'T13': 'Adult, just below high-temperature threshold', 'T14': 'Adult, at high-temperature threshold (39.0 °C)', 'T15': 'Adult, hypothermia',
 'T16': 'Pregnant, at 38.0 °C (not above)', 'T17': 'Pregnant, fever >38.0 °C', 'T18': "Former 'under 4 months' rule removed (90 days)",
 'T19': 'Young infant, reported fever only', 'T20': 'Age 2 months (DOB unknown): child band', 'T21': 'Age 1 month (DOB unknown): young infant',
 'G01': 'Blood in stool, adult', 'G02': 'Diarrhoea ≥14 days, child', 'G03': 'Diarrhoea ≥14 days, adult', 'G04': 'Infant <1 y, diarrhoea >12 h',
 'G05': 'Infant <1 y, diarrhoea ≤12 h', 'G06': 'Child 1–<2 y, vomiting >24 h', 'G07': 'Child ≥2 y, diarrhoea ≤2 days', 'G08': 'Child ≥2 y, diarrhoea >2 days', 'G09': 'Child 1–<2 y, diarrhoea >24 h', 'G10': 'Child 1–<2 y, diarrhoea ≤24 h',
 'S01': 'Cough >2 weeks', 'S02': 'Cough with blood', 'S03': 'Headache ≥7 days', 'S04': 'Unexplained weight loss', 'S05': 'Rash with fever',
 'S06': 'Fever with dark urine or unusual bleeding (danger sign)', 'S07': 'Headache <7 days', 'S08': 'Chest pain (symptoms page)',
 'S09': 'Pregnant with fever and neck stiffness or severe headache with intolerance to bright light (danger sign)', 'R01': 'Two danger signs and high temperature: each reason listed',
 'R02': 'Severe muscle or joint pain', 'R03': 'Fatigue ≥7 days', 'R04': 'Night sweats ≥14 days',
 'N01': 'Headache <7 days with weight loss: referral for weight loss only', 'N02': 'Headache ≥7 days, fatigue <7 days',
 'N03': 'Night sweats <14 days only', 'N04': 'Weight loss only', 'N05': 'Blood in stool: no duration questions asked',
 'N06': 'Short diarrhoea, vomiting >2 days', 'N07': 'Diarrhoea ≥14 days, short vomiting',
 'A01': 'Pf with rash: treat and refer as soon as possible', 'A02': 'Pv with chest pain', 'A03': 'Pf with persistent vomiting',
 'A04': 'Pv with weight loss and night sweats: refer after treatment', 'A05': 'Pf with symptoms explained by malaria: no extra referral',
 'C01': 'Pf with blood in stool and rash: urgent referral only', 'C02': 'Mixed infection with diarrhoea ≥14 days: urgent referral only',
 'C03': 'Prolonged fever and headache ≥7 days: one referral, both reasons', 'C04': 'Pf with prolonged fever: treat and refer',
 'C05': 'Young infant with Pv: urgent referral',
 'B01': 'TB symptoms only: BRAC clinic', 'B02': 'TB symptoms and rash: one health centre referral', 'B03': 'TB symptoms and prolonged fever: one referral',
 'B04': 'Pv with TB symptoms only: treatment and TB clinic note', 'B05': 'Pf with TB symptoms and rash: TB in also-refer list',
 'B06': 'Pv with TB symptoms and weight loss: all in refer-now list', 'B07': 'TB symptoms with blood in stool: urgent, TB listed',
 'V01': 'Pf with low temperature: urgent referral', 'V02': 'Pf with high temperature, no danger sign: treatment',
 'V03': 'Young infant with Pf: urgent referral', 'V04': 'Young infant with Pf and danger sign: severe malaria',
 'V05': 'Adult with fever every day >7 days', 'V06': 'Adult with fever ≤7 days', 'V07': 'Pregnant at age 13 with fever', 'V08': 'Age 11: pregnancy not asked', 'V09': 'Age 50: pregnancy not asked',
 'O01': 'Fever, no test available: referral for testing', 'O02': 'No test available with danger sign', 'O03': 'No test available with TB symptoms',
 'O04': 'Fever, negative test: return advice shown', 'O05': 'No fever: return advice not shown', 'O06': 'Saved reasons: two danger signs and high temperature',
 'O07': 'Saved reasons: Pf with rash', 'O08': 'Saved reasons: empty for rest',
 'P01': 'Pregnant with prolonged fever: pregnancy listed', 'P02': 'Pregnant with fever >38.0 °C: not listed twice', 'P03': 'Pregnant with danger sign: pregnancy listed',
 'P04': 'Not pregnant: no pregnancy line', 'P05': 'Pregnant with severe Pf: pregnancy listed',
 'M01': 'Fever in past 48 h triggers RDT', 'M02': 'No current or recent fever: RDT not prompted', 'M03': 'Pf, infant 3 months, <5 kg', 'M04': 'Pv, infant 3 months, <5 kg',
 'M05': 'Pv in pregnancy: treatment and referral', 'M18': 'Pf in pregnancy: ACT, no primaquine, referral', 'M06': 'Pv, breastfeeding a baby <6 months',
 'M07': 'Pv, child 6 years', 'M08': 'Pf, adult', 'M09': 'Pf, child 6 years', 'M10': 'Mixed infection, adult', 'M11': 'Primaquine safety advice',
 'M12': 'Chloroquine band, decimal weight 5.5 kg', 'M13': 'Chloroquine band, decimal weight 9.5 kg', 'M14': 'Malaria with TB symptoms',
 'M15': 'Pv, age 5 months (DOB unknown): no primaquine', 'M16': 'Pv, age 150 days (DOB known): no primaquine', 'M17': 'Malaria with temperature ≥39.0 °C, no danger signs',
 'H01': 'Severe Pf, age 2 years', 'H02': 'Severe Pf, infant 4 months', 'H03': 'Severe Pf, exactly 6 years', 'H04': 'Severe Pf, adult',
 'H05': 'Severe Pf, rectal artesunate unavailable', 'H06': 'Danger sign with Pv only', 'H07': 'Severe mixed infection, adult', 'H08': 'Severe Pf, age 200 days (DOB known)',
 'H09': 'Severe Pf defined by jaundice/pallor (national criterion)',
 'K01': 'High temperature, Pf, blood in stool: symptoms assessed, urgent referral', 'K02': 'High temperature, Pf, rash: treatment and also refer',
 'K03': 'High temperature, negative test, rash: urgent referral', 'K04': 'Pregnant with fever >38.0 °C and blood in stool: urgent referral',
 'K05': 'Young infant with reported fever and blood in stool: urgent referral', 'K06': 'High temperature, Pv, prolonged fever: treatment and also refer',
 'K07': 'Low temperature: symptoms skipped, urgent referral', 'K08': 'Young infant with fever: symptoms skipped, urgent referral',
 'U01': 'Usability scenario 1: suspected TB', 'U02': 'Usability scenario 2: uncomplicated Pf malaria'}
DSN = {'difficult_breathing': 'Difficulty breathing', 'severe_abdominal_pain': 'Severe abdominal pain', 'confusion': 'Confusion or unusual behaviour',
       'loss_of_consciousness': 'Unusually sleepy, lethargic or unconscious', 'convulsions': 'Convulsions', 'not_drinking': 'Not able to drink or breastfeed',
       'extreme_weakness': 'Unable to stand or sit if previously able', 'vomits_everything': 'Vomits everything',
       'jaundice_pallor': 'Yellow eyes or skin, or very pale palms, tongue or eyes', 'urine_bleeding': 'Dark or very little urine, or unusual bleeding',
       'severe_headache': 'Neck stiffness, or severe headache with intolerance to bright light', 'fast_breathing': 'Fast breathing (young infant)', 'chest_indrawing': 'Severe chest indrawing (young infant)',
       'movement_stimulated': 'Moves only when stimulated (young infant)'}
REC = {'severe_malaria': 'Severe malaria: pre-referral artesunate and urgent referral', 'urgent_referral': 'Refer to the health centre immediately',
       'malaria_treatment': 'Initiate malaria treatment', 'referral': 'Refer to the health centre', 'tb_referral': 'Visit the BRAC clinic for TB testing', 'rest': 'Rest and monitor'}
RDT = {'pos_falci': 'RDT Pf', 'pos_vivax': 'RDT Pv', 'pos_mixed': 'RDT mixed', 'negative': 'RDT negative', 'not_available': 'RDT not available'}
RL = {'r_temp_high': 'Body temperature too high', 'r_temp_low': 'Body temperature too low', 'r_blood_stool': 'Blood in stool', 'r_diarrhoea_14d': 'Diarrhoea ≥14 days',
      'r_malaria_pf': 'Positive test (Pf)', 'r_malaria_pv': 'Positive test (Pv)', 'r_malaria_mixed': 'Positive test (mixed)', 'r_preg_urgent': 'Patient is pregnant',
      'r_preg_info': 'Patient is pregnant', 'sm_preg': 'Patient is pregnant', 'r_rdt_na': 'No malaria test available', 'r_rdt_na_urgent': 'No malaria test available',
      'r_tb': 'TB symptoms', 'r_tb_urgent': 'TB symptoms', 'm_tb': 'TB symptoms', 'r_prolonged': 'Fever every day >7 days', 'm_prolonged': 'Fever every day >7 days',
      'r_infant': 'Young infant with reported fever', 'm_infant': 'Young infant with fever', 'r_pregnant': 'Fever in pregnancy', 'm_pregnant': 'Pregnancy',
      'r_muscle_joints': 'Severe muscle or joint pain', 'r_chest': 'Chest pain', 'm_chest': 'Chest pain', 'r_headache_7d': 'Headache ≥7 days', 'r_fatigue_7d': 'Fatigue ≥7 days',
      'r_weight_loss': 'Unexplained weight loss', 'm_weight_loss': 'Unexplained weight loss (after treatment)', 'mn_weight_loss': 'Unexplained weight loss (now)',
      'r_sweats_14d': 'Night sweats ≥14 days', 'm_sweats_14d': 'Night sweats ≥14 days (after treatment)', 'mn_sweats_14d': 'Night sweats ≥14 days (now)',
      'r_rash': 'Skin rash with fever', 'm_rash': 'Skin rash with fever', 'r_diarrhoea_u1': 'Diarrhoea >12 h', 'r_diarrhoea_1to2': 'Diarrhoea >24 h', 'r_diarrhoea_2plus': 'Diarrhoea >2 days',
      'r_vomiting_u1': 'Vomiting >12 h', 'r_vomiting_1to2': 'Vomiting >24 h', 'r_vomiting_2plus': 'Vomiting >2 days', 'm_vomiting_2plus': 'Persistent vomiting'}
RL.update({f'r_ds_{k}': v for k, v in DSN.items()}); RL.update({f'sm_ds_{k}': v for k, v in DSN.items()})
SCREEN = {'malaria_also_refer': "'Also refer' section", 'malaria_refer_now_txt': "'Refer as soon as possible' list", 'malaria_refer_later_txt': "'Refer after treatment' list",
          'TB_clinic': 'TB clinic note (malaria screen)', 'rest_fever_txt': 'Return advice for fever with negative test', 'referral': 'Health centre referral',
          'severe_illness': 'Urgent referral', 'severe_malaria': 'Severe malaria', 'suspected_tb': 'BRAC clinic referral', 'all_symptoms': 'Symptoms pages',
          'uncomplicated_malaria': 'Malaria treatment', 'rdt_group': 'Malaria test page', 'weight': 'Weight question', 'fever_7_days': 'Prolonged-fever question',
          'reasons_urgent': 'Reasons heading', 'reasons_referral': 'Reasons heading', 'reasons_severe_malaria': 'Danger-sign heading',
          'diarrhoea_dur_2plus': 'Diarrhoea duration question', 'vomiting_long_2plus': 'Vomiting duration question', 'headache_7d': 'Headache duration question',
          'sweats_14d': 'Night-sweats duration question', 'history_fever': 'Fever-history question'}
LBL = {'dosage_act': 'ACT per dose', 'dosage_chloroquine': 'Chloroquine days 1–2', 'dosage_chloroquine_day_3': 'Chloroquine day 3', 'dosage_primaquine': 'Primaquine (mg)',
       'artesunate_dosage': 'Rectal artesunate (mg)', 'artesunate_im_dosage': 'IM artesunate (mg)', 'referral_reasons': 'Saved reasons', 'young_infant': 'Young infant',
       'temp_danger': 'Temperature danger'}

def inputs(kw):
    s = []
    if kw.get('age_days') is not None: s.append(f"Age {kw['age_days']} days (DOB entered)")
    elif kw.get('years') == 0: s.append(f"Age {kw.get('months')} months (DOB unknown)")
    else: s.append(f"Age {kw['years']} years (DOB unknown)")
    if kw.get('sex') == 'female': s.append('female' + (', pregnant' if kw.get('pregnant') == 'yes' else ''))
    if kw.get('danger', 'none') != 'none': s.append(' + '.join(DSN[x] for x in kw['danger'].split()))
    f = kw['tf'] if kw.get('tf') is not None else tests.c2f(kw.get('tc') if kw.get('tc') is not None else 36.8)
    s.append(f"T {f:.1f} °F ({(f - 32) * 5 / 9:.1f} °C)")
    if kw.get('hist'): s.append('fever in past 48 h: ' + kw['hist'])
    if kw.get('fever7'): s.append('fever every day >7 days: ' + kw['fever7'])
    sy = kw.get('systemic', 'none')
    if sy != 'none':
        parts = []
        for x in sy.split():
            p = x.replace('_', ' ')
            if x == 'headache' and (kw.get('headache7') or kw.get('one_week')): p += f" (≥7 days: {kw.get('headache7') or kw.get('one_week')})"
            if x == 'fatigue' and (kw.get('fatigue7') or kw.get('one_week')): p += f" (≥7 days: {kw.get('fatigue7') or kw.get('one_week')})"
            if x == 'sweats' and (kw.get('sweats14') or kw.get('two_weeks')): p += f" (≥14 days: {kw.get('sweats14') or kw.get('two_weeks')})"
            parts.append(p)
        s.append(', '.join(parts))
    if kw.get('cough') == 'yes': s.append(f"persistent cough (>2 weeks: {kw.get('two_weeks_cough')}; blood: {kw.get('blood')})")
    gi = kw.get('intestinal', 'none')
    if gi != 'none':
        names = {'blood_stool': 'blood in stool', 'diarrhea': 'diarrhoea', 'vomiting': 'vomiting'}
        g = ', '.join(names[x] for x in gi.split())
        short = 'yes' in (kw.get('h12'), kw.get('h24'), kw.get('d2'))
        if 'diarrhea' in gi and 'blood_stool' not in gi:
            dd = kw.get('ddur') or ('long' if kw.get('d14') == 'yes' else ('medium' if short else 'short'))
            g += {'short': '; diarrhoea below age cut-off', 'medium': '; diarrhoea above age cut-off, <14 days', 'long': '; diarrhoea ≥14 days'}[dd]
        if 'vomiting' in gi and 'blood_stool' not in gi:
            g += f"; vomiting above age cut-off: {kw.get('vlong') or ('yes' if short else 'no')}"
        s.append(g)
    if kw.get('rash') == 'yes': s.append('skin rash')
    if kw.get('rdt'): s.append(RDT[kw['rdt']])
    if kw.get('weight') is not None: s.append(f"{kw['weight']} kg")
    if kw.get('bf'): s.append('breastfeeding baby <6 months: ' + kw['bf'])
    return '; '.join(s)

def checks(ch):
    out = []
    for k, v in ch.items():
        if isinstance(v, bool):
            if k in RL: out.append(f"reason '{RL[k]}': {'listed' if v else 'not listed'}")
            else: out.append(f"{SCREEN.get(k, k)}: {'shown' if v else 'not shown'}")
        else: out.append(f"{LBL.get(k, k)} = {v if v else '(empty)'}")
    return '; '.join(out)

wb = Workbook(); rd = wb.active; rd.title = 'README'
txt = [('S1 File. Software test cases for DAISY v4', True),
       ('Each case specifies the answers entered and the expected recommendation, emergency level and, where relevant, doses, screens shown and reasons listed on the recommendation page.', False),
       ('Temperatures are entered in the application in °F (one decimal), as used by CHWs; °C equivalents are given in brackets.', False),
       ('Automated result: all cases were run against the v4 XForm using JavaRosa, the open-source ODK form engine, with the test script in the tests/ folder of the GitHub repository. The script enters the answers in form order, skipping questions the form does not show, and records the calculated recommendation, emergency level, doses, screens and reason lines shown.', False),
       ('Manual check: 20 selected cases were also entered by hand in the KoboToolbox web form (Enketo); results are recorded in the yellow column.', False),
       ('Table 1 row(s): the row(s) of Table 1 (decision rules) that each case checks; every row of Table 1 is checked by at least one case. Expected results were specified from the rules in Table 1.', False),
       ('Module codes: ' + '; '.join(f'{k} {v[0].lower() + v[1:] if not v.startswith("TB") else v}' for k, v in MOD.items()) + '.', False)]
for i, (t_, b) in enumerate(txt, 1):
    c = rd.cell(i, 1, t_); c.font = Font(bold=b, size=12 if b else 11); c.alignment = Alignment(wrap_text=True, vertical='top')
rd.column_dimensions['A'].width = 120
ws = wb.create_sheet('Test cases')
H = ['ID', 'Table 1 row(s)', 'Module', 'Description', 'Inputs entered', 'Expected recommendation', 'Expected level', 'Specific checks', 'Automated result (JavaRosa)', 'Manual check in Kobo (Pass/Fail)', 'Notes']
ws.append(H)
for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1C5CAB'); c.alignment = Alignment(wrap_text=True, vertical='top')
yellow = PatternFill('solid', fgColor='FFF2CC'); thin = Side(style='thin', color='BBBBBB')
ORDER = 'TDGSNRKCABVOPMHU'
rowsT = sorted(T, key=lambda x: (ORDER.index(x[0][0]), x[0]))
fails = 0
for cid, kw, er, el, ch in rowsT:
    r = res[cid]
    ok = r['recommendation'][0] == er and r['emergency_level_calc'][0] == el and all((r[k][1] if isinstance(v, bool) else r[k][0]) == v for k, v in ch.items())
    fails += not ok
    desc = DESC.get(cid) or f"{' + '.join(DSN[x] for x in kw['danger'].split())} ({kw.get('years', '')} years)".replace('( years)', f"({kw.get('age_days')} days)")
    ws.append([cid, ', '.join(str(x) for x in tests.ROWS[cid]), MOD[cid[0]], desc, inputs(kw), REC[er], el.capitalize(), checks(ch), 'Pass' if ok else 'Fail', None, None])
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment = Alignment(wrap_text=True, vertical='top'); c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
    row[9].fill = yellow; row[10].fill = yellow
for col, w in zip('ABCDEFGHIJK', [6, 9, 18, 34, 52, 30, 10, 44, 14, 14, 24]): ws.column_dimensions[col].width = w
ws.freeze_panes = 'B2'
wb.save(OUT)
print(f'S1 File: {len(T)} cases, {fails} not passing')
