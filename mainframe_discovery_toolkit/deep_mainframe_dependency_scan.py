import os
import re
import pandas as pd

BASE_DIR="Mainframe"

db2_records=[]
gdg_records=[]
vsam_records=[]
flat_files=[]
external_calls=[]

sql_block_pattern=re.compile(r"EXEC\s+SQL(.*?)END-EXEC",re.IGNORECASE|re.DOTALL)
table_pattern=re.compile(r"(FROM|INTO|UPDATE|DELETE\s+FROM)\s+([A-Z0-9_]+)",re.IGNORECASE)
select_pattern=re.compile(r"SELECT\s+([A-Z0-9_]+)",re.IGNORECASE)
open_input_pattern=re.compile(r"OPEN\s+INPUT\s+([A-Z0-9_-]+)",re.IGNORECASE)
open_output_pattern=re.compile(r"OPEN\s+OUTPUT\s+([A-Z0-9_-]+)",re.IGNORECASE)
call_pattern=re.compile(r"CALL\s+'?([A-Z0-9_-]+)'?",re.IGNORECASE)
vsam_pattern=re.compile(r"ORGANIZATION\s+IS\s+INDEXED",re.IGNORECASE)
gdg_pattern=re.compile(r"([A-Z0-9\.]+\([+-]?\d+\))",re.IGNORECASE)

def scan_file(file_path,program):
    with open(file_path,errors="ignore") as f:
        content=f.read()

    for block in sql_block_pattern.findall(content):
        operation="UNKNOWN"
        if "SELECT" in block.upper(): operation="SELECT"
        elif "INSERT" in block.upper(): operation="INSERT"
        elif "UPDATE" in block.upper(): operation="UPDATE"
        elif "DELETE" in block.upper(): operation="DELETE"

        for t in table_pattern.findall(block):
            db2_records.append({"Program":program,"Table":t[1],"Operation":operation})

    for m in select_pattern.findall(content):
        flat_files.append({"Program":program,"File":m,"Access":"SELECT"})

    for m in open_input_pattern.findall(content):
        flat_files.append({"Program":program,"File":m,"Access":"READ"})

    for m in open_output_pattern.findall(content):
        flat_files.append({"Program":program,"File":m,"Access":"WRITE"})

    if vsam_pattern.search(content):
        vsam_records.append({"Program":program,"VSAM_Detected":"YES"})

    for g in gdg_pattern.findall(content):
        gdg_records.append({"Program":program,"GDG_Dataset":g})

    for c in call_pattern.findall(content):
        external_calls.append({"Program":program,"Calls":c})

for root,dirs,files in os.walk(BASE_DIR):
    for file in files:
        if file.lower().endswith((".cbl",".cob",".cobol",".cpy")):
            scan_file(os.path.join(root,file),file.split(".")[0])

with pd.ExcelWriter("Mainframe_Deep_Dependency_Report.xlsx") as writer:
    pd.DataFrame(db2_records).to_excel(writer,"DB2_CRUD_Access",index=False)
    pd.DataFrame(gdg_records).to_excel(writer,"GDG_Datasets",index=False)
    pd.DataFrame(vsam_records).to_excel(writer,"VSAM_Files",index=False)
    pd.DataFrame(flat_files).to_excel(writer,"Flat_File_Access",index=False)
    pd.DataFrame(external_calls).to_excel(writer,"External_Program_Calls",index=False)

print("Deep dependency scan completed")