#%%
"""
First of all several functions are defined to create the samples (Latin Hypercube Sampling)
and the connection HYSYS-python (UnisimConnection(object)).
Then, samples are randomly generated and ordered, so HYSYS feasibility is improved.
Finally, the connection is created and samples are simulated. The results are eventually
exported to an Excel file through a pandas DataFrame.
"""

#%% Defini the Latin Hypercube Sampling functions
import numpy as np
import matplotlib.pyplot as plt
import array


def latin_hypercube_normalized(d,n):
  "Normalized values from 0-1"
  lower_limits = np.arange(0,n)/n
  upper_limits = np.arange(1,n+1)/n      

  points = np.random.uniform(low=lower_limits, high=upper_limits, size=[d,n]).T
   
  for i in range(0,d):
    np.random.shuffle(points[:,i])
  return points


def latin_hypercube_sampling(LOW,UP,p,d):
  "Values from upper to lower limits"
  for i in range(0,d):
    p[:,i]=p[:,i]*(UP[i]-LOW[i])+LOW[i]
  return p

#%% Pip install
#pip install cognite-sdk
#%% Imports
import numpy as np
import pandas as pd
import win32com.client
import os
import time
import datetime as dt
from datetime import datetime
from datetime import timedelta 
from cognite.client import CogniteClient
from pathlib import Path
from win32com.client import makepy 
import matplotlib.pyplot as plt
import sys
class UnisimConnection(object):
    ''' All the functions related to Unisim communication '''
    #Open Unisim Case
    def __init__(self,filepath,unisimpath):
        '''
        Set all the global variables and do the convertion for C classes to Python language.
        The CLSID may be wrong because this script was written for Unisim in case is wrong we can look for the good ones
        '''
        try:
            self.casepath = filepath
            self.uniapp = win32com.client.Dispatch("HYSYS.Application.NewInstance")
            self.simcase = self.uniapp.SimulationCases.Open(filepath)
            ## Call to Unisim backdor class on the register
            self.BackDoor=makepy.gencache.GetClassForCLSID("{11FE7386-A1D1-4E47-B46A-8A09A7CE5EB2}")
            # Define class for FixedDataTables, Datatalbe and VarDefinition lybraries
            self.FixedDataTables = makepy.gencache.GetClassForCLSID("{4DEF63F0-103B-11D1-A455-00A0C923285C}")
            self.DataTable = makepy.gencache.GetClassForCLSID("{FE57ADBD-5DFA-46DA-B205-423FBF3799AA}")
            self.VarDefinition = makepy.gencache.GetClassForCLSID("{B37CCBF0-E29E-11D0-A418-00A0C923285C}")
            sys.argv = ["makepy", unisimpath]
            makepy.main ()
            return
        except:
            assert self.simcase is not None, "Hysys Case is null"
            UnisimConnection.KillUnisim(self.simcase)

    def OpenCase(self):
        ''' Open Hysys case & Activate the select case '''
        self.uniapp.Visible = False
        self.simcase.Activate()
        return [self.simcase,self.uniapp]

    def KillUnisim(self,simCase = ''):
        ''' Kill Hysys at the end of the run or when somethin goes wrong '''
        if self.simcase != '': 
            self.simcase.Close(False)
        return self.uniapp.Quit()   
                    
    def ReadDataTable(self,TableName):
        ''' Read Information from Process data table and convert it to a python dictionary'''
        # Look for the Process Data Table of the Unisim case
        DataTables = self.FixedDataTables(self.simcase.DataTables)
        ProcessDataTable = self.DataTable(DataTables.Item(TableName))
        ProcessDataTable.StartTransfer()
        vd = ProcessDataTable.GetAllVarDefinitions()    #Això hauria de ser un diccionari, no?        
        # Extract all Tags info and save it into a dict
        DataTable = {}
        idict = {}
        Values = []
        for x,value in enumerate(vd):
            vd = self.VarDefinition(value)  #Aquests son els values del diccionari final
            idict[vd.Tag] = vd              #Dins del GetValue es podrien especificar les unitats en que volem que ho llegeixi.
            Values.append(vd.Variable.GetValue())
        ProcessDataTable.EndTransfer()  
        DataTable[TableName] = idict
        return DataTable, Values

    def WriteTagsDataTable(self, TableDict,Values,dataTableName):
        '''Write all tags to selected process data table'''
        #try:
            #ProcessDataTable.StartTransfer()
            # Write all the values back to the ProcessDataTable 
        DataTables = self.FixedDataTables(self.simcase.DataTables)
        ProcessDataTable = self.DataTable(DataTables.Item(dataTableName))
        ProcessDataTable.StartTransfer()
        getvalues = ProcessDataTable.GetAllValues()
        #print('Inputs: ',type(getvalues))
        #print(type(tuple(Values)))
        for iDataTable in TableDict:
            tempDict = TableDict[iDataTable]
            dictindex = 0
            for Tag in tempDict.values():
                vd = self.VarDefinition(Tag)    
                if (vd.accessMode == 3 or vd.accessMode == 2):                  #Write and Write/Read
                    if not(np.isnan(Values[dictindex])):
                        vd.Variable.SetValue(Values[dictindex], vd.Units) 
                dictindex +=1
        ProcessDataTable.EndTransfer()
        #except:
            #print("Error writing tags")
    def Run(self): 
        ''' Runs the Unisim simulation from a script previously defined'''
        # References to BackDoor Variables
        #PropPkgBd = self.BackDoor(self.simcase)
        #PropPkgBd.SendBackDoorMessage('"FlowSht.1/UnitOpObject.400(A-BCD)/FlowSht.600" "Run"')
        self.uniapp.PlayScript(r'G:\arnau\RunColumnPython.scp')
        'This sleep is jut to let the optimizer calculate, it can be checked also with a While loop'
        #time.sleep(5) 
        return True

    def Calculate(self): 
        ''' Call to Unisim optimizer '''
        # References to BackDoor Variables
        PropPkgBd = self.BackDoor(self.simcase)
        PropPkgBd.SendBackDoorMessage('Optimizer.300:Execute')
        'This sleep is jut to let the optimizer calculate, it can be checked also with a While loop'
        time.sleep(7) 
        return True

