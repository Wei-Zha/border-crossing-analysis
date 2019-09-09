# -*- coding: utf-8 -*-
"""
info source: https://github.com/InsightDataScience/border-crossing-analysis
Problem
The Bureau of Transportation Statistics regularly makes available data on the number of vehicles, 
equipment, passengers and pedestrians crossing into the United States by land.

For this challenge, we want to you to calculate the total number of times vehicles, equipment, 
passengers and pedestrians cross the U.S.-Canadian and U.S.-Mexican borders each month. We also 
want to know the running monthly average of total number of crossings for that type of crossing 
and border.

Input Dataset
For this challenge, you will be given an input file, Border_Crossing_Entry_Data.csv, that will
reside in the top-most input directory of your repository.
    -Border: Designates what border was crossed
    -Date: Timestamp indicating month and year of crossing
    -Measure: Indicates means, or type, of crossing being measured (e.g., vehicle, equipment, 
              passenger or pedestrian)
    -Value: Number of crossings

Expected Output:
Using the input file, you must write a program to

Sum the total number of crossings (Value) of each type of vehicle or equipment, or passengers 
or pedestrians, that crossed the border that month, regardless of what port was used.
Calculate the running monthly average of total crossings, rounded to the nearest whole number, 
for that combination of Border and Measure, or means of crossing.    

For example,
    Border,Date,Measure,Value,Average
    US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,114487
    US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,0
    US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,0
    US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,172163,56810
    US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,0
    US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,0
    
W. Zha coded @ 08/20/2019    
"""

import csv, sys
from datetime import datetime as dt
#%%
def read_border_csv_file(input_file,field_indices):
    # Read the input *.csv into a n_record-by-4 2D list 
    # Desired input variables: Border, Date, Measure, Value
    #input_file = '../input/Border_Crossing_Entry_Data.csv'
#        input_file = "../insight_testsuite/tests/test_1/input/border-crossing-analysis.csv"
        with open(input_file) as border_csv:
        
            readCSV = csv.reader(border_csv, delimiter=',')
        
            #    
            border_data, n_record = [],0
            
            for row_entry in readCSV:
                
                
                if n_record>0:  
                    
                    this_row = dict()
                    for field,idx in field_indices.items():
                        
                        this_field_value = row_entry[idx]
                        this_row[field] = this_field_value
        
                    border_data.append(this_row)                   
#                    print('read in line ' +str(n_record)+'...\t')
                n_record +=1
        border_csv.close()
        
        return border_data
    
    
    # Write report.csv    
def write_report_csv_file(output_file,report):
    
    with open(output_file, mode='w', newline='') as report_file:
        fieldnames = list(report[0].keys())
        writer = csv.DictWriter(report_file,fieldnames=fieldnames)
        writer.writeheader()
        
        for _,entry in enumerate(report):
            writer.writerow(entry)
    
    report_file.close()   
    print('\n'+output_file+' is written.\n')
            
#%%
# Loop over raw border_data and create the list report with the desired output 
# variables: Border, Date, Measure, Value, Average
def parse_raw_border_sheet(border_data, input_date_format):

    desired_date_format = '%m/%d/%Y %I:%M:%S %p'
       
    report=[]
    unique_records = dict()
    unique_border_measures = dict()
       
    for entry in border_data:
        border_measure = entry['Border'] + ',' + entry['Measure']
        unique_record_string = border_measure + ',' + entry['Date']
        
        datetime_object = dt.strptime(entry['Date'], input_date_format)
        
        # 1) Accumulate the sum of the crossing values per boder, measure and date  
        this_output = dict()
        if unique_record_string not in unique_records.keys():
            unique_records[unique_record_string]=len(report)
            
            this_output['Border'] = entry['Border']
            this_output['Date'] = datetime_object.strftime(desired_date_format)
            this_output['Measure'] = entry['Measure']
            this_output['Value'] = this_output.get('Value',0) + int(entry['Value'])
            this_output['Average']=0
            report.append(this_output)
            
        else:
            record_index = unique_records[unique_record_string]
            report[record_index]['Value'] += int(entry['Value'])
            
           
#        print(border_measure)
        
        # 2) Use a dictionary to record the tuple (date,value) per border and measure
        if border_measure not in unique_border_measures:
            unique_border_measures[border_measure] = []            
          
        unique_border_measures[border_measure].append((dt.strptime(entry['Date'], input_date_format), int(entry['Value'])))
                
        
    """ 
       Sort the output row entries according to the required order:
       "The lines should be sorted in descending order by

        -Date
        -Value (or number of crossings)
        -Measure
        -Border"
    """
   
    report.sort(key=lambda x:x['Border'], reverse = True)
    report.sort(key=lambda x:x['Measure'],reverse = True)
    report.sort(key=lambda x:x['Value'],reverse = True)
    report.sort(key=lambda x:dt.strptime(x['Date'], desired_date_format),reverse = True)            
    
        
   # Loop over report to calcualte running monthly average
    for index, entry in enumerate(report):
        border_measure = entry['Border']+','+entry['Measure']
        current_date = dt.strptime(entry['Date'], desired_date_format)
    
    
        date_value = unique_border_measures[border_measure]
        previous_values = [value for datestr,value in date_value if datestr<current_date]
    
        # Get all previous months per border and measure. Use set() to eliminate duplicate month entries.
        previous_months = set([datestr for datestr,_ in date_value if datestr<current_date])
        
        if previous_months:
            
            # Added the bias of 0.2 to ensure rounding up to the next integer when resulting in xxx.5
            report[index]['Average'] = round(sum(previous_values)/len(previous_months)+0.2)         
    return report,unique_border_measures


#%%  
def border_analytics(input_file,output_file):
    
   
   field_indices = {'Border':3, 'Date':4, 'Measure':5, 'Value':6}
   border_data = read_border_csv_file(input_file,field_indices)
    
   # Accommodate two different date time format
   input_date_format = '%m/%d/%Y %H:%M' 
   desired_date_format = '%m/%d/%Y %I:%M:%S %p'
   while True:
       try:
           dt.strptime(border_data[0]['Date'], input_date_format)
           break
       except ValueError:
           input_date_format = desired_date_format
   
    
   report,unique_border_measures = parse_raw_border_sheet(border_data, input_date_format)
    

    # Get output_file path based on input_file 
#        output_file = input_file[::-1]
#        output = output_file.replace('/tupni/','/tuptuo/',1)[::-1]        
#        phrases = output.split('/')
#        phrases[-1] = 'output.csv'
#        output = '/'.join(phrases)
   write_report_csv_file(output_file,report)


#%%
if __name__ == '__main__':
    if len(sys.argv)<2:
        print("Function usaage: python border_analytics.py ../input/border_crossing.csv ../output/report.csv")
        exit 
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print('input file is ', input_file +'\n')
    print('output file is ', output_file + '\n')

    border_analytics(input_file,output_file)
    
