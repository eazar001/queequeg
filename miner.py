import csv
import time
from iexfinance.stocks import Stock


def main():
    tickers = []

    with open('crsp_large_cap_value.csv', newline='') as equities_file:
        reader = csv.reader(equities_file)

        for row in reader:
            tickers.append(row[0])

    with open('stocks.pl', mode='w') as stocks_db:
        for ticker in tickers:
            stock = Stock(ticker)
            peers, advanced_stats = stock.get_peers(), stock.get_advanced_stats()
            stocks_db.write("stock('{}', {}, {}).\n".format(ticker, peers, advanced_stats))
            time.sleep(0.5)


if __name__ == '__main__':
    main()
