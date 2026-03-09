
"""
Mainframe Enterprise Discovery Tool
----------------------------------
Single CLI tool that performs:
- Inventory generation
- File flow mapping
- Program clustering
- Business rule extraction
- Deep dependency scan (DB2, GDG, VSAM, flat files)
"""

import os
import re
import argparse
import pandas as pd
import networkx as nx

BASE_DIR = "Mainframe"

# regex patterns
call_pattern = re.compile(r"CALL\s+'?([A-Z0-9_-]+)'?", re.IGNORECASE)
copy_pattern = re.compile(r"COPY\s+([A-Z0-9_-]+)", re.IGNORECASE)
sql_block_pattern = re.compile(r"EXEC\s+SQL(.*?)END-EXEC", re.IGNORECASE | re.DOTALL)
table_pattern = re.compile(r"(FROM|INTO|UPDATE|DELETE\s+FROM)\s+([A-Z0-9_]+)", re.IGNORECASE)
open_input_pattern = re.compile(r"OPEN\s+INPUT\s+([A-Z0-9_-]+)", re.IGNORECASE)
open_output_pattern = re.compile(r"OPEN\s+OUTPUT\s+([A-Z0-9_-]+)", re.IGNORECASE)
read_pattern = re.compile(r"READ\s+([A-Z0-9_-]+)", re.IGNORECASE)
write_pattern = re.compile(r"WRITE\s+([A-Z0-9_-]+)", re.IGNORECASE)
select_pattern = re.compile(r"SELECT\s+([A-Z0-9_-]+)", re.IGNORECASE)
if_pattern = re.compile(r"\bIF\b(.*)", re.IGNORECASE)
move_pattern = re.compile(r"MOVE\s+(\w+)\s+TO\s+(\w+)", re.IGNORECASE)
evaluate_pattern = re.compile(r"EVALUATE\s+(.*)", re.IGNORECASE)
when_pattern = re.compile(r"WHEN\s+(.*)", re.IGNORECASE)
vsam_pattern = re.compile(r"ORGANIZATION\s+IS\s+INDEXED", re.IGNORECASE)
gdg_pattern = re.compile(r"([A-Z0-9\.]+\([+-]?\d+\))", re.IGNORECASE)

def scan_cobol(base):
    programs=[]
    copybooks=[]
    db=[]
    file_reads=[]
    file_writes=[]
    rules=[]
    mappings=[]
    gdgs=[]
    vsams=[]
    
    for root,_,files in os.walk(base):
        for file in files:
            if not file.lower().endswith((".cbl",".cob",".cobol",".cpy")):
                continue
            
            program=file.split(".")[0]
            path=os.path.join(root,file)
            
            with open(path,errors="ignore") as f:
                content=f.read()
                lines=f.readlines()
            
            for c in call_pattern.findall(content):
                programs.append((program,c))
            
            for cp in copy_pattern.findall(content):
                copybooks.append((cp,program))
            
            for block in sql_block_pattern.findall(content):
                op="UNKNOWN"
                if "SELECT" in block.upper(): op="SELECT"
                elif "INSERT" in block.upper(): op="INSERT"
                elif "UPDATE" in block.upper(): op="UPDATE"
                elif "DELETE" in block.upper(): op="DELETE"
                
                for t in table_pattern.findall(block):
                    db.append((program,t[1],op))
            
            for r in open_input_pattern.findall(content)+read_pattern.findall(content):
                file_reads.append((program,r))
            
            for w in open_output_pattern.findall(content)+write_pattern.findall(content):
                file_writes.append((program,w))
            
            for g in gdg_pattern.findall(content):
                gdgs.append((program,g))
            
            if vsam_pattern.search(content):
                vsams.append((program,"YES"))
            
            for line in lines:
                if if_pattern.search(line):
                    rules.append((program,"IF",line.strip()))
                if evaluate_pattern.search(line):
                    rules.append((program,"EVALUATE",line.strip()))
                if when_pattern.search(line):
                    rules.append((program,"WHEN",line.strip()))
                
                m=move_pattern.search(line)
                if m:
                    mappings.append((program,m.group(1),m.group(2)))
    
    return programs,copybooks,db,file_reads,file_writes,rules,mappings,gdgs,vsams

def build_file_flow(reads,writes):
    flow=[]
    for p_out,f in writes:
        for p_in,f2 in reads:
            if f==f2:
                flow.append((p_out,f,p_in))
    return flow

def cluster_programs(programs):
    G=nx.DiGraph()
    for p,c in programs:
        G.add_edge(p,c)
    clusters=list(nx.connected_components(G.to_undirected()))
    
    rows=[]
    for i,c in enumerate(clusters):
        for p in c:
            rows.append((f"Cluster_{i+1}",p))
    return rows

def run_scan():
    cobol=os.path.join(BASE_DIR)
    
    programs,copybooks,db,reads,writes,rules,mappings,gdgs,vsams=scan_cobol(cobol)
    
    flow=build_file_flow(reads,writes)
    clusters=cluster_programs(programs)
    
    with pd.ExcelWriter("Mainframe_Discovery_Report.xlsx") as writer:
        
        pd.DataFrame(programs,columns=["Program","Calls"]).to_excel(writer,"Program_Dependencies",index=False)
        pd.DataFrame(copybooks,columns=["Copybook","Used_By"]).to_excel(writer,"Copybooks",index=False)
        pd.DataFrame(db,columns=["Program","Table","Operation"]).to_excel(writer,"DB2_CRUD",index=False)
        pd.DataFrame(reads,columns=["Program","Input_File"]).to_excel(writer,"File_Reads",index=False)
        pd.DataFrame(writes,columns=["Program","Output_File"]).to_excel(writer,"File_Writes",index=False)
        pd.DataFrame(flow,columns=["Producer","File","Consumer"]).to_excel(writer,"File_Flow",index=False)
        pd.DataFrame(clusters,columns=["Cluster","Program"]).to_excel(writer,"Program_Clusters",index=False)
        pd.DataFrame(rules,columns=["Program","Rule_Type","Rule"]).to_excel(writer,"Business_Rules",index=False)
        pd.DataFrame(mappings,columns=["Program","Source","Target"]).to_excel(writer,"Field_Mappings",index=False)
        pd.DataFrame(gdgs,columns=["Program","GDG"]).to_excel(writer,"GDG_Usage",index=False)
        pd.DataFrame(vsams,columns=["Program","VSAM"]).to_excel(writer,"VSAM_Detection",index=False)
    
    print("Discovery report generated: Mainframe_Discovery_Report.xlsx")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Mainframe Enterprise Discovery Tool")
    parser.add_argument("--scan",action="store_true",help="Run full discovery scan")
    
    args=parser.parse_args()
    
    if args.scan:
        run_scan()
    else:
        print("Use --scan to run discovery")
