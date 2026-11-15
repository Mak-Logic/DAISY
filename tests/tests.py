import sys; sys.argv=[sys.argv[0], sys.argv[1]]
from cases import case, run, c2f
T = []  # (id, case_kwargs, expected recommendation, expected level, checks)
def t(cid, exp_rec, exp_lvl, checks=None, **kw): T.append((cid, kw, exp_rec, exp_lvl, checks or {}))
R = lambda name: (name, True); NR = lambda name: (name, False)
# --- Temperature (entered in F) ---
t('T01','rest','low',{'temp_danger':'no'}, age_days=30, tc=37.4, hist='no')
t('T02','urgent_referral','high',{}, age_days=30, tc=37.5)
t('T03','rest','low',{'temp_danger':'no'}, age_days=30, tf=95.9, hist='no')
t('T04','urgent_referral','high',{'r_temp_low':True}, age_days=30, tf=95.8, hist='no')
t('T05','urgent_referral','high',{}, age_days=59, tc=37.5)
t('T06','rest','low',{'young_infant':'no','temp_danger':'no'}, age_days=60, tc=37.5, fever7='no', rdt='negative')
t('T07','urgent_referral','high',{}, age_days=60, tc=39.0)
t('T08','referral','moderate',{'r_prolonged':True,'referral':True}, years=0, months=3, tc=38.0, fever7='yes', rdt='negative')
t('T09','rest','low',{'r_prolonged':False}, years=0, months=3, tc=38.0, fever7='no', rdt='negative')
t('T10','urgent_referral','high',{}, years=4, tf=94.9, hist='no')
t('T11','rest','low',{'temp_danger':'no'}, years=4, tf=95.0, hist='no')
t('T12','rest','low',{'fever_7_days':True}, years=5, tc=38.5, fever7='no', rdt='negative')
t('T13','rest','low',{'temp_danger':'no'}, years=30, tf=102.1, rdt='negative')
t('T14','urgent_referral','high',{'r_temp_high':True,'r_temp_low':False}, years=30, tf=102.2)
t('T15','urgent_referral','high',{'r_temp_low':True,'r_temp_high':False}, years=30, tf=94.9, hist='no')
t('T16','rest','low',{'r_pregnant':False}, years=25, sex='female', pregnant='yes', tf=100.4, rdt='negative')
t('T17','referral','moderate',{'r_pregnant':True,'referral':True}, years=25, sex='female', pregnant='yes', tf=100.5, rdt='negative')
t('T18','rest','low',{'young_infant':'no','r_infant':False}, age_days=90, tc=37.8, fever7='no', rdt='negative')
t('T19','referral','moderate',{'r_infant':True,'referral':True}, age_days=30, tc=36.8, hist='yes', rdt='negative')
t('T20','rest','low',{'young_infant':'no'}, years=0, months=2, tc=36.8, hist='no')
t('T21','rest','low',{'young_infant':'yes'}, years=0, months=1, tc=36.8, hist='no')
# --- Danger signs ---
ds=['difficult_breathing','severe_abdominal_pain','confusion','loss_of_consciousness','convulsions','not_drinking','extreme_weakness','vomits_everything','jaundice_pallor','urine_bleeding','severe_headache']
k=1
for d in ds:
    for y in (3,30):
        t(f'D{k:02d}','urgent_referral','high',{'all_symptoms':False,f'r_ds_{d}':True,'reasons_urgent':True,'r_temp_high':False}, years=y, danger=d, hist='no'); k+=1
for d in ('fast_breathing','chest_indrawing','movement_stimulated'):
    t(f'D{k:02d}','urgent_referral','high',{'all_symptoms':False,f'r_ds_{d}':True}, age_days=30, danger=d, tc=36.8, hist='no'); k+=1
