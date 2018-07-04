from openpyxl import load_workbook
import pandas as pd
import collections, itertools

#Input Variables
inputxlsx = 'Test1.xlsx'
outputcsv = 'Test.csv'
inputsheet = 'Sheet1'
outputsheet = 'Sheet1'
ColHeadline = 'D{}'
ColStory = 'E{}'


iwbook = load_workbook(filename = inputxlsx)
iwsheet = iwbook[inputsheet]
listfreqarray = []
listheadlines = []
irow = 1
print ("Taking input from ",inputxlsx)
while(True):
    irow+=1
    Headline = str(iwsheet[ColHeadline.format(irow)].value)
    Story = str(iwsheet[ColStory.format(irow)].value)
    if Headline == 'None':
        break
    wordlist = Story.split()
    wordfreq = [wordlist.count(w) for w in wordlist]
    freqarray = dict(zip(wordlist, wordfreq))
    listheadlines.append(Headline)
    listfreqarray.append(freqarray)
print ("Calculating individual frequency")
MasterFrequencyArray = dict(pair for d in listfreqarray for pair in d.items())
MasterFrequencyArraySkeleton = collections.OrderedDict(zip(MasterFrequencyArray, itertools.repeat(0)))
vwords = MasterFrequencyArraySkeleton.keys()
icol = 1
index = 0
irow -=1
MasterFrequencyArraySkeleton = {}
print ("Creating The Frequency Matrix")
while (icol<irow):
    icol+=1
    MasterFrequencyArray = []
    for key in vwords:
        MasterFrequencyArray.append(listfreqarray[index].get(key,0))
    MasterFrequencyArraySkeleton.update({listheadlines[index]:MasterFrequencyArray})
    index += 1
print ("Writing to",outputcsv)
df = pd.DataFrame(MasterFrequencyArraySkeleton, index = vwords,columns = listheadlines)
df.to_csv(outputcsv,index_label='Words/Headlines')
print ("Successfully Completed ")
