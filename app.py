import os
from flask import Flask, render_template, request, url_for, redirect,session,Response
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import base64
import random
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///valyxstor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQLAlchemy(app)
class products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))
    sizes = db.Column(db.String(80))
    price=db.Column(db.Integer)
    colors = db.Column(db.String(80))
    image=db.Column(db.LargeBinary)
    quantity=db.Column(db.Integer)
    pv= db.Column(db.String(80))
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    email=db.Column(db.Integer)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))
    sizes = db.Column(db.String(80))
    price=db.Column(db.Integer)
    colors = db.Column(db.String(80))
    image=db.Column(db.LargeBinary)
    quantity=db.Column(db.Integer)
    pv= db.Column(db.String(80))
    stat=db.Column(db.Integer)
class Order_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qun=db.Column(db.String(120))
    firstName=db.Column(db.String(120))
    lastName=db.Column(db.String(120))
    phon=db.Column(db.String(120))
    phon2=db.Column(db.String(120))
    email=db.Column(db.String(120))
    zipcode=db.Column(db.String(120))
    address=db.Column(db.String(1200))
    address2=db.Column(db.String(1200))
    user =db.Column(db.String(120))
    Total_bill=db.Column(db.String(120))
    allprodect=db.Column(db.String(120))
    state=db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now()) 

@app.before_request
def before_request():
    if 'random_number' not in session:
        session['random_number'] = random.randint(1000000000000, 10000000000000)
    u=session.get('random_number')
    print(u)
@app.route("/")
def home():
    if 'random_number' not in session:
        session['random_number'] = random.randint(1000000000000, 10000000000000)
        u=session.get('random_number')
        print(u)
    return render_template('index.html')
@app.route("/card")
def card():
    my_p=Card.query.filter_by(email=session['random_number'],stat=0)
    return render_template('card.html',info=my_p)
@app.route("/shop-bags")
def shop_bags():
    list1=products.query.filter_by(pv='bags').all()
    return render_template('shop.html' ,products=list1,items='Bags')
@app.route("/shop-tshirts")
def shop_tshirts():
    list1=products.query.filter_by(pv='tshirts').all()
    return render_template('shop.html' ,products=list1,items='T-Shirts')
@app.route("/shop-hody")
def shop_hody():
    list1=products.query.filter_by(pv='hody').all()
    return render_template('shop.html' ,products=list1,items='Hody')
@app.route("/custom")
def custom():
    return render_template('custom.html')
@app.route('/<int:t_id>/viwe/', methods=('GET', 'POST'))
def viwe(t_id):

    info=products.query.filter_by(id=t_id).first()
    size= info.sizes
    
    lp=products.query.filter_by(pv=info.pv).all()
    return render_template('shop-single.html',info=info,lp=lp,s=size.split())
@app.route('/<int:t_id>/viwe/add', methods=('GET', 'POST'))
def adddd(t_id):
    info=products.query.filter_by(id=t_id).first()
    lp=products.query.filter_by(pv=info.pv).all()
    size= info.sizes
    return render_template('shop-single.html',info=info,lp=lp,mess= 'add',s=size.split())
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/addreset",methods=[ "POST"])
def addreset():
    qun=request.form['qun']
    phon2=request.form['phon']
    firstName=request.form['firstName']
    lastName=request.form['lastName']
    phon=request.form['phon']
    email=request.form['email']
    zipcode=request.form['zip']
    address=request.form['address']
    address2=request.form['address2']
    user =session["random_number"]
    my_p=Card.query.filter_by(email=session['random_number'],stat=0)
    Total_bill=0
    allprodect=0
    for item in my_p:
        print(item.price)
        Total_bill += item.price
        allprodect+=1
    for x in my_p:
        x.stat=1
        db.session.add(x)
        db.session.commit()
    Order = Order_info(qun=qun, 
                       state=0,
                       firstName=firstName,
                       lastName =lastName,
                       allprodect=allprodect,
                       Total_bill=Total_bill, 
                       phon=phon, 
                       email=email,
                       zipcode=zipcode, 
                       address=address,
                       address2=address2,
                       user=user,
                       phon2=phon2
                       )
    db.session.add(Order)
    db.session.commit()
    return render_template('end.html')
# ...
@app.route("/adminvalyx")
def admin():
    try:
        if session['email']=='admin@valyx.valyx':
            return render_template('madmin.html')
        return redirect(url_for('loginadmin'))
    except KeyError:
        return redirect(url_for('loginadmin'))
@app.route("/loginadmin", methods=['GET', 'POST'])
def loginadmin():
    if request.method == 'POST':
        passw = request.form['passw']
        email = request.form['email']
        if passw =="ValyxadminValyx" and email == "admin@valyx.valyx" :
            print('ok')
            session['email']=email
            return redirect("/adminvalyx")
    return render_template("adminlog.html")
@app.route("/<int:t_id>/addtocatd")
def addtocatd(t_id):
        return redirect('/')
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if session['email']=='admin@valyx.valyx':
        if request.method == 'POST':
            print('ok')
            # Retrieve form data
            name = request.form['product-name']
            price = request.form['price']
            description = request.form['description']
            file = request.files['image']
            
            category= request.form.get('category')
            colors = " ".join(request.form.getlist('colors'))
            sizes = request.form['sizes']
            # Save product to database
            product = products(name=name, price=price,pv =category, description=description, sizes=sizes,colors=colors,image=file.read())
            db.session.add(product)
            db.session.commit()
            image_data = base64.b64encode(product.image).decode('utf-8')
            return render_template('add_product.html',mess='Add product',pname=name,image_data=image_data)
        else:
            return render_template('add_product.html')
    else:
        return render_template('404.html')
@app.route('/p/<int:img_id>/img_pic')
def img(img_id):
    img = products.query.get_or_404(img_id)
    return Response(img.image, mimetype='image/jpeg')
@app.route("/addtocard/<int:p_id>" ,methods=['POST','GET'])
def addtocard(p_id):
    if request.method == 'POST':

            yt=products.query.get(p_id)
            size= request.form.get('product-size')
            print(size)
            new_item=Card(
                name=yt.name,
                pid=yt.id,    
                email=session['random_number'],
                description=yt.description,
                sizes=size,
                price=yt.price,
                colors=yt.colors,
                image=yt.image,
                quantity=yt.quantity,
                pv=yt.pv,
                stat=0)
            db.session.add(new_item)
            db.session.commit()
            return redirect(f'/{p_id}/viwe/add')
@app.route("/Checkout")
def Checkout():
    my_p=Card.query.filter_by(email=session['random_number'],stat=0)
    price=0
    numofitem=0
    for item in my_p:
        print(item.price)
        price += item.price
        numofitem+=1
    return render_template('Checkout.html',info=my_p,total=str(price),num=str(numofitem))
@app.route('/deletfromcard/<int:p_id>')
def deletfromcard(p_id):
    product = Card.query.get_or_404(p_id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/card')
@app.route('/shop')
def shopp():
    return render_template('shop1.html')
@app.route('/orders')
def orders():
    if session['email']=='admin@valyx.valyx':
        orders=Order_info.query.filter_by(state=0)
        return render_template('orders.html',info=orders)
    return render_template('404.html')
@app.route('/vieworder/<int:o_id>')
def vieworder(o_id):
    order=Order_info.query.get(o_id)
    my_p=Card.query.filter_by(email=order.user,stat=1)
    return render_template('vieworder.html',user=order,prodects=my_p)
@app.route('/<int:o_id>/finish',methods=('GET', 'POST'))
def finish(o_id):
    info = Order_info.query.get(o_id)
    my_p=Card.query.filter_by(email=info.user,stat=1)
    if request.method == 'POST':
        info.state = 1
        db.session.add(info)
        db.session.commit()
        for x in my_p:
            x.stat=2
            db.session.add(x)
            db.session.commit()
        my_p2=Card.query.filter_by(email=info.user,stat=2)
        return render_template('finish.html',p=my_p2,info=info)
    my_p1=Card.query.filter_by(email=info.user,stat=2)
    return render_template('finish.html',p=my_p1,info=info)
@app.route('/<int:pid>/d1')
def d1(pid):
    p = products.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('edit'))

@app.route('/edit')
def edit():
    if session['email']=='admin@valyx.valyx':
        prodect = products.query.all()
        return render_template('editprodects.html',p=prodect)
    return render_template('404.html')
@app.route('/<int:p_id>/editp',methods=('GET', 'POST'))
def editp(p_id):
    prodect = products.query.get(p_id)
    if request.method == 'POST':
        prodect.name = request.form['product-name']
        prodect.price = request.form['price']
        prodect.description = request.form['description']
        prodect.file = request.files['image'].read()
        prodect.quantity = request.form['quantity']
        prodect.category = request.form.get('category')
        prodect.colors = " ".join(request.form.getlist('colors'))
            
        db.session.commit()
        print(prodect.name)

        return redirect('/edit')
    return render_template('editprodect.html',info= prodect)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
        app.run(host='0.0.0.0',debug=True)   
