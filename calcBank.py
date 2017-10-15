import datetime, locale
from datetime import datetime, date, time, timedelta
import dateutil
from dateutil import parser

# dictionaries - examples
#payload = {"amount": 1000,
#            "term": 12,
#            "rate": 0.05,
#            "date":  '2017-08-05 02:18Z'}
#
#loan = {"loan_id": "000-0000-0000-0000",
#        "installment": 85.60}
#
#payment_made = {"payment": "made",
#                "date": '2017-09-05 02:18Z',
#                "amount": 85.60}

"""
Calculates Installment

Payload:
- amount: loan amount in dollars.
- term: number of months that will take until its gets paid-off.
- rate: interest rate as decimal.
- date: when a loan was asked (origination date as an ISO 8601 string).

- loan_id: unique id of the loan.
- installment: monthly loan payment.

Loan payment formula:
r = rate / 12.
Installment (monthly) = [ r + r / ( (1+r) ^ term - 1) ] x amount

"""
def calcInstallment(payload):
    try:
         #get the values for rate, term and amount from the csv file
         rate = float(payload["rate"])
         term = float(payload["term"])
         amount = float(payload["amount"])
    except ValueError:
        return
   
    #calculate rate per year
    r = rate/12

    #print installment rate as per formula provided
    installment = (r + r/((1+r)**term - 1))*amount
    print "installment = %s" %installment
    
    return installment
    
"""
Calculates the difference between 2 months
"""
def months_between(date1,date2):
    if date2 == None:
        return
    if date1 > date2:
        date1,date2 = date2,date1
    m1 = date1.year*12 + date1.month
    m2 = date2.year*12 + date2.month
    months = m2-m1
    if date1.day > date2.day:
        months-=1
    elif date1.day == date2.day:
        seconds1 = date1.hour*3600 + date1.minute + date1.second
        seconds2 = date2.hour*3600 + date2.minute + date2.second
        if seconds1 > seconds2:
            months-=1
    return months

"""
Get the total number of payments, by using:
- the start date of the loan
- the date when it was payed 
"""
def getNoTotalPayments(payload):
    date_taken = payload["date_taken"]
    #get the start date and time of the payment
    start_datetime = parser.parse(date_taken)
    
    #get the date when the payment was made
    date_payment = payload["date_payment"]
    date_payment = parser.parse(date_payment)
    
    #Print the difference between the current datetime and the start time of the loan
    difference = months_between(date_payment, start_datetime)
    
    return difference

"""
Calculate loan balance using:
- rate
- full_amount
- installment
- number of payments

Formula balance used:
Balance = Full amount + Full amount * Rate - Installment * Number of Payments
"""
def calcBalance(payload):
    #get the values for rate, full_amount, installment and no_payments from the csv file
    try:
        rate = float(payload["rate"])
        full_amount = float(payload["amount"])
        installment = float(payload["installment"])
        no_payments = payload["no_payments"] 
    except ValueError:
        return
    
    payment = no_payments + 1
    #Calculate balance
    balance = full_amount + full_amount * rate - installment*payment
    print "Balance = %s" %balance
    
    return balance
    