# --- GI ---
t('G01','urgent_referral','high',{'r_blood_stool':True}, years=30, intestinal='blood_stool', hist='no')
t('G02','urgent_referral','high',{'r_diarrhoea_14d':True}, years=3, intestinal='diarrhea', d14='yes', d2='yes', hist='no')
t('G03','urgent_referral','high',{}, years=30, intestinal='diarrhea', d14='yes', d2='yes', hist='no')
t('G04','referral','moderate',{'r_diarrhoea_u1':True,'r_diarrhoea_2plus':False}, years=0, months=8, intestinal='diarrhea', d14='no', h12='yes', hist='no')
t('G05','rest','low',{}, years=0, months=8, intestinal='diarrhea', d14='no', h12='no', hist='no')
t('G06','referral','moderate',{'r_vomiting_1to2':True}, years=1, months=None, intestinal='vomiting', h24='yes', hist='no')
t('G07','rest','low',{}, years=3, intestinal='diarrhea', d14='no', d2='no', hist='no')
t('G09','referral','moderate',{'r_diarrhoea_1to2':True}, years=1, intestinal='diarrhea', ddur='medium', hist='no')
t('G10','rest','low',{'r_diarrhoea_1to2':False}, years=1, intestinal='diarrhea', ddur='short', hist='no')
t('G08','referral','moderate',{'r_diarrhoea_2plus':True,'reasons_referral':True}, years=3, intestinal='diarrhea', d14='no', d2='yes', hist='no')
# --- Other symptoms ---
t('S01','tb_referral','moderate',{'suspected_tb':True}, years=30, cough='yes', two_weeks_cough='yes', blood='no', hist='no')
t('S02','tb_referral','moderate',{'suspected_tb':True}, years=30, cough='yes', two_weeks_cough='no', blood='yes', hist='no')
t('S03','referral','moderate',{'r_headache_7d':True,'r_fatigue_7d':False}, years=30, systemic='headache', one_week='yes', hist='no')
t('S04','referral','moderate',{'r_weight_loss':True}, years=30, systemic='weight_loss', two_weeks='yes', hist='no')
t('S05','referral','moderate',{'r_rash':True}, years=10, tc=38.0, rash='yes', rdt='negative')
t('S06','urgent_referral','high',{'all_symptoms':False}, years=10, tc=38.0, danger='urine_bleeding', rdt='negative')
t('S07','rest','low',{}, years=30, systemic='headache', one_week='no', hist='no')
t('S08','referral','moderate',{'r_chest':True,'r_muscle_joints':False,'referral':True,'suspected_tb':False,'severe_illness':False}, years=45, systemic='chest', hist='no')
t('S09','urgent_referral','high',{'severe_illness':True,'all_symptoms':False}, years=28, sex='female', pregnant='yes', danger='severe_headache', tc=38.5)
t('H09','severe_malaria','high',{'sm_ds_jaundice_pallor':True,'sm_ds_convulsions':False,'severe_malaria_more_6a':True}, years=30, danger='jaundice_pallor', tc=38.5, rdt='pos_falci', weight=50)
# --- Referral reasons ---
t('R01','urgent_referral','high',{'r_ds_convulsions':True,'r_ds_confusion':True,'r_temp_high':True,'r_ds_difficult_breathing':False,'r_malaria_pf':False}, years=30, danger='convulsions confusion', tf=103.0, rdt='negative')
t('R02','referral','moderate',{'r_muscle_joints':True,'r_chest':False}, years=30, systemic='muscle_joints', hist='no')
t('R03','referral','moderate',{'r_fatigue_7d':True,'r_headache_7d':False}, years=30, systemic='fatigue', one_week='yes', hist='no')
t('R04','referral','moderate',{'r_sweats_14d':True,'r_weight_loss':False}, years=30, systemic='sweats', two_weeks='yes', hist='no')
# --- Per-symptom durations ---
t('N01','referral','moderate',{'r_weight_loss':True,'r_headache_7d':False,'headache_7d':True}, years=30, systemic='headache weight_loss', headache7='no', hist='no')
t('N02','referral','moderate',{'r_headache_7d':True,'r_fatigue_7d':False}, years=30, systemic='headache fatigue', headache7='yes', fatigue7='no', hist='no')
t('N03','rest','low',{'sweats_14d':True}, years=30, systemic='sweats', sweats14='no', hist='no')
t('N04','referral','moderate',{'r_weight_loss':True}, years=30, systemic='weight_loss', hist='no')
t('N05','urgent_referral','high',{'r_blood_stool':True,'diarrhoea_dur_2plus':False,'vomiting_long_2plus':False}, years=30, intestinal='diarrhea vomiting blood_stool', hist='no')
t('N06','referral','moderate',{'r_vomiting_2plus':True,'r_diarrhoea_2plus':False}, years=30, intestinal='diarrhea vomiting', ddur='short', vlong='yes', hist='no')
t('N07','urgent_referral','high',{'r_diarrhoea_14d':True,'r_vomiting_2plus':False}, years=30, intestinal='diarrhea vomiting', ddur='long', vlong='no', hist='no')
# --- Malaria positive with symptoms not explained by malaria ---
t('A01','malaria_treatment','moderate',{'malaria_also_refer':True,'malaria_refer_now_txt':True,'m_rash':True,'malaria_refer_later_txt':False,'referral':False}, years=10, tc=38.0, rash='yes', rdt='pos_falci', weight=30)
t('A02','malaria_treatment','moderate',{'malaria_refer_now_txt':True,'m_chest':True}, years=30, tc=38.0, systemic='chest', rdt='pos_vivax', weight=50)
t('A03','malaria_treatment','moderate',{'malaria_refer_now_txt':True,'m_vomiting_2plus':True}, years=30, tc=38.0, intestinal='vomiting', vlong='yes', rdt='pos_falci', weight=50)
t('A04','malaria_treatment','moderate',{'malaria_refer_later_txt':True,'m_weight_loss':True,'m_sweats_14d':True,'malaria_refer_now_txt':False}, years=30, tc=38.0, systemic='weight_loss sweats', sweats14='yes', rdt='pos_vivax', weight=50)
t('A05','malaria_treatment','moderate',{'malaria_also_refer':False}, years=30, tc=38.0, systemic='headache muscle_joints', headache7='yes', intestinal='diarrhea', ddur='medium', rdt='pos_falci', weight=50)
# --- Combined findings: one consistent recommendation ---
t('C01','urgent_referral','high',{'r_blood_stool':True,'r_malaria_pf':True,'uncomplicated_malaria':False,'malaria_also_refer':False}, years=30, tc=38.0, intestinal='blood_stool', rash='yes', rdt='pos_falci', weight=50)
t('C02','urgent_referral','high',{'r_diarrhoea_14d':True,'r_malaria_mixed':True,'uncomplicated_malaria':False}, years=10, tc=38.0, intestinal='diarrhea', ddur='long', rdt='pos_mixed', weight=30)
t('C03','referral','moderate',{'r_prolonged':True,'r_headache_7d':True,'referral':True}, years=3, tc=38.0, fever7='yes', systemic='headache', headache7='yes', rdt='negative')
t('C04','malaria_treatment','moderate',{'m_prolonged':True,'malaria_refer_now_txt':True,'referral':False}, years=3, tc=38.0, fever7='yes', rdt='pos_falci', weight=14)
t('C05','urgent_referral','high',{'r_malaria_pv':True,'uncomplicated_malaria':False}, age_days=40, tc=36.8, hist='yes', rdt='pos_vivax', weight=4)
# --- TB symptoms with other referral reasons: one destination ---
t('B01','tb_referral','moderate',{'suspected_tb':True,'referral':False}, years=30, cough='yes', two_weeks_cough='yes', blood='no', hist='no')
t('B02','referral','moderate',{'referral':True,'r_tb':True,'r_rash':True,'suspected_tb':False}, years=30, tc=38.0, cough='yes', two_weeks_cough='yes', blood='no', rash='yes', rdt='negative')
t('B03','referral','moderate',{'r_tb':True,'r_prolonged':True,'suspected_tb':False}, years=3, tc=38.0, fever7='yes', cough='yes', two_weeks_cough='yes', blood='no', rdt='negative')
t('B04','malaria_treatment','moderate',{'TB_clinic':True,'malaria_also_refer':False}, years=30, tc=38.0, cough='yes', two_weeks_cough='yes', blood='no', rdt='pos_vivax', weight=50)
t('B05','malaria_treatment','moderate',{'TB_clinic':False,'m_tb':True,'m_rash':True,'malaria_refer_now_txt':True}, years=30, tc=38.0, cough='yes', two_weeks_cough='yes', blood='no', rash='yes', rdt='pos_falci', weight=50)
t('B06','malaria_treatment','moderate',{'TB_clinic':False,'m_tb':True,'mn_weight_loss':True,'m_weight_loss':False,'malaria_refer_later_txt':False}, years=30, tc=38.0, systemic='weight_loss', cough='yes', two_weeks_cough='yes', blood='no', rdt='pos_vivax', weight=50)
t('B07','urgent_referral','high',{'r_tb_urgent':True,'r_blood_stool':True,'suspected_tb':False}, years=30, cough='yes', two_weeks_cough='yes', blood='no', intestinal='blood_stool', hist='no')
t('V01','urgent_referral','high',{'r_temp_low':True,'r_malaria_pf':True,'uncomplicated_malaria':False}, years=30, tf=94.5, hist='yes', rdt='pos_falci', weight=50)
t('V02','malaria_treatment','moderate',{'severe_illness':False}, years=30, tf=103.0, rdt='pos_falci', weight=50)
t('V03','urgent_referral','high',{'r_malaria_pf':True,'uncomplicated_malaria':False}, age_days=50, tc=36.8, hist='yes', rdt='pos_falci', weight=4)
t('V04','severe_malaria','high',{'severe_malaria_more_6a':True}, age_days=50, danger='convulsions', tc=36.8, hist='yes', rdt='pos_falci', weight=4)
t('V05','referral','moderate',{'fever_7_days':True,'r_prolonged':True}, years=30, tc=38.0, fever7='yes', rdt='negative')
t('V06','rest','low',{'fever_7_days':True,'r_prolonged':False}, years=45, tc=38.0, fever7='no', rdt='negative')
t('V07','referral','moderate',{'r_pregnant':True}, years=13, sex='female', pregnant='yes', tf=100.6, rdt='negative')
t('V08','rest','low',{'r_pregnant':False}, years=11, sex='female', pregnant='yes', tf=100.6, rdt='negative')
t('V09','rest','low',{'r_pregnant':False}, years=50, sex='female', pregnant='yes', tf=100.6, rdt='negative')
t('O01','referral','moderate',{'r_rdt_na':True,'rest':False,'weight':False,'referral_reasons':'r_rdt_na'}, years=30, tc=38.0, rdt='not_available')
t('O02','urgent_referral','high',{'r_rdt_na_urgent':True,'r_ds_convulsions':True}, years=30, danger='convulsions', tc=38.0, rdt='not_available')
t('O03','referral','moderate',{'r_rdt_na':True,'r_tb':True,'suspected_tb':False}, years=30, tc=38.0, cough='yes', two_weeks_cough='yes', blood='no', rdt='not_available')
t('O04','rest','low',{'rest_fever_txt':True}, years=30, tc=38.0, rdt='negative')
t('O05','rest','low',{'rest_fever_txt':False}, years=30, tc=36.8, hist='no')
t('O06','urgent_referral','high',{'referral_reasons':'r_ds_confusion r_ds_convulsions r_temp_high'}, years=30, danger='convulsions confusion', tf=103.0, rdt='negative')
t('O07','malaria_treatment','moderate',{'referral_reasons':'m_rash'}, years=10, tc=38.0, rash='yes', rdt='pos_falci', weight=30)
t('O08','rest','low',{'referral_reasons':''}, years=30, tc=36.8, hist='no')
t('P01','referral','moderate',{'r_prolonged':True,'r_preg_info':True,'r_pregnant':False}, years=25, sex='female', pregnant='yes', tf=100.0, fever7='yes', rdt='negative')
t('P02','referral','moderate',{'r_pregnant':True,'r_preg_info':False}, years=25, sex='female', pregnant='yes', tf=100.6, rdt='negative')
t('P03','urgent_referral','high',{'r_preg_urgent':True,'r_ds_convulsions':True}, years=25, sex='female', pregnant='yes', danger='convulsions', tf=98.2, hist='no')
t('P04','referral','moderate',{'r_preg_info':False}, years=25, sex='female', pregnant='no', tf=100.0, fever7='yes', rdt='negative')
t('P05','severe_malaria','high',{'sm_preg':True,'sm_ds_convulsions':True}, years=25, sex='female', pregnant='yes', danger='convulsions', tc=38.0, rdt='pos_falci', weight=55)
# --- Symptom assessment is skipped only when urgent referral is already certain ---
t('K01','urgent_referral','high',{'all_symptoms':True,'r_blood_stool':True,'r_malaria_pf':True,'uncomplicated_malaria':False}, years=30, tf=103.0, intestinal='blood_stool', rdt='pos_falci', weight=50)
t('K02','malaria_treatment','moderate',{'all_symptoms':True,'m_rash':True,'malaria_refer_now_txt':True}, years=10, tf=103.0, rash='yes', rdt='pos_falci', weight=30)
t('K03','urgent_referral','high',{'all_symptoms':True,'r_temp_high':True}, years=30, tf=103.0, rash='yes', rdt='negative')
t('K04','urgent_referral','high',{'all_symptoms':True,'r_blood_stool':True,'r_preg_urgent':True}, years=25, sex='female', pregnant='yes', tf=100.6, intestinal='blood_stool', rdt='negative')
t('K05','urgent_referral','high',{'all_symptoms':True,'r_blood_stool':True}, age_days=30, tc=36.8, hist='yes', intestinal='blood_stool', rdt='negative')
t('K06','malaria_treatment','moderate',{'fever_7_days':True,'m_prolonged':True}, years=30, tf=103.0, fever7='yes', rdt='pos_vivax', weight=50)
t('K07','urgent_referral','high',{'all_symptoms':False,'r_temp_low':True}, years=30, tf=94.5, hist='no')
t('K08','urgent_referral','high',{'all_symptoms':False,'r_temp_high':True}, age_days=30, tc=38.0)
# --- Malaria uncomplicated ---
t('M01','rest','low',{'rdt_group':True,'history_fever':True}, years=30, tc=36.8, hist='yes', rdt='negative')
t('M02','rest','low',{'rdt_group':False}, years=30, tc=36.8, hist='no')
t('M03','malaria_treatment','moderate',{'dosage_act':'one tablet','primaquine_pf':False,'falciparum':True}, years=0, months=3, tc=38.0, fever7='no', rdt='pos_falci', weight=4)
t('M04','malaria_treatment','moderate',{'dosage_chloroquine':'1/4 tablet','dosage_chloroquine_day_3':'1/4 tablet','primaquine':False}, years=0, months=3, tc=38.0, fever7='no', rdt='pos_vivax', weight=4)
t('M05','malaria_treatment','moderate',{'primaquine':False,'vivax_infection':True,'m_pregnant':True,'malaria_refer_now_txt':True,'referral':False}, years=25, sex='female', pregnant='yes', tc=38.0, rdt='pos_vivax', weight=50)
t('M18','malaria_treatment','moderate',{'dosage_act':'four tablets','primaquine_pf':False,'falciparum':True,'m_pregnant':True}, years=24, sex='female', pregnant='yes', tc=37.8, rdt='pos_falci', weight=55)
t('M06','malaria_treatment','moderate',{'primaquine':False,'breastfeeding_u6m':True}, years=25, sex='female', pregnant='no', tc=38.0, rdt='pos_vivax', weight=50, bf='yes')
t('M07','malaria_treatment','moderate',{'dosage_chloroquine':'one and 1/2 tablets','dosage_chloroquine_day_3':'3/4 tablet','dosage_primaquine':'5','primaquine':True,'followup_vivax':True}, years=6, tc=38.0, rdt='pos_vivax', weight=20)
t('M08','malaria_treatment','moderate',{'dosage_act':'three tablets','dosage_primaquine':'7.5','primaquine_pf':True,'followup_falciparum':True,'caution_primaquine_pf':True}, years=30, tc=38.0, rdt='pos_falci', weight=30)
t('M09','malaria_treatment','moderate',{'dosage_act':'two tablets','dosage_primaquine':'4.5','primaquine_pf':True}, years=6, tc=38.0, rdt='pos_falci', weight=18)
t('M10','malaria_treatment','moderate',{'dosage_act':'four tablets','dosage_primaquine':'12.5','primaquine_mix':True,'followup_mixed':True,'mixed_infection':True}, years=30, tc=38.0, rdt='pos_mixed', weight=50)
t('M11','malaria_treatment','moderate',{'caution_primaquine':True}, years=30, tc=38.0, rdt='pos_vivax', weight=50)
t('M12','malaria_treatment','moderate',{'dosage_chloroquine':'1/4 tablet'}, years=0, months=7, tc=38.0, fever7='no', rdt='pos_vivax', weight=5.5)
t('M13','malaria_treatment','moderate',{'dosage_chloroquine':'1/2 tablet'}, years=1, tc=38.0, fever7='no', rdt='pos_vivax', weight=9.5)
t('M14','malaria_treatment','moderate',{'TB_clinic':True}, years=30, tc=38.0, cough='yes', two_weeks_cough='yes', blood='no', rdt='pos_falci', weight=50)
t('M15','malaria_treatment','moderate',{'primaquine':False}, years=0, months=5, tc=38.0, fever7='no', rdt='pos_vivax', weight=7)
t('M16','malaria_treatment','moderate',{'primaquine':False}, age_days=150, tc=38.0, fever7='no', rdt='pos_vivax', weight=7)
t('M17','malaria_treatment','moderate',{'uncomplicated_malaria':True,'severe_illness':False}, years=30, tf=102.5, rdt='pos_falci', weight=50)
# --- Malaria severe ---
t('H01','severe_malaria','high',{'sm_ds_convulsions':True,'reasons_severe_malaria':True,'artesunate_dosage':'120','severe_malaria_less_6a':True,'severe_malaria_more_6a':False}, years=2, danger='convulsions', tc=38.0, rdt='pos_falci', weight=12)
t('H02','severe_malaria','high',{'severe_malaria_less_6a':False,'severe_malaria_more_6a':True,'artesunate_im_dosage':'14.4'}, years=0, months=4, danger='convulsions', tc=38.0, rdt='pos_falci', weight=6)
t('H03','severe_malaria','high',{'severe_malaria_more_6a':True,'artesunate_im_dosage':'48'}, years=6, danger='convulsions', tc=38.0, rdt='pos_falci', weight=20)
t('H04','severe_malaria','high',{'severe_malaria_more_6a':True,'artesunate_im_dosage':'120'}, years=25, danger='convulsions', tc=38.0, rdt='pos_falci', weight=50)
t('H05','severe_malaria','high',{'severe_malaria_less_6b':True,'artesunate_im_dosage':'28.8'}, years=2, danger='convulsions', tc=38.0, rdt='pos_falci', weight=12)
t('H06','urgent_referral','high',{'r_malaria_pv':True,'r_ds_convulsions':True,'severe_malaria':False,'severe_illness':True}, years=30, danger='convulsions', tc=38.0, rdt='pos_vivax', weight=50)
t('H07','severe_malaria','high',{'severe_malaria_more_6a':True}, years=30, danger='confusion', tc=38.0, rdt='pos_mixed', weight=50)
t('H08','severe_malaria','high',{'severe_malaria_less_6a':True}, age_days=200, danger='convulsions', tc=38.0, rdt='pos_falci', weight=7)
# --- Usability scenarios ---
t('U01','tb_referral','moderate',{}, years=4, tf=100.1, fever7='no', systemic='fatigue', one_week='no', cough='yes', two_weeks_cough='yes', blood='no', rdt='negative')
t('U02','malaria_treatment','moderate',{'dosage_act':'two tablets','dosage_primaquine':'4.5'}, years=6, tf=101.2, systemic='headache', one_week='no', rdt='pos_falci', weight=18)

