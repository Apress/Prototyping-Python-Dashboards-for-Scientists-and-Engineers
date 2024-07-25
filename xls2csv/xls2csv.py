# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 22:52:20 2021

@author: pjhmx
"""

import re

############################################################################
#
# Convert a downloaded ATADS file from xls format to CSV
#
# Non-data blocks are skipped, then the data rows are processed 
#
# Unwanted commas are removed, and an unwanted space removed so
# airport 3 letter ids are recovered
#
# Data read in from local directory ATADS_XLS
#
# Data saved to ATADS_CSV - must exist!
#
############################################################################


class my_xls2csv:
    def __init__(self):
        self.f_xls          = ''
        self.f_csv          = ''
        self.in_data_table  = False
        self.year_list      = [*range(2020,2024,1)]
        self.year           = 2006
        self.res            = ''
        



    
    ############################################################################
    #
    # Skip from top to the end of the thead block
    #
    
    def skip_through_end_of_thead_block(self):
        while (True):
            line = self.f_xls.readline()
            if '/thead>' in line:
                break
            
        print("leading headers skipped")
        return

    ############################################################################
    #
    # Process a row of the XL table which is multi-line of the form
    #
    # <tr>
    # <td> </td>
    # ...
    # </tr>
    #
    # Clean data by removing unwanted commas and fixing Airport ID field
    # by removing extra space  ('ABC ' -> 'ABC')
    #
    # and by erasing <*> entries
    #
    
    def read_XL_row(self):
        do_read = True
        str0 = ''
        while (do_read):
            line = self.f_xls.readline()
            line = line.strip()
            if 'table_footer_lead' in line:             # End of data table
                self.in_data_table=False
                
            elif "<tr" in line: 				        # XL row start
                str0 = ""
                
            elif "<td " in line:      			        # cell start
                line0 = re.sub(',','',line) 		    # remove commas
    
    							                        # change'ABC ' to 'ABC'
                line1 = re.sub(r'([A-Z]{3})([ ])',r'\1', line0, count=1) 
                
                                                        #remove <> tags
                str0   = str0 + ',' + re.sub('<.*?>','',line1)  
    
            elif "</tr" in line: 				        # End of XL row found
                do_read = False

        
        self.row_str = str0[1:]+'\n'                 # also cleanup leading ','





    ############################################################################
    #
    # Convert one year of ATADS xls data
    #
    
    def do_atads_year(self):
       
        print ('Doing year: ',str(self.year))
        self.xls_file = 'ATADS_XLS/atads' + str(self.year) + '.xls'
        self.csv_file = 'ATADS_CSV/atads' + str(self.year) + '.csv'
        
        print ("Converting ", self.xls_file, " to ", self.csv_file)
        
        self.f_xls = open(self.xls_file,'r')
        self.f_csv = open(self.csv_file,'a')
        
        self.skip_through_end_of_thead_block()
        
        print("reading data table...\n")
        self.in_data_table=True					# Table Start
        
        while self.in_data_table:
            self.read_XL_row()
            
            if self.in_data_table:
                self.f_csv.write(self.row_str)
            else:
                break
            
        self.f_csv.close()
        self.f_xls.close()




x2c = my_xls2csv()

for year in x2c.year_list:
    x2c.year = year

    x2c.do_atads_year()  
