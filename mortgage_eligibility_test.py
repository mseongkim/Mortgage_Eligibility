# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 01:01:45 2015
@author: Min Seong Kim 
"""

import pandas as pd
import numpy as np
import pandas.io.data

file = 'mortgage_sample_data.xlsx'
data = pd.read_excel(file, sheetname='Sheet1')
LoanNo = data['Loan #']
LTV = data['LTV']
Balance = data['Current Balance']
FICO = data['FICO']
DTI = data['DTI']
Occupancy = data['Occupancy']
Purpose = data['Purpose']
list=['a','b','c','d']


def logictest1(programNo):
    Tier1_a=[]
    if programNo == 1:
        for i in range(len(Balance)):
            Tier1_a.append(np.logical_and(np.logical_or(Occupancy[i] == 'Primary Residence', Occupancy[i] == 'Secondary Residence'),\
                       np.logical_or(Purpose[i] == 'Purchase', Purpose[i] =='Rate/Term')))
        return Tier1_a

def logictest2(programNo):
    Tier1_b=[]
    if programNo == 1:
        for i in range(len(Balance)):
            Tier1_b.append(np.logical_and(np.logical_or(Occupancy[i] == 'Primary Residence', Occupancy[i] == 'Secondary Residence'),\
                       Purpose[i] == 'Cash-out'))
        return Tier1_b

# program No
# Example..
# Bank Statement = 1
# Non_Prime Program = 2

def InitCondition(programNo):
    if  programNo == 1:
        InitCondition = 100000
        return InitCondition
    elif programNo == 2:
        InitCondition = 200000
        return InitCondition
    else:
        InitCondition = 0
        return InitCondition


def Tier_Condi(programNo,list):
    if programNo == 1 and list == 'a':
       #Purpose == 'Purchase' or 'Rate/Term':
            Tier_Condi = pd.DataFrame({'LTV': [80,75,70,65,60],
                                       'Amount': [750000,1000000,1000000,1000000,1000000],
                                       'FICO':[700,680,660,640,620],
                                       'DTI':[43,43,43,43,43]}, index=range(0,5))
            return Tier_Condi
            
    elif programNo == 1 and list == 'b':
            Tier_Condi = pd.DataFrame({'LTV': [75,70,65,60],
                                       'Amount': [750000,1000000,1000000,1000000],
                                       'FICO':[700,680,660,640],
                                       'DTI':[43,43,43,43]}, index=range(0,4))
            return Tier_Condi

    elif programNo == 1 and list == 'c':
            Tier_Condi = pd.DataFrame({'LTV': [70,65,60],
                                       'Amount': [500000,750000,750000],
                                       'FICO':[700,680,660],
                                       'DTI':[43,43,43]}, index=range(0,3))
            return Tier_Condi

    elif programNo == 1 and list == 'd':
            Tier_Condi = pd.DataFrame({'LTV': [65,60],
                                       'Amount': [500000,750000],
                                       'FICO':[700,680],
                                       'DTI':[43,43]}, index=range(0,2))
            return Tier_Condi
    else:
        return 0.0

        
def remove_duplicates(retData):
    retData_rm=[]
    
    if programNo == 1:
        for i in retData:
            if i not in retData_rm:
                retData_rm.append(i)
    return (retData_rm)
        

class Matrix:

    def __init__(self,programNo):
        self.programNo = programNo
        return

    def testEligibility(self):

        retData1 = []; retData1_rm = []
        retData2 = []; retData2_rm = []
        retData3 = []; retData3_rm = []
        retData4 = []; retData4_rm = []

        if self.programNo == 1 : 
           for i in range(len(Balance)):
               if Balance[i] >= InitCondition(self.programNo): 
                  if logictest1(self.programNo)[i] == True:
                      for x in range (0,5):
                            if LTV[i] <= Tier_Condi(self.programNo,'a')['LTV'][x] and \
                               Balance[i] <= Tier_Condi(self.programNo,'a')['Amount'][x] and \
                               FICO[i] >= Tier_Condi(self.programNo,'a')['FICO'][x] and \
                               DTI[i] <= Tier_Condi(self.programNo,'a')['DTI'][x] :
                                 retData1.append(LoanNo[i])

                      for y in range (0,3):
                            if LTV[i] <= Tier_Condi(self.programNo,'c')['LTV'][y] and \
                               Balance[i] <= Tier_Condi(self.programNo,'c')['Amount'][y] and \
                               FICO[i] >= Tier_Condi(self.programNo,'c')['FICO'][y] and \
                               DTI[i] <= Tier_Condi(self.programNo,'c')['DTI'][y] :
                                 retData3.append(LoanNo[i])

                  elif logictest2(self.programNo)[i] == True:
                       for x in range (0,4):
                            if LTV[i] <= Tier_Condi(self.programNo,'b')['LTV'][x] and \
                               Balance[i] <= Tier_Condi(self.programNo,'b')['Amount'][x] and \
                               FICO[i] >= Tier_Condi(self.programNo,'b')['FICO'][x] and \
                               DTI[i] <= Tier_Condi(self.programNo,'b')['DTI'][x] :
                                retData2.append(LoanNo[i])

                       for y in range (0,2):
                            if LTV[i] <= Tier_Condi(self.programNo,'d')['LTV'][y] and \
                               Balance[i] <= Tier_Condi(self.programNo,'d')['Amount'][y] and \
                               FICO[i] >= Tier_Condi(self.programNo,'d')['FICO'][y] and \
                               DTI[i] <= Tier_Condi(self.programNo,'d')['DTI'][y] :
                                retData4.append(LoanNo[i])
                  else:
                        print('Not eligible loan number is '+ str(LoanNo[i]))
                        
        else:
            print "Program number %d is not valid yet." % self.programNo
        
        retData1_rm = remove_duplicates(retData1)
        retData2_rm = remove_duplicates(retData2)
        retData3_rm = remove_duplicates(retData3)
        retData4_rm = remove_duplicates(retData4)
        
        return (retData1_rm,retData2_rm,retData3_rm,retData4_rm)

#choose mortgage loan program
programNo = 1
T = Matrix(programNo)
T.testEligibility()