# --- Table 1 traceability: each test case cites the Table 1 row(s) it checks ---
TABLE1_ROWS = 35
SIGN_ROW = {'difficult_breathing': 1, 'severe_abdominal_pain': 2, 'loss_of_consciousness': 3, 'convulsions': 4, 'not_drinking': 5,
            'confusion': 6, 'vomits_everything': 7, 'extreme_weakness': 8, 'severe_headache': 9, 'jaundice_pallor': 10,
            'urine_bleeding': 11, 'fast_breathing': 12, 'chest_indrawing': 12, 'movement_stimulated': 12}
ROWS = {
 'T01': [13, 35], 'T02': [13], 'T03': [13, 35], 'T04': [13], 'T05': [13], 'T06': [13, 35], 'T07': [14], 'T08': [16], 'T09': [16, 35],
 'T10': [14], 'T11': [14, 35], 'T12': [16, 35], 'T13': [14, 35], 'T14': [14], 'T15': [14], 'T16': [15, 35], 'T17': [15], 'T18': [13, 35],
 'T19': [17], 'T20': [13, 35], 'T21': [13, 35],
 'G01': [24], 'G02': [25], 'G03': [25], 'G04': [26], 'G05': [26, 35], 'G06': [26], 'G07': [26, 35], 'G08': [26], 'G09': [26], 'G10': [26, 35],
 'S01': [23], 'S02': [23], 'S03': [18], 'S04': [21], 'S05': [27], 'S06': [11], 'S07': [18, 35], 'S08': [20], 'S09': [9, 15],
 'R01': [4, 6, 14], 'R02': [19], 'R03': [18], 'R04': [22],
 'N01': [18, 21], 'N02': [18], 'N03': [22, 35], 'N04': [21], 'N05': [24, 26], 'N06': [26], 'N07': [25, 26],
 'A01': [27, 29], 'A02': [20, 29], 'A03': [26, 29], 'A04': [21, 22, 29], 'A05': [18, 19, 26, 28],
 'C01': [24, 27, 33], 'C02': [25, 33], 'C03': [16, 18], 'C04': [16, 29], 'C05': [17, 32],
 'B01': [23], 'B02': [23, 27], 'B03': [16, 23], 'B04': [23, 28], 'B05': [23, 27, 29], 'B06': [21, 23, 29], 'B07': [23, 24],
 'V01': [14, 33], 'V02': [14, 28], 'V03': [32], 'V04': [30, 32], 'V05': [16], 'V06': [16, 35], 'V07': [15], 'V08': [15, 35], 'V09': [15, 35],
 'O01': [34], 'O02': [4, 34], 'O03': [23, 34], 'O04': [35], 'O05': [35], 'O06': [4, 6, 14], 'O07': [27, 29], 'O08': [35],
 'P01': [15, 16], 'P02': [15], 'P03': [4, 15], 'P04': [16], 'P05': [15, 30],
 'M01': [28, 35], 'M02': [35], 'M03': [28], 'M04': [28], 'M05': [15, 28, 29], 'M18': [15, 28, 29], 'M06': [28], 'M07': [28], 'M08': [28],
 'M09': [28], 'M10': [28], 'M11': [28], 'M12': [28], 'M13': [28], 'M14': [23, 28], 'M15': [28], 'M16': [28], 'M17': [14, 28],
 'H01': [30], 'H02': [30], 'H03': [30], 'H04': [30], 'H05': [30], 'H06': [31], 'H07': [30], 'H08': [30], 'H09': [10, 30], 'K01': [14, 24, 33], 'K02': [14, 27, 29], 'K03': [14], 'K04': [15, 24], 'K05': [17, 24], 'K06': [14, 16, 29], 'K07': [14], 'K08': [13],
 'U01': [23], 'U02': [28]}
