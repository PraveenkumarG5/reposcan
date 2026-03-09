import os
import re
import pandas as pd

BASE_DIR = "Mainframe"

programs = []
copybooks = []
db_tables = []
file_usage = []
job_flow = []
utilities = []
gdg_usage = []

call_pattern = re.compile(r"CALL\s+'?(\w+)'?", re.IGNORECASE)
copy_pattern = re.compile(r"COPY\s+(\w+)", re.IGNORECASE)
sql_pattern = re.compile(r"FROM\s+(\w+)", re.IGNORECASE)
file_read_pattern = re.compile(r"OPEN\s+INPUT\s+(\w+)", re.IGNORECASE)
file_write_pattern = re.compile(r"OPEN\s+OUTPUT\s+(\w+)", re.IGNORECASE)
select_pattern = re.compile(r"SELECT\s+(\w+)", re.IGNORECASE)
jcl_exec_pattern = re.compile(r"EXEC\s+PGM=(\w+)", re.IGNORECASE)
utility_pattern = re.compile(r"(SORT|IDCAMS|FTP)", re.IGNORECASE)
gdg_pattern = re.compile(r"\(\+?\-?\d+\)")

for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        path = os.path.join(root, file)
        program = file.split(".")[0]

        if file.lower().endswith((".cbl",".cob",".cobol",".cpy")):
            with open(path, errors="ignore") as f:
                content = f.read()

            for c in call_pattern.findall(content):
                programs.append({"Program":program,"Calls":c})

            for cp in copy_pattern.findall(content):
                copybooks.append({"Copybook":cp,"Used By":program})

            for t in sql_pattern.findall(content):
                db_tables.append({"Program":program,"Table":t})

            for r in file_read_pattern.findall(content):
                file_usage.append({"Program":program,"File":r,"Operation":"READ"})

            for w in file_write_pattern.findall(content):
                file_usage.append({"Program":program,"File":w,"Operation":"WRITE"})

            for s in select_pattern.findall(content):
                file_usage.append({"Program":program,"File":s,"Operation":"SELECT"})

            for g in gdg_pattern.findall(content):
                gdg_usage.append({"Program":program,"GDG":g})

        if file.lower().endswith(".jcl"):
            job = program
            with open(path, errors="ignore") as f:
                for line in f:
                    m = jcl_exec_pattern.search(line)
                    if m:
                        job_flow.append({"Job":job,"Program":m.group(1)})

                    u = utility_pattern.search(line)
                    if u:
                        utilities.append({"Job":job,"Utility":u.group(1)})

df_programs=pd.DataFrame(programs)
df_jobs=pd.DataFrame(job_flow)
df_files=pd.DataFrame(file_usage)
df_copy=pd.DataFrame(copybooks)
df_db=pd.DataFrame(db_tables)
df_utils=pd.DataFrame(utilities)
df_gdg=pd.DataFrame(gdg_usage)

with pd.ExcelWriter("Mainframe_Inventory.xlsx") as writer:
    df_programs.to_excel(writer,"Programs",index=False)
    df_jobs.to_excel(writer,"Batch_Job_Flow",index=False)
    df_files.to_excel(writer,"File_Usage",index=False)
    df_copy.to_excel(writer,"Copybooks",index=False)
    df_db.to_excel(writer,"Database",index=False)
    df_utils.to_excel(writer,"Utilities",index=False)
    df_gdg.to_excel(writer,"GDG_Usage",index=False)

print("Inventory workbook generated")