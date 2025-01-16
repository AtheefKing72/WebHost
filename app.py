from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API endpoint for currency conversion
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

@app.route('/')
def index():
    # Fetch supported currencies from the API
    response = requests.get(API_URL)
    if response.status_code != 200:
        return "Error fetching currencies. Please try again later."
    
    data = response.json()
    currencies = list(data['rates'].keys())  # Get all currency codes

    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert():
    base_currency = request.form['base_currency']
    target_currency = request.form['target_currency']
    amount = float(request.form['amount'])

    # Fetch exchange rates
    response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base_currency}")
    if response.status_code != 200:
        return "Error fetching exchange rate. Please try again later."

    data = response.json()
    rates = data['rates']

    if target_currency not in rates:
        return "Target currency not supported."

    conversion_rate = rates[target_currency]
    converted_amount = amount * conversion_rate

    return render_template(
        'result.html',
        base_currency=base_currency,
        target_currency=target_currency,
        amount=amount,
        converted_amount=converted_amount,
        conversion_rate=conversion_rate,
    )

if __name__ == '__main__':
    app.run(debug=True)