"""
    def WriteSingleTag(self,TableDict,Tag,Value):
        '''Write a single tag to process datatable'''
        # Write all the values back to the ProcessDataTable 
        #ProcessDataTable.StartTransfer()
        for iDataTable in TableDict:
            tempDict = TableDict[iDataTable]
            if Tag in tempDict:
                vd = self.VarDefinition(tempDict[Tag])
                if vd.accessMode == 3 or vd.accessMode == 2:
                    vd.Variable.SetValue(Value, vd.Units)    
        #ProcessDataTable.EndTransfer()
    
def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = [value , dict1[key]]
   return dict3
""" 

#%% Create the sampling points.
#Define the upper and lower intervals for each variable. Remember that each position "i" in vectors LOW and UP matches each variable "i" in array p.
#Model 1
Inputs = ['NT', 'RR', 'Distillate_Rate']
UP  = [20, 3 , 6150]
LOW = [5, 0.3,5000]

"""
#MODEL 2
Inputs = ['NT','A_Flow_Propene', 'BCD_Flow_Ethylene']
UP  = [40, 8.3397, 21.8991]
LOW = [10, 0.0834, 0.2190 ]
"""


n = 10000     #Number of samples that are required
d = len(UP)   #Number of inputs that are required

#The array "p" is normalized between 0-1.
p = latin_hypercube_normalized(d,n)

#The array "q" is not normalized. These are the sampling points. 
q = latin_hypercube_sampling(LOW,UP,p,d)
q[:,0]=q[:,0].astype(int)                           #Always keep the first input as NT (number of trays), as it must be a natural number (int).
#q[:,1:]=np.around(q[:,1:],4)                         # We want the other variables to have 4 decimals, as this is the length in HYSYS variables.
#q=np.around(q,4)                                     # We want all the other variables to have 4 decimals, as this is the length in HYSYS variables.
#%% Plot the sampling points to check everything is random
x=2
y=1

#Figure
plt.figure(figsize=[10,10])
plt.xlim([LOW[x],UP[x]])
plt.ylim([LOW[y],UP[y]])
plt.xlabel(Inputs[x])
plt.ylabel(Inputs[y])
plt.scatter(q[:,x], q[:,y], c='r', s=10)

#Create the grid so the position of the points is the one desired (just one point per column and row).
for i in np.arange(LOW[x], UP[x], 1/n*(UP[x]-LOW[x])):
  plt.axvline(i, linewidth=0.01)
for i in np.arange(LOW[y], UP[y], 1/n*(UP[y]-LOW[y])):
  plt.axhline(i, linewidth=0.01)

plt.show()

#%%
q= sorted(sorted(sorted(q,key=lambda x: x[1]),key=lambda x: -x[2]),key=lambda x: -x[0])   #Though the sample is random, the points are ordenated to reduce HYSYS hysteresis
#sorted(q, key=lambda x: -x[0])
#q
#%% Sample the data points

filepath   =r'G:\arnau\Simulations\Column_A-BCD.hsc'  # Ubicació de la simulació a mapejar
unisimpath =r'C:\Program Files\AspenTech\Aspen HYSYS V11.0\hysys.tlb'  # Ubicació de la instal·lació de HYSYS 

obj = UnisimConnection(filepath,unisimpath)
obj.OpenCase()
#%%
TableDict, Values = obj.ReadDataTable('ProcData3')
#%%
from datetime import datetime
start_time = datetime.now()

Results = []
Counter = 0
for x in q:
    obj.WriteTagsDataTable(TableDict,x,'ProcData3')     #El tamany de q ha de ser igual als Write i Read/Writes del DataTable
    obj.Run()
    #obj.Calculate()
    #obj.Run()
    Result, Values = obj.ReadDataTable('ProcData3')
    Results.append(Values)
    Counter = Counter + 1
    print(Counter)
end_time = datetime.now()
#%% Proves
import csv 
  
# field names  
fields = list(Result[list(Result.keys())[0]].keys())
   
# data rows of csv file  
rows = Results

with open('Model', 'w') as f: 
    # using csv.writer method from CSV package 
    write = csv.writer(f) 
    write.writerow(fields) 
    write.writerows(rows) 

Data_Model  = Results

#%% Proves    
#print('Results: ', Results)

print('Time:0', end_time-start_time)

#%% 
#Results

"""
Tenir present que en la lectura de dades les variables temporales passen de h a sec (exemple: duties en kJ/s i flows en kmols/s)
"""

tags = list(Result[list(Result.keys())[0]].keys())
Results=pd.DataFrame(Results)
Results.columns = tags
#o = win32com.client.Dispatch("Excel.Application")
#o.Visible = 1   
Results.to_excel(r'G:\arnau\Sampling\Book1.xlsx')
