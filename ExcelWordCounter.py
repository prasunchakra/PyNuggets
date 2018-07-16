from openpyxl import load_workbook

def count(inputxlsx,inputsheet,inputcolumn,outputcolumn):
    inputcolumn+='{}'
    iwbook = load_workbook(filename = inputxlsx)
    iwsheet = iwbook[inputsheet]
    irow = 1
    while(True):
        irow+=1
        Story = str(iwsheet[inputcolumn.format(irow)].value)
        if Story == 'None':
            break
        #print "Processing Row",irow        
        count = len(Story.split())
        cell = outputcolumn + str(irow)
        iwsheet[cell] = count
    iwbook.save(inputxlsx)
        

if __name__ == '__main__':
    inputxlsx = 'YellowPages.xlsx'
    sheet = 'Sheet1'
    inputcolumn = 'A'
    outputcolumn = 'B'    
    count(inputxlsx,sheet,inputcolumn,outputcolumn)
