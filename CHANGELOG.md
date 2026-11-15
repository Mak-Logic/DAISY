# DAISY changelog

## v4 (November 2026)
Changes from v3b, the version used in the 2025 pilot. Temperatures are entered in F; C in brackets. Sources in square brackets; "co-design" marks rules set by the study team where guidelines give none.

### Opening screen and danger signs
- Opening screen lists non-febrile emergencies for immediate referral, including violent behaviour toward self or others [IMAI]
- Danger signs added or reworded: vomits everything; neck stiffness, or severe headache with intolerance to bright light; yellow eyes or skin, or very pale palms, tongue or eyes; dark urine or very little urine, or unusual bleeding; unusually sleepy, lethargic or unconscious; confusion or unusual behaviour [IMCI; IMAI; national malaria and dengue guidelines]
- Three additional danger signs for young infants: fast breathing, severe chest indrawing, moves only when stimulated or not at all [IMCI].

### Age and temperature
- Young infants: 0-59 days (or 0-1 completed months if date of birth unknown); the "under 4 months" rule was removed
- Urgent referral for temperature: young infants ≥99.5 F (37.5 C) or <95.9 F (35.5 C) [IMCI]; all others ≥102.2 F (39.0 C) [co-design] or <95.0 F (35.0 C). Malaria with ≥39.0 C and no danger sign is treated as uncomplicated malaria
- Pregnancy asked from 12-49 years (previously 15-49); referral if temperature >100.4 F (38.0 C) [PCPNC] or positive malaria test (after starting treatment)
- Malaria testing for fever ≥99.5 F (37.5 C) or fever in the past 48 hours (previously 72 hours) [IMCI].
- Referral for fever every day for more than 7 days, from 2 months of age [IMCI; co-design for adults].
- Young infants with reported fever in the past 48 hours and normal temperature: referral.

### Symptoms
- Separate duration question for each symptom: headache and fatigue ≥7 days, night sweats ≥14 days [co-design]; weight loss, severe muscle or joint pain and chest pain referred without duration.
- Blood in stool and diarrhoea ≥14 days: urgent referral [IMCI]; age-specific duration thresholds for diarrhoea and vomiting [co-design].
- Rash referred when accompanied by fever; chest pain removed from the TB pathway.
- TB referral for cough ≥2 weeks or cough with blood [national TB guideline].
- Symptoms are skipped only when urgent referral is already certain; patients with ≥39.0 C, pregnant women with fever and young infants with reported fever are assessed for symptoms.

### Malaria
- Pre-referral artesunate only for P. falciparum or mixed infection with a danger sign: rectal 10 mg/kg (6 months to <6 years) or IM 2.4 mg/kg via CHCP (other ages, or if suppositories unavailable) [national CHW manual]. P. vivax with a danger sign: urgent referral.
- Single-dose primaquine for P. falciparum; primaquine withheld in pregnancy, under 6 months or 5 kg, and for mothers breastfeeding babies under 6 months [national CHW manual].
- Young infants with a positive test: urgent referral, no CHW treatment [IMCI].
- Another urgent finding replaces malaria treatment with urgent referral; findings unlikely to be explained by malaria lead to referral alongside treatment
- "Test not available" option: referral for testing

### Recommendation page
- One recommendation and one destination per patient, on a single page, with the reasons for referral listed and saved (`referral_reasons`).
- TB symptoms with any other referral reason: one health centre referral.
- Rest advice for fever with negative test: follow-up after 3 days if fever persists [IMCI].

### Testing
- 152 automated test cases, covering all 35 rules, run with JavaRosa (see tests/README.md); 20 cases also checked manually in KoboToolbox.