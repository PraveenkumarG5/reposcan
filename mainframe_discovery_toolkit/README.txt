Mainframe Discovery Toolkit
===========================

This toolkit contains Python scripts to analyze Mainframe COBOL/JCL code during modernization projects.

Scripts Included
----------------
1. generate_inventory.py
   Generates a mainframe inventory workbook:
   - Programs
   - Batch Job Flow
   - File Usage
   - Copybooks
   - Database tables
   - Utilities
   - GDG usage

2. file_flow_mapper.py
   Detects producer and consumer programs for files and generates file flow architecture.

3. cluster_programs.py
   Uses program dependencies to group programs into clusters for migration planning.

4. business_rule_extractor.py
   Extracts business rules from COBOL code (IF, EVALUATE, MOVE statements).

5. deep_mainframe_dependency_scan.py
   Deep scan of code to identify:
   - DB2 tables and CRUD operations
   - GDG datasets
   - VSAM detection
   - Flat file usage
   - External program calls

Requirements
------------
Python 3.9+

Install dependencies:

pip install pandas openpyxl networkx graphviz

Recommended Folder Structure
----------------------------

project/
    scripts/
    Mainframe/
        CPY/
        CTC/
        DCL/
        JCL/
        PRC/
        SRD/

Run Scripts
-----------

python generate_inventory.py
python file_flow_mapper.py
python cluster_programs.py
python business_rule_extractor.py
python deep_mainframe_dependency_scan.py

Outputs
-------

The scripts generate Excel workbooks such as:

Mainframe_Inventory.xlsx
File_Flow_Architecture.xlsx
Program_Clusters.xlsx
Business_Rules.xlsx
Mainframe_Deep_Dependency_Report.xlsx

These outputs help build:

- Program dependency diagrams
- Batch job flows
- File flow architecture
- Business rule documentation
- External dependency mapping

Useful for Mainframe to Java modernization projects.