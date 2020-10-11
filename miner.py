import string
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
        s = "'{}'".format(x)
        return s.replace('\'', '\'\'')

    return str(x)


def main():
    tickers, valid_ticker_chars = set([]), set(string.ascii_uppercase + '.')

    for entry in get_symbols():
        if entry['type'] == 'cs' and set(entry['symbol']) <= valid_ticker_chars:
            tickers.add(entry['symbol'])

    with open('equities.lgt', mode='w') as stocks_db:
        for ticker in tickers:
            stock = Stock(ticker)
            peers, advanced_stats, company = set(stock.get_peers()), stock.get_advanced_stats(), stock.get_company()
            if set(ticker) <= valid_ticker_chars:
                stocks_db.write("stock('{}', {}, {}, {}).\n".format(ticker, format_dict(company), list(peers), format_dict(advanced_stats)))


if __name__ == '__main__':
    main()
