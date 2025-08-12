import tkinter as tk
import requests
from forex_python.converter import CurrencyRates

# Supported currencies (fiat + crypto)
common_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'BTC', 'ETH', 'DOGE', 'LTC', 'BNB', 'XRP']

class CurrencyConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Currency Converter')
        self.root.geometry('250x230')

        self.refresh_interval = 5000  # Auto-refresh every 5 seconds

        # FROM currency
        self.from_var = tk.StringVar(self.root)
        self.from_var.set('USD')
        self.from_menu = tk.OptionMenu(self.root, self.from_var, *common_currencies)
        self.from_menu.pack(pady=5)

        # TO currency
        self.to_var = tk.StringVar(self.root)
        self.to_var.set('EUR')
        self.to_menu = tk.OptionMenu(self.root, self.to_var, *common_currencies)
        self.to_menu.pack(pady=5)

        # Amount input
        self.amount_label = tk.Label(self.root, text='Amount:')
        self.amount_label.pack(pady=1)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.insert(0, "1")  # Default amount
        self.amount_entry.pack(pady=5)

        # Convert button (manual option)
        self.convert_button = tk.Button(self.root, text='Convert', command=self.convert_currency)
        self.convert_button.pack(pady=5)

        # Result label
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=5)

        # Start auto-refresh loop
        self.auto_refresh()

        # Keep the window open
        self.root.mainloop()

    def auto_refresh(self):
        self.convert_currency()
        self.root.after(self.refresh_interval, self.auto_refresh)

    def convert_currency(self):
        try:
            from_currency = self.from_var.get().upper()
            to_currency = self.to_var.get().upper()
            amount = float(self.amount_entry.get())

            crypto_list = ['BTC', 'ETH', 'DOGE', 'LTC', 'BNB', 'XRP']

            if from_currency in crypto_list or to_currency in crypto_list:
                url = "https://api.coingecko.com/api/v3/simple/price"
                coin_id = self.crypto_id(from_currency, to_currency)
                vs_id = self.vs_currency_id(from_currency, to_currency)
                params = {"ids": coin_id, "vs_currencies": vs_id}
                resp = requests.get(url, params=params).json()

                if coin_id in resp and vs_id in resp[coin_id]:
                    rate = resp[coin_id][vs_id]
                else:
                    self.result_label.config(text="Crypto conversion failed")
                    return
            else:
                c_rates = CurrencyRates()
                rate = c_rates.get_rate(from_currency, to_currency)

            converted_amount = amount * rate
            self.result_label.config(
                text=f'{amount} {from_currency} = {converted_amount:.6f} {to_currency}'
            )

        except ValueError:
            self.result_label.config(text='Please enter a valid number')
        except Exception as e:
            self.result_label.config(text=f'Error: {e}')

    def crypto_id(self, from_currency, to_currency):
        mapping = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'DOGE': 'dogecoin',
            'LTC': 'litecoin',
            'BNB': 'binancecoin',
            'XRP': 'ripple'
        }
        return mapping.get(from_currency, mapping.get(to_currency)).lower()

    def vs_currency_id(self, from_currency, to_currency):
        mapping = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'DOGE': 'dogecoin',
            'LTC': 'litecoin',
            'BNB': 'binancecoin',
            'XRP': 'ripple'
        }
        if from_currency in mapping:
            return to_currency.lower()
        return from_currency.lower()


if __name__ == '__main__':
    CurrencyConverter()

        