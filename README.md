# Boder Crossing Analysis

### Coding challenge (https://github.com/InsightDataScience/border-crossing-analysis)
python3 by W. Zha@08/20/2019.

## Requires libraries/dependencies
- import csv
- import sys
- from datetime import datetime

## Function call 
The solution border_analytics.py takes two inputs: 1)input_file and 2) output_file. For instance, 

python3.7 ./src/border_analytics.py ./input/Border_Crossing_Entry_Data.csv ./output/report.csv

## Strategy
### Read the input *.csv: read_border_csv_file()
The list border_data=[dict()] of size n_record-by-4 was created and filled after reading the input .csv file per line. n_record is the total number of rows in the input file and each row of border_data is a dictionary (i.e., {'Border':US-Mexico Border,'Date':'03/01/2019 12:00:00 AM','Measure':'Pedestrians','Value':'346158'} with len=4.

### Get the monthly sum: parse_raw_border_sheet()
- Two dictionaries unique_records and unique_border_measures were created prior to looping over the list "border_data" which was loaded from the input .csv. The "unique_records" keeps track of unique combination of Border, Measure and Date and the corresponding row index in the list "report", whereas "unique_border_measures" keeps track of unique combination of Border and Measure and recording the corresponding Date and Value as a list of tuple (Date, Value).

- Similar to border_ata, a new list "report = [{'Border':xxx,'Date':xxx,'Measure':xxx,'Value':xxx,'Average':0}]" was initialized with the dictionary items designed according to the output requirements.

- Loop over each row of "border_data", and
  1) append a new row to the list "report" if it is unseen in unique_records; otherwise only update (add) the 'Value' of the row that yielded the same Border, Measure and Date;
  2) append a tuple (Date, Value) for each combination of Border and Measure
  
- According to the output rule that "The lines should be sorted in descending order by Date, Value (or number of crossings), Measure
Border", the list "report" was sorted using lambda functions.
 
- Lastly, loop over each row of the list "report" and calculate the running monthly average as required.

### Write the output *.csv: write_report_csv_file()
The output report.csv file is written in a row-by-row or line-by-line fashion using csv.DictWriter.

