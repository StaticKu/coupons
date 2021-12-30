from datetime import datetime
from functools import wraps

from flask import render_template, request, redirect, flash, url_for

from MyExp4 import app
from MyExp4.database import db_session, engine
from sqlalchemy import text
from MyExp4.models import CouponsForm, CustomerForm, Sign
from MyExp4.crud import CouponsInsert
from MyExp4.crud import CustomerInsert
from MyExp4.crud import SignInsert

from sqlalchemy import text

from MyExp4 import models
from MyExp4.database import db_session

user_number = 0


@app.route('/admin/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form["password"]
        db = db_session()
        error = None

        if not email:
            error = 'Email address is required.'
        elif not password:
            error = 'Please enter the password.'

        if error is None:
            try:
                from MyExp4.crud import CustomerInsert
                db.execute(
                    "INSERT INTO customer_form (name, email) VALUES (?, ?)",
                    (name, email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {name} is already registered."
            else:
                return redirect(url_for("admin.login"))

        flash(error)

    return render_template('admin/register.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    try:
        session = db_session()  # 创建会话
        global user_number
        if request.method == 'POST':
            email = request.form['email']
            password = request.form["password"]
            db = db_session()
            error = None

            if not email:
                error = 'Email address is required.'
            elif not password:
                error = 'Please enter the password.'
            user = db.execute(
                text('SELECT * FROM customer_form WHERE email =:email'), {'email': email}).fetchone()
            user_number = user[1]
            new_log = models.LogTable(customer_number=user_number, operation="login",
                                      op_time=datetime.now(), success="yes")
            session.add(new_log)
            session.commit()  # 提交即保存到数据库
            session.close()  # 关闭会话
            if user is None:
                error = 'Invalid user!'

            if error is None:
                # return render_template("home.html", user=user)
                return redirect(url_for('home'))
            else:
                flash(error)
                return redirect(url_for('login'))
    except AttributeError:
        new_log = models.LogTable(customer_number=user_number, operation="login",
                                  op_time=datetime.now(), success="no")
        session.add(new_log)
        session.commit()  # 提交即保存到数据库
        session.close()  # 关闭会话
        flash(error)
        return redirect(url_for('login'))
    except Exception as e:
        new_log = models.LogTable(customer_number=user_number, operation="login",
                                  op_time=datetime.now(), success="no")
        session.add(new_log)
        session.commit()  # 提交即保存到数据库
        session.close()  # 关闭会话
        flash(error)
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route("/logout")
def logout():
    session = db_session()  # 创建会话
    new_log = models.LogTable(customer_number=user_number, operation="logout",
                              op_time=datetime.now(), success="yes")
    session.add(new_log)
    session.commit()  # 提交即保存到数据库
    session.close()  # 关闭会话
    """Clear the current session, including the stored user id."""
    db_session.clear()
    return redirect(url_for("login"))


@app.route('/functions/MaximumPrice', methods=['GET', 'POST'])
def MaximumPrice():
    try:
        session = db_session()  # 创建会话
        max_price = 50.0
        if request.method == 'POST':
            max_price = request.form["maximum_price"]
            new_log = models.LogTable(customer_number=user_number, operation="FindMaximumPrice",
                                      op_time=datetime.now(), success="yes")
            session.add(new_log)
            session.commit()  # 提交即保存到数据库
            session.close()  # 关闭会话
        else:
            new_log = models.LogTable(customer_number=user_number, operation="FindMaximumPrice",
                                      op_time=datetime.now(), success="yes")
            session.add(new_log)
            session.commit()  # 提交即保存到数据库
            session.close()  # 关闭会话
        return render_template('functions/MaximumPrice.html',
                               results=db_session.execute(
                                   text('SELECT * FROM maximum_price(:max_price)'), {'max_price': max_price}).all())
    except Exception as e:
        new_log = models.LogTable(customer_number=user_number, operation="FindMaximumPrice",
                                  op_time=datetime.now(), success="no")
        session.add(new_log)
        session.commit()  # 提交即保存到数据库
        session.close()  # 关闭会话
        return redirect(url_for('MaximumPrice'))
    # return render_template('home.html', Coupons=db_session.query(CouponsForm).all())


@app.route('/functions/MoreThan100')
def MoreThan100():
    session = db_session()  # 创建会话
    new_log = models.LogTable(customer_number=user_number, operation="MoreThan100",
                              op_time=datetime.now(), success="yes")
    session.add(new_log)
    session.commit()  # 提交即保存到数据库
    session.close()  # 关闭会话
    return render_template('functions/MoreThan100.html',
                           results=db_session.execute("SELECT * FROM more_than_100()").all())


@app.route('/functions/MostPopularDeal')
def MostPopularDeal():
    session = db_session()  # 创建会话
    new_log = models.LogTable(customer_number=user_number, operation="MostPopularDeal",
                              op_time=datetime.now(), success="yes")
    session.add(new_log)
    session.commit()  # 提交即保存到数据库
    session.close()  # 关闭会话
    return render_template('functions/MostPopularDeal.html',
                           results=db_session.execute("SELECT * FROM most_popular_deal()").all())


@app.route('/functions/Bargain')
def Bargain():
    session = db_session()  # 创建会话
    new_log = models.LogTable(customer_number=user_number, operation="Bargain",
                              op_time=datetime.now(), success="yes")
    session.add(new_log)
    session.commit()  # 提交即保存到数据库
    session.close()  # 关闭会话
    return render_template('functions/Bargain.html',
                           results=db_session.execute("SELECT * FROM percentage_bargain()").all())


@app.route('/functions/AddCoupon', methods=['GET', 'POST'])
def AddCoupon():
    try:
        session = db_session()  # 创建会话
        if request.method == 'POST':
            deal_number = request.form["deal_number"]
            description = request.form["description"]
            location = request.form["location"]
            deal_price = request.form["deal_price"]
            original_price = request.form["original_price"]
            ending_date = request.form["ending_date"]
            print(user_number)
            CouponsInsert(user_number, deal_number, description, location, deal_price, original_price, ending_date)
        return render_template('functions/AddCoupon.html')
    except Exception as e:
        new_log = models.LogTable(customer_number=user_number, operation="AddCoupon",
                                  op_time=datetime.now(), success="no")
        session.add(new_log)
        session.commit()  # 提交即保存到数据库
        session.close()  # 关闭会话
        return redirect(url_for('AddCoupon'))

@app.route('/functions/AddCustomer', methods=['GET', 'POST'])
def AddCustomer():
    try:
        session = db_session()  # 创建会话
        if request.method == 'POST':
            customer_number = request.form["customer_number"]
            name = request.form["name"]
            email = request.form["email"]

            CustomerInsert(customer_number, name, email)
        return render_template('functions/AddCustomer.html')
    except Exception as e:
        new_log = models.LogTable(customer_number=user_number, operation="AddCustomer",
                                  op_time=datetime.now(), success="no")
        session.add(new_log)
        session.commit()  # 提交即保存到数据库
        session.close()  # 关闭会话
        return redirect(url_for('AddCustomer'))


@app.route('/functions/AddSignup', methods=['GET', 'POST'])
def AddSignup():
    try:
        session = db_session()  # 创建会话
        if request.method == 'POST':
            sign_up_number = request.form["sign_up_number"]
            customer_number = request.form["customer_number"]
            deal_number = request.form["deal_number"]

            SignInsert(customer_number, sign_up_number, deal_number)
        return render_template('functions/AddSignup.html')
    except Exception as e:
        new_log = models.LogTable(customer_number=user_number, operation="AddSignup",
                                  op_time=datetime.now(), success="no")
        session.add(new_log)
        session.commit()  # 提交即保存到数据库
        session.close()  # 关闭会话
        return redirect(url_for('AddSignup'))


@app.route('/functions/MyCoupons', methods=['GET', 'POST'])
def MyCoupons():
    try:
        session = db_session()  # 创建会话
        customer_number = str(user_number)
        if request.method == 'POST':

            session = db_session()  # 创建会话

            customer_number = request.form["customer_number"]
            new_log = models.LogTable(customer_number=customer_number, operation="FindMyCoupons",
                                      op_time=datetime.now(), success="yes")
            session.add(new_log)
            session.commit()
            session.close()  # 关闭会话
            return render_template('functions/MyCoupons.html',
                                   results=db_session.execute(
                                       text('SELECT * FROM personal_signup(:customer_number)'),
                                       {'customer_number': customer_number}).all())
    except AttributeError:
        new_log = models.LogTable(customer_number=user_number, operation="FindMyCoupons",
                                  op_time=datetime.now(), success="no")
        session.add(new_log)
        session.commit()  # 提交即保存到数据库
        session.close()  # 关闭会话
        return redirect(url_for('MyCoupons'))

    except Exception as e:
        new_log = models.LogTable(customer_number=customer_number, operation="FindMyCoupons",
                                  op_time=datetime.now(), success="no")
        session.add(new_log)
        session.commit()
        session.close()
        flash("暂无已选优惠券")
        return redirect('/MyCoupons')
    return render_template('functions/MyCoupons.html',
                           results=db_session.execute(
                               text('SELECT * FROM personal_signup(:customer_number)'),
                               {'customer_number': customer_number}).all())

    # return render_template('home.html', Coupons=db_session.query(CouponsForm).all())
