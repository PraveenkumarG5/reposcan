import os
import re
import pandas as pd

COBOL_DIR="Mainframe/CTC"

if_pattern=re.compile(r"\bIF\b(.*)",re.IGNORECASE)
move_pattern=re.compile(r"MOVE\s+(\w+)\s+TO\s+(\w+)",re.IGNORECASE)
evaluate_pattern=re.compile(r"EVALUATE\s+(.*)",re.IGNORECASE)
when_pattern=re.compile(r"WHEN\s+(.*)",re.IGNORECASE)

rules=[]
mappings=[]

for file in os.listdir(COBOL_DIR):
    path=os.path.join(COBOL_DIR,file)
    if not os.path.isfile(path):
        continue

    program=file.split(".")[0]

    with open(path,errors="ignore") as f:
        for line in f:
            line=line.strip()

            if if_pattern.search(line):
                rules.append({"Program":program,"Rule_Type":"IF","Condition":line})

            m=move_pattern.search(line)
            if m:
                mappings.append({"Program":program,"Source":m.group(1),"Target":m.group(2)})

            if evaluate_pattern.search(line):
                rules.append({"Program":program,"Rule_Type":"EVALUATE","Condition":line})

            if when_pattern.search(line):
                rules.append({"Program":program,"Rule_Type":"WHEN","Condition":line})

with pd.ExcelWriter("Business_Rules.xlsx") as writer:
    pd.DataFrame(rules).to_excel(writer,"Rules",index=False)
    pd.DataFrame(mappings).to_excel(writer,"Field_Mappings",index=False)

print("Business rules extracted")