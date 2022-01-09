import string
import time
import sys
import ast
from iexfinance.stocks import Stock
from iexfinance.refdata import get_symbols

# growth screening variant

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
        s = "'{}'".format(x.replace('\'', '\'\''))
        s = s.replace('\\', '\\\\')
        return s

    return str(x)


def get_stock_info(tickers):
    retries, retry_limit = 0, 25

    while retries <= retry_limit:
        try:
            stock = Stock(list(tickers))

            return stock.get_income_statement(period='annual', last=5)
        except:
            retries += 1
            error_type, value, _traceback = sys.exc_info()
            print('Access Error - type: {}, value: {}'.format(error_type, value))
            time.sleep(10.0)

    print('Number of retries exceeded ({})'.format(retry_limit))
    sys.exit(1)


def main():
    tickers, valid_ticker_chars = [], set(string.ascii_uppercase + '.')

    for entry in get_symbols():
        if entry['type'] in ['cs', 'ps', 'ad'] and set(entry['symbol']) <= valid_ticker_chars:
            tickers.append(entry['symbol'])

    length, i = len(tickers), 100
    groups = list(filter(lambda x: x != [], [tickers[i - 100:i] for i in range(i, length + i, i)]))

    with open('equities.lgt', mode='w', newline='', encoding='utf-8') as stocks_db:
        for group in groups:
            statements = get_stock_info(group)

            for ticker in group:
                ss = statements[ticker]
                length = len(ss)
                if set(ticker) <= valid_ticker_chars:
                    stocks_db.write("stock('{}', [".format(ticker))
                    for i, d in enumerate(ss):
                        if i < length - 1:
                            stocks_db.write('{}, '.format(format_dict(d)))
                        else:
                            stocks_db.write('{}'.format(format_dict(d)))
                    stocks_db.write("]).\n")


if __name__ == '__main__':
    main()
