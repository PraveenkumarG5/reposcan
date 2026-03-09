import pandas as pd
import networkx as nx

df=pd.read_excel("Mainframe_Inventory.xlsx",sheet_name="Programs")

G=nx.DiGraph()

for _,row in df.iterrows():
    G.add_edge(row["Program"],row["Calls"])

UG=G.to_undirected()
clusters=list(nx.connected_components(UG))

rows=[]
cid=1

for cluster in clusters:
    for prog in cluster:
        rows.append({"Cluster":f"Cluster_{cid}","Program":prog})
    cid+=1

pd.DataFrame(rows).to_excel("Program_Clusters.xlsx",index=False)
print("Clusters generated")