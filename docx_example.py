from docx import Document

document = Document('Sample_AWR.docx')

for table in document.tables:
    print table
    
