import openpyxl
from openpyxl.styles import Alignment
from openpyxl.worksheet.properties import PageSetupProperties
F='5.2026_CompiledInvoices.xlsx'
wb=openpyxl.load_workbook(F); ws=wb['Sam_Daitzman']

# balanced widths tuned for landscape Letter, fit-to-1-page-wide
widths={'A':10,'B':8,'C':15,'D':20,'E':17,'F':12,'G':26,'H':7.5,'I':7.5}
for col,w in widths.items(): ws.column_dimensions[col].width=w

# ensure long-text columns wrap in the labor table so widths can stay modest
for r in range(13,26):
    for c in (3,4,5,7):
        cell=ws.cell(r,c); a=cell.alignment
        cell.alignment=Alignment(horizontal='left',vertical='top',wrap_text=True)

# page setup: landscape, fit to 1 page wide, center horizontally, slim margins
ws.page_setup.orientation='landscape'
ws.page_setup.fitToWidth=1
ws.page_setup.fitToHeight=0
ws.sheet_properties.pageSetUpPr=PageSetupProperties(fitToPage=True)
ws.print_options.horizontalCentered=True
pm=ws.page_margins
pm.left=pm.right=0.3; pm.top=pm.bottom=0.5; pm.header=pm.footer=0.2
ws.page_setup.paperSize=1  # Letter
wb.save(F)
print('print formatting applied; total width units =',sum(widths.values()))
