import tkinter as tk
from tkinter import messagebox
import requests

def fetch_exchange_rates():
    url = "https://v6.exchangerate-api.com/v6/73e440ca59a3c7d32dc59715/latest/USD"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['result'] == 'success':
            return data['conversion_rates']
        else:
            print("Error in fetching exchange rates:", data['error-type'])
            return None
    else:
        print(f"Error fetching data from API: {response.status_code}")
        return None

def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency == "USD":
        base_amount = amount
    else:
        if from_currency not in rates:
            print(f"Invalid from_currency: {from_currency}")
            return None
        base_amount = amount / rates[from_currency]

    if to_currency not in rates:
        print(f"Invalid to_currency: {to_currency}")
        return None

    converted_amount = base_amount * rates[to_currency]
    return converted_amount

def handle_conversion():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_entry.get().upper()
        to_currency = to_currency_entry.get().upper()

        rates = fetch_exchange_rates()
        if rates is None:
            return

        converted_amount = convert_currency(amount, from_currency, to_currency, rates)

        if converted_amount is not None:
            result_label.config(text=f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
        else:
            messagebox.showerror("Error", "Conversion failed due to invalid currencies.")
    
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for amount.")

root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x300")

amount_label = tk.Label(root, text="Amount:")
amount_label.pack(pady=10)
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

from_currency_label = tk.Label(root, text="From Currency (e.g., USD):")
from_currency_label.pack(pady=10)
from_currency_entry = tk.Entry(root)
from_currency_entry.pack(pady=5)

to_currency_label = tk.Label(root, text="To Currency (e.g., EUR):")
to_currency_label.pack(pady=10)
to_currency_entry = tk.Entry(root)
to_currency_entry.pack(pady=5)

convert_button = tk.Button(root, text="Convert", command=handle_conversion)
convert_button.pack(pady=20)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()