for cid, kw, *_ in T:
    if cid.startswith('D'): ROWS[cid] = [SIGN_ROW[kw['danger']]]
_missing_tests = [c for c, *_ in T if not ROWS.get(c)]
_covered = {r for v in ROWS.values() for r in v}
_uncovered = [r for r in range(1, TABLE1_ROWS + 1) if r not in _covered]
_unknown = [c for c in ROWS if c not in {x[0] for x in T}]

from cases import case as mk
res = run([mk(cid, **kw) for cid, kw, *_ in T])
fails = 0
for cid, kw, er, el, ch in T:
    r = res[cid]; bad = []
    if r['recommendation'][0] != er: bad.append(f"rec {r['recommendation'][0]}!={er}")
    if r['emergency_level_calc'][0] != el: bad.append(f"lvl {r['emergency_level_calc'][0]}!={el}")
    for k, v in ch.items():
        got = r[k][1] if isinstance(v, bool) else r[k][0]
        if isinstance(v, str) and got != v: bad.append(f'{k}={got}!={v}')
        if isinstance(v, bool) and got != v: bad.append(f'{k} rel={got}!={v}')
    if bad: fails += 1; print('FAIL', cid, '; '.join(bad))
# --- Structural check: young-infant danger signs exist and are filtered to babies under 2 months ---
import re as _re
_x = open(sys.argv[1], encoding='utf8').read(); _i = _x.index('<instance id="df96d69">'); _seg = _x[_i:_x.index('</instance>', _i)]
for _n in ('fast_breathing', 'chest_indrawing', 'movement_stimulated'):
    if not _re.search(r'<name>%s</name>(?:<order>\d+</order>)?<infant_only>yes</infant_only>' % _n, _seg): fails += 1; print('FAIL structure: option missing or not infant-only:', _n)
if "young_infant  = 'yes' or infant_only = 'no'" not in _x: fails += 1; print('FAIL structure: danger-sign choice filter missing')
if _missing_tests or _uncovered or _unknown:
    fails += 1; print('FAIL traceability: tests without a Table 1 row:', _missing_tests, '| rows without a test:', _uncovered, '| unknown IDs:', _unknown)
print(f'Table 1 coverage: {len(_covered)} of {TABLE1_ROWS} rows tested')
print(f'{len(T)} cases, {fails} failed')
import json; json.dump({c: {k: v for k, v in d.items()} for c, d in res.items()}, open('results.json', 'w'))
