from flask import Flask, render_template, request, flash
from math import log
import datetime

current_time=datetime.datetime.now()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def test():  
  return render_template('base.html',
                         my_title="Home page is currently under construction",
                         current_time=datetime.datetime.now())

@app.route("/fin", methods=["GET"])
def compound_interest_get():
  return render_template('compound_interest.html',
                         my_title="Compound Interest",
                         present_value="",
                         interest_rate="",
                         time="",
                         future_value="",
                         current_time=datetime.datetime.now())

@app.route("/fin", methods=["POST"])
def compound_interest_post():
  present_value = request.form["present_value"]
  interest_rate = request.form["interest_rate"]
  time = request.form["time"]
  future_value = request.form["future_value"]
  if ((not present_value) + (not interest_rate) + (not time) + (not future_value)) != 1:
    raise RuntimeError
  if not present_value:
    present_value = round(float(future_value) / ((1 + float(interest_rate)) ** float(time)), 2)
  elif not interest_rate:
    interest_rate = round((((float(future_value) / float(present_value)) ** (1 / float(time))) - 1), 2)
  elif not time:
    time = round((log(float(future_value) / float(present_value)) / log(1 + float(interest_rate))), 2)
  elif not future_value:
    future_value = round((float(present_value) * ((1 + float(interest_rate)) ** float(time))), 2)
  return render_template('compound_interest.html',
                         my_title="Compound Interest",
                         present_value=present_value,
                         interest_rate=interest_rate,
                         time=time,
                         future_value=future_value,
                         current_time=datetime.datetime.now())

@app.route("/min", methods=["GET"])
def minimum_balance_get():
  return render_template('pay_minimum.html',
                        my_title="Paying Minimum Balance",
                        balance="",
                        annualInterestRate="",
                        monthlyPaymentRate="",
                        current_time=datetime.datetime.now())

@app.route("/min", methods=["POST"])
def minimum_balance_post():
  balance = request.form["balance"]
  annualInterestRate = request.form["annualInterestRate"]
  monthlyPaymentRate = request.form["monthlyPaymentRate"]
  
  month = 0
  totalPaid = 0
  monthsInYear = range(0, 12)
  for month in monthsInYear:
    minimumMonthlyPayment = float(monthlyPaymentRate) * float(balance)
    monthlyUnpaidBalance = float(balance) - float(minimumMonthlyPayment)
    monthlyInterest = (float(annualInterestRate) / 12.0) * float(monthlyUnpaidBalance)
    balance = monthlyUnpaidBalance + monthlyInterest
    month += 1
    totalPaid += minimumMonthlyPayment
  
  return render_template('pay_minimum.html',
                        my_title="Paying Minimum Balance",
                        balance = request.form["balance"],
                        annualInterestRate=annualInterestRate,
                        monthlyPaymentRate=monthlyPaymentRate,
                        month=month,
                        minimumMonthlyPayment=minimumMonthlyPayment,
                        totalPaid="%.2f" % totalPaid,
                        remainingBalance="%.2f" % balance,
                        current_time=datetime.datetime.now())
  
@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
  """Convert a datetime to a different format."""
  return value.strftime(format)

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=8080)