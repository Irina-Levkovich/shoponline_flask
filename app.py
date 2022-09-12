from flask import Flask,render_template,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cloudipsp import Api,Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    isActive = db.Column(db.Boolean, default = True)
    date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<Item %r>' %self.id


@app.route('/product')
def product():
    items = Item.query.order_by(Item.price).all()
    return render_template('product.html', data=items)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/buy/<int:id>')#функция оплаты
def item_buy(id):
    item=Item.query.get(id)#из нашей базы
    api = Api(merchant_id=1396424,# нужен id company(my)
              secret_key='test')# для тестовой версии
    checkout = Checkout(api=api)#объект строницы оплаты
    data = {
        "currency": "BYN",
        "amount": str(item.price)+'00'#+ копейки
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)# перенаправляет на url оплаты


@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title,price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/product')
        except:
            return "Произошла ошибка"

    else:
        return render_template('create.html')


@app.route('/catalog')
def catalog():
    return render_template('catalog.html')


@app.route('/discount')
def discount():
    return render_template('discount.html')


if __name__ == '__main__':
    app.run(debug=True)
