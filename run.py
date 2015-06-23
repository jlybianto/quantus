from flask import Flask, render_template, request
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
                        current_time=datetime.datetime.now())

@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
  """Convert a datetime to a different format."""
  return value.strftime(format)

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=8080)