import csv
import json
from dateutil import parser
import requests


def output_csv_of_dates_to_total_portfolio_value(initial_portfolio_size_in_dollars, include_cash_in_outputted_portfolio_value=True):
    coin_api_name_to_symbol = {'Bitcoin': 'BTC', 'Ethereum': "ETH", "BitcoinCash": "BCH", "Ripple": "XRP",
                               "Litecoin": "LTC", "IOTA": "MIOTA", "Dash": "DASH", "NEM": "XEM"}
    # coin_api_name_to_symbol = {key, value in coin_api_name_to_symbol if value in    }
    coin_symbols = set(coin_api_name_to_symbol.values())

    days_data = get_days_data(coin_api_name_to_symbol)
    sorted_dates_as_strings = sorted(list(set([entry['date'] for entry in days_data])))  # Ex: ['1503633600', ...]
    first_day = sorted_dates_as_strings[0]  # Ex: '1503633600'

    coin_symbol_to_its_percentage_of_initial_portfolio = get_coin_symbol_to_its_percentage_of_initial_portfolio()
    coin_symbol_to_map_of_dates_to_prices = get_coin_symbol_to_map_of_dates_to_prices(coin_symbol_to_its_percentage_of_initial_portfolio, days_data)
    coin_symbol_to_initial_buy_in_price = {symbol: coin_symbol_to_map_of_dates_to_prices[symbol][first_day] for symbol in coin_symbols}

    coin_symbol_to_initial_dollar_amount = {symbol: initial_portfolio_size_in_dollars * coin_symbol_to_its_percentage_of_initial_portfolio[symbol] for symbol in coin_symbols}

    coin_symbol_to_coin_amount_held = {symbol: coin_symbol_to_initial_dollar_amount[symbol] / coin_symbol_to_initial_buy_in_price[symbol] for symbol in coin_symbols}

    cash_held = initial_portfolio_size_in_dollars - sum([amount for amount in coin_symbol_to_initial_dollar_amount.values()])

    date_to_portfolio_value = get_date_to_portfolio_value(sorted_dates_as_strings, coin_symbol_to_coin_amount_held,
                                                          coin_symbol_to_map_of_dates_to_prices, cash_held,
                                                          include_cash_in_outputted_portfolio_value)

    output_csv(date_to_portfolio_value)
    return date_to_portfolio_value


def get_days_data(coin_api_name_to_symbol):

    symbol_query = ",".join(coin_api_name_to_symbol.values())  # Ex: "BTC,ETH,ADA"
    url = "https://bindexfund.com/api/v1/get-historical-data?search=" + symbol_query + "&time=1222212322"

    resp = requests.get(url=url)
    days_data = json.loads(resp.text)

    for entry in days_data:
        entry['symbol'] = coin_api_name_to_symbol[entry['name']]
    return days_data


def get_coin_symbol_to_its_percentage_of_initial_portfolio():
    percents_data = get_percents_data()

    coin_symbol_to_its_percentage_of_initial_portfolio = {}
    for entry in percents_data:
        coin_trading_symbol = entry['symbol']
        coin_percentage_of_initial_portfolio = float(entry['percent'])
        coin_symbol_to_its_percentage_of_initial_portfolio[coin_trading_symbol] = coin_percentage_of_initial_portfolio
    return coin_symbol_to_its_percentage_of_initial_portfolio


def get_percents_data():
    with open('percents.json') as percentsfile:
        percents_data = json.load(percentsfile)
    return percents_data


def get_coin_symbol_to_map_of_dates_to_prices(coin_symbol_to_its_percentage_of_initial_portfolio, days_data):
    coin_symbol_to_map_of_dates_to_prices = {}  # Example: {BTC: {date_sec: $504}, ...}
    for coin_symbol in coin_symbol_to_its_percentage_of_initial_portfolio.keys():
        days_data_for_just_this_symbol = {entry['date']: float(entry['price']) for entry in days_data if entry['symbol'] == coin_symbol}

        coin_symbol_to_map_of_dates_to_prices[coin_symbol] = days_data_for_just_this_symbol
    return coin_symbol_to_map_of_dates_to_prices


def get_date_to_portfolio_value(sorted_dates_as_strings, coin_symbol_to_coin_amount_held,
                                coin_symbol_to_map_of_dates_to_prices, cash_held,
                                include_cash_in_outputted_portfolio_value):
    dates_to_portfolio_value = {}
    for index, date in enumerate(sorted_dates_as_strings):  # A date is going to be in seconds as a string, so for example, "1503720000"

        if include_cash_in_outputted_portfolio_value:
            total_portfolio_value_on_this_date = cash_held
        else:
            total_portfolio_value_on_this_date = 0

        for coin_symbol in coin_symbol_to_coin_amount_held.keys():
            coins_held = coin_symbol_to_coin_amount_held[coin_symbol]

            if coin_symbol_to_map_of_dates_to_prices[coin_symbol].get(date):
                value_for_this_coin = coins_held * float(coin_symbol_to_map_of_dates_to_prices[coin_symbol][date])
            else:  # If we didn't get a price for this coin on this date...
                print("No price found for %s on %s" % (coin_symbol, date))
                # Use the average of the previous and next day.
                previous_date_index = index - 1
                next_date_index = index + 1
                while True:
                    previous_date = sorted_dates_as_strings[previous_date_index]
                    if not coin_symbol_to_map_of_dates_to_prices[coin_symbol].get(previous_date):
                        previous_date_index -= 1
                        continue
                    previous_date_value = coins_held * float(coin_symbol_to_map_of_dates_to_prices[coin_symbol][previous_date])
                    break
                try:
                    while True:
                        next_date = sorted_dates_as_strings[next_date_index]
                        if not coin_symbol_to_map_of_dates_to_prices[coin_symbol].get(next_date):
                            next_date_index += 1
                            continue
                        next_date_value = coins_held * float(coin_symbol_to_map_of_dates_to_prices[coin_symbol][next_date])
                        break
                    value_for_this_coin = (previous_date_value + next_date_value) / 2
                except IndexError:
                    value_for_this_coin = previous_date_value

            total_portfolio_value_on_this_date += value_for_this_coin

        dates_to_portfolio_value[parser.parse(date)] = total_portfolio_value_on_this_date
    return dates_to_portfolio_value


def output_csv(date_to_portfolio_value):
    with open('output.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['date', 'total_portfolio_value'])
        for date, total_portfolio_value in date_to_portfolio_value.items():
            writer.writerow([date, total_portfolio_value])


if __name__ == '__main__':
    initial_portfolio_size_in_dollars = 10000
    output_csv_of_dates_to_total_portfolio_value(initial_portfolio_size_in_dollars)
