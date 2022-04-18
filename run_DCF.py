'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : Lin Shi

'''

import pandas as pd
import datetime

from stock import Stock
from discount_cf_model import DiscountedCashFlowModel

def run():
    input_fname = "StockUniverseWithData.csv"
    output_fname = "StockUniverseValuation.csv"

    as_of_date = datetime.date(2021, 6, 15)
    df = pd.read_csv(input_fname)
    
    # TODO
    results = []
    for index, row in df.iterrows():
        
        try:
            print('Calculating fair value for ' + row['Symbol'])
            stock = Stock(row['Symbol'], 'annual')
            model = DiscountedCashFlowModel(stock, as_of_date)

            short_term_growth_rate = float(row['EPS Next 5Y'])
            medium_term_growth_rate = short_term_growth_rate/2
            long_term_growth_rate = 0.04

            model.set_FCC_growth_rate(short_term_growth_rate, medium_term_growth_rate, long_term_growth_rate)
        
            fair_value = model.calc_fair_value()

            results.append(fair_value)
        except:
            results.append('no data')
    df['DCF'] = results    
    print("Generating StockUniverseValuation.csv")
    df.to_csv(output_fname, index = False)
    # end TODO

    
if __name__ == "__main__":
    run()
