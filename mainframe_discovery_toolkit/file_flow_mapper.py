import os
import re
import pandas as pd

BASE_DIR="Mainframe/CTC"

input_pattern=re.compile(r"OPEN\s+INPUT\s+(\w+)",re.IGNORECASE)
output_pattern=re.compile(r"OPEN\s+OUTPUT\s+(\w+)",re.IGNORECASE)
read_pattern=re.compile(r"READ\s+(\w+)",re.IGNORECASE)
write_pattern=re.compile(r"WRITE\s+(\w+)",re.IGNORECASE)

program_inputs=[]
program_outputs=[]

for file in os.listdir(BASE_DIR):
    path=os.path.join(BASE_DIR,file)
    if not os.path.isfile(path):
        continue

    program=file.split(".")[0]

    with open(path,errors="ignore") as f:
        content=f.read()

    inputs=input_pattern.findall(content)+read_pattern.findall(content)
    outputs=output_pattern.findall(content)+write_pattern.findall(content)

    for i in inputs:
        program_inputs.append({"Program":program,"Input_File":i})

    for o in outputs:
        program_outputs.append({"Program":program,"Output_File":o})

df_inputs=pd.DataFrame(program_inputs)
df_outputs=pd.DataFrame(program_outputs)

file_flow=[]

for _,out_row in df_outputs.iterrows():
    file_name=out_row["Output_File"]
    producer=out_row["Program"]
    consumers=df_inputs[df_inputs["Input_File"]==file_name]

    for _,in_row in consumers.iterrows():
        file_flow.append({
            "Producer_Program":producer,
            "File":file_name,
            "Consumer_Program":in_row["Program"]
        })

pd.DataFrame(file_flow).to_excel("File_Flow_Architecture.xlsx",index=False)
print("File flow generated")