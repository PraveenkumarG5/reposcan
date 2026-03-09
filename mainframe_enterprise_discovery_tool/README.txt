
Mainframe Enterprise Discovery Tool
===================================

Purpose
-------
This tool performs a complete automated discovery of mainframe COBOL systems before migration to Java.

Capabilities
------------
The tool automatically detects:

• Program dependencies
• Copybook usage
• DB2 tables and CRUD operations
• File reads and writes
• File flow architecture
• Program clusters for migration planning
• Business rules (IF, EVALUATE, WHEN)
• Field mappings (MOVE statements)
• GDG dataset usage
• VSAM detection

Requirements
------------
Python 3.9+

Install dependencies:

pip install pandas openpyxl networkx

Folder Structure
----------------
Place the script next to the Mainframe source folder:

project/
    discovery_tool.py
    Mainframe/
        CPY/
        CTC/
        DCL/
        JCL/
        PRC/
        SRD/

Run
---

python discovery_tool.py --scan

Output
------

Mainframe_Discovery_Report.xlsx

Sheets Generated
----------------

Program_Dependencies
Copybooks
DB2_CRUD
File_Reads
File_Writes
File_Flow
Program_Clusters
Business_Rules
Field_Mappings
GDG_Usage
VSAM_Detection

Use Case
--------
This discovery output is typically used to:

• Build program dependency diagrams
• Understand batch job architecture
• Identify external dependencies
• Extract business rules
• Plan mainframe to Java migration

