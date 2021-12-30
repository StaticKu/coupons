from flask import render_template, request

from MyExp4 import app
from MyExp4.database import db_session, engine
from sqlalchemy import text
from MyExp4.models import CouponsForm, CustomerForm, Sign
from MyExp4.crud import CouponsInsert
from MyExp4.crud import CustomerInsert
from MyExp4.crud import SignInsert


@app.route('/functions/MaximumPrice', methods=['GET', 'POST'])
def MaximumPrice():
    max_price = 50.0
    if request.method == 'POST':
        max_price = request.form["maximum_price"]
    return render_template('functions/MaximumPrice.html',
                           results=db_session.execute(
                               text('SELECT * FROM maximum_price(:max_price)'), {'max_price': max_price}).all())
    # return render_template('home.html', Coupons=db_session.query(CouponsForm).all())


@app.route('/functions/MoreThan100')
def MoreThan100():
    return render_template('functions/MoreThan100.html',
                           results=db_session.execute("SELECT * FROM more_than_100()").all())


@app.route('/functions/MostPopularDeal')
def MostPopularDeal():
    return render_template('functions/MostPopularDeal.html',
                           results=db_session.execute("SELECT * FROM most_popular_deal()").all())


@app.route('/functions/Bargain')
def Bargain():
    return render_template('functions/Bargain.html',
                           results=db_session.execute("SELECT * FROM percentage_bargain()").all())


@app.route('/functions/AddCoupon', methods=['GET', 'POST'])
def AddCoupon():
    if request.method == 'POST':
        deal_number = request.form["deal_number"]
        description = request.form["description"]
        location = request.form["location"]
        deal_price = request.form["deal_price"]
        original_price = request.form["original_price"]
        ending_date = request.form["ending_date"]

        CouponsInsert("admin", deal_number, description, location, deal_price, original_price, ending_date)
    return render_template('functions/AddCoupon.html')


@app.route('/functions/AddCustomer', methods=['GET', 'POST'])
def AddCustomer():
    if request.method == 'POST':
        customer_number = request.form["customer_number"]
        name = request.form["name"]
        email = request.form["email"]

        CustomerInsert(customer_number, name, email)
    return render_template('functions/AddCustomer.html')


@app.route('/functions/AddSignup', methods=['GET', 'POST'])
def AddSignup():
    if request.method == 'POST':
        sign_up_number = request.form["sign_up_number"]
        customer_number = request.form["customer_number"]
        deal_number = request.form["deal_number"]

        SignInsert(customer_number, sign_up_number, deal_number)
    return render_template('functions/AddSignup.html')


@app.route('/functions/MyCoupons', methods=['GET', 'POST'])
def MyCoupons():
    customer_number = 'C2000'
    if request.method == 'POST':
        customer_number = request.form["customer_number"]
    return render_template('functions/MyCoupons.html',
                           results=db_session.execute(
                               text('SELECT * FROM personal_signup(:customer_number)'),
                               {'customer_number': customer_number}).all())
    # return render_template('home.html', Coupons=db_session.query(CouponsForm).all())
