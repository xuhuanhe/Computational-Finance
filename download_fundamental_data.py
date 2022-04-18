'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : Xuhuan He

https://github.com/JECSand/yahoofinancials

'''

import pandas as pd
import csv
from utils import MyYahooFinancials

def download_fundamental_data(input_file_name, output_file_name):
    # reading csv file
    # initializing the titles and rows list

    fields = []
    rows_data = []
    freq = 'annual'
    
    with open(input_file_name, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
      
        # extracting field names through first row
        fields = next(csvreader)
        print("field:",fields)
    # extracting each data row one by one
        for row in csvreader:
            rows = []
            rows.append(row[0])
            rows.append(row[1])
            rows.append(row[2])
            yfinance = MyYahooFinancials (row[0])
            try:
                rows.append(yfinance.get_market_cap())
            except:
                rows.append("no data")
            try:
                rows.append(yfinance._financial_statement_data('balance',
                                                          'balanceSheetHistory',
                                                          'totalAssets',
                                                          freq))
            except:
                rows.append("no data")
                        
                   
            
            try:
                long_term_debt = (yfinance.get_long_term_debt())
                current_liabilities = (yfinance.get_total_current_liabilities())
                accounts_payables = (yfinance.get_account_payable())
                other_current_liabilities = (yfinance.get_other_current_liabilities())
                
                rows.append(long_term_debt + current_liabilities - accounts_payables - other_current_liabilities)
            except:
                rows.append("no data")
                
            '''
        get free cash flow as operating cashflow + capital expenditures (which will be negative)
            '''
            try:
                operating_cashflow = (yfinance.get_operating_cashflow())
                capital_expenditures = (yfinance.get_capital_expenditures())
                if(capital_expenditures < 0):
                    rows.append(operating_cashflow + capital_expenditures)
                else:
                    rows.append(operating_cashflow - capital_expenditures)
            except:
                rows.append("no data")
            try:
                rows.append(yfinance.get_beta())
            except:
                rows.append("no data")
            try:
                rows.append(yfinance.get_pe_ratio())
            except:
                rows.append("no data")
            
            rows_data.append(rows)
         
                
            
            
            
            
            print("rows:",rows)
            print("rows_data:",rows_data)
   
           
        
        
        
    # writing to csv file
    with open(output_file_name, 'w',newline="") as file:
    # creating a csv writer object
        csvwriter = csv.writer(file)
      
    # writing the fields
        csvwriter.writerow(fields)
        
      
    # writing the data rows
        csvwriter.writerows(rows_data)
        
def run():
    input_fname = "StockUniverse.csv"
    output_fname = "StockUniverseWithData.csv"
    
    download_fundamental_data(input_fname, output_fname)

    
if __name__ == "__main__":
    run()

