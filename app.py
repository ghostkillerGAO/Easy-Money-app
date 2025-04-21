from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

expenses = []
income = []

@app.route('/')
def home():
    today_expenses = sum(e['amount'] for e in expenses if e['date'] == datetime.today().date())
    total_income = sum(i['amount'] for i in income)
    total_expense = sum(e['amount'] for e in expenses)
    balance = total_income - total_expense

    return render_template('index.html', today_expenses=today_expenses,
                           total_income=total_income, total_expense=total_expense,
                           balance=balance)

@app.route('/log-expense', methods=['GET', 'POST'])
def log_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        note = request.form['note']
        expenses.append({'amount': amount, 'category': category, 'note': note, 'date': datetime.today().date()})
        return redirect(url_for('home'))
    return render_template('log_expense.html')

@app.route('/log-income', methods=['GET', 'POST'])
def log_income():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        source = request.form['source']
        note = request.form['note']
        income.append({'amount': amount, 'source': source, 'note': note, 'date': datetime.today().date()})
        return redirect(url_for('home'))
    return render_template('log_income.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
