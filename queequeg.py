import string
import time
import sys
from iexfinance.stocks import Stock
from iexfinance.refdata import get_symbols


def format_dict(d):
    last = len(d) - 1
    s = ''
    s += '_{'

    for i, (k, v) in enumerate(d.items()):
        if v is None:
            s += "{}: '{}'".format(format_kv(k), None)
        elif type(v) is dict:
            s += '{}: {}'.format(format_kv(k), format_dict(v))
        else:
            s += '{}: {}'.format(format_kv(k), format_kv(v))

        if i < last:
            s += ', '

    s += '}'

    return s


def format_kv(x):
    if type(x) is str:
        return "'{}'".format(x.replace('\'', '\'\''))

    return str(x)


def get_stock_info(ticker):
    retries, retry_limit = 0, 25

    while retries <= retry_limit:
        try:
            stock = Stock(ticker)
            peers = set(stock.get_peers())
            advanced_stats = stock.get_advanced_stats()
            company = stock.get_company()

            return peers, advanced_stats, company
        except:
            retries += 1
            error_type, value, _traceback = sys.exc_info()
            print('Access Error - type: {}, value: {}'.format(error_type, value))
            time.sleep(10.0)

    print('Number of retries exceeded ({})'.format(retry_limit))
    sys.exit(1)


def main():
    tickers, valid_ticker_chars = set([]), set(string.ascii_uppercase + '.')

    for entry in get_symbols():
        if entry['type'] in ['cs', 'ps', 'ad'] and set(entry['symbol']) <= valid_ticker_chars:
            tickers.add(entry['symbol'])

    with open('equities.lgt', mode='w') as stocks_db:
        for ticker in tickers:
            peers, advanced_stats, company = get_stock_info(ticker)

            if set(ticker) <= valid_ticker_chars:
                stocks_db.write("stock('{}', {}, {}, {}).\n".format(ticker, format_dict(company), list(peers), format_dict(advanced_stats)))


if __name__ == '__main__':
    main()
