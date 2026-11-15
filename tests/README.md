# DAISY automated tests

All checks run the DAISY XForm in JavaRosa, the open-source ODK form engine. For each case the scripts enter the answers in form order (skipping questions the form does not show) and read back the calculated recommendation, emergency level, doses, the screens shown and the reasons listed.

Requirements: Python 3, a Java runtime (Java 8 or later), and `pip3 install pyxform` (pyxform bundles ODK Validate, which contains JavaRosa, and installs openpyxl). `Run.class` is included, so no Java compiler is needed; to rebuild it from `Run.java`, use the `javac` line below with a full JDK.

```
python3 -m pyxform.xls2xform ../DAISY_v4.xlsx DAISY_v4.xml
J=$(python3 -c "import pyxform,os;print(os.path.join(os.path.dirname(pyxform.__file__),'validators/odk_validate/bin/ODK_Validate.jar'))")
javac -cp $J Run.java                          # only needed if Run.class is rebuilt
python3 tests.py DAISY_v4.xml                  # 152 test cases (S1 File)       -> "Table 1 coverage: 35 of 35 rows tested" and "152 cases, 0 failed"
python3 make_s1.py DAISY_v4.xml S1_File.xlsx   # writes S1 File from the test cases

```

Files
- `Run.java`: drives JavaRosa (SET answer, OUT read value and visibility, END).
- `cases.py`: builds the answer sequence for a case; temperatures may be given in °C and are converted to °F.
- `tests.py`: the 152 cases with expected results, each linked to the Table 1 row(s) it checks, with a check that every row of Table 1 is covered, plus a structural check that the young-infant danger signs exist and are filtered to babies under 2 months.
- `make_s1.py`: produces S1 File.

Limits: JavaRosa is the engine used by ODK Collect. KoboToolbox web forms use Enketo, which can behave differently for on-screen display (choice filters, layout) and for hidden answers; those aspects were checked by hand in Kobo.

Lines starting with `WARN ... skipped (not shown)` are expected: they are answers in a test case that the form correctly does not ask for (for example pregnancy for a male patient).
