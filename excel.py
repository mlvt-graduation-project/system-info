import xlsxwriter

def export_excel(listColumn, listRow, fileName):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(fileName)
    worksheet = workbook.add_worksheet()
    
    # Assuming listColumn is a list of column headers and listRow is the data.
    # Write the headers first
    for col_num, header in enumerate(listColumn.split(', ')):  # Split string into list of column names
        worksheet.write(0, col_num, header.strip())  # Write each header to the first row
    
    # Write the data
    for row_num, row in enumerate(listRow, 1):  # Start from row 1 to avoid the header
        for col_num, item in enumerate(row):
            worksheet.write(row_num, col_num, item)  # Write each item to the worksheet

    # Close the workbook
    workbook.close()

# Call the function with proper column headers and data
export_excel('colA, colB, colC', [['Hello',2,3], [4,5,6], [7,8,9]], 'excel.xlsx')
