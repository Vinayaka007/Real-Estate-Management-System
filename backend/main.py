import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, flash, json, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, logout_user, login_user, LoginManager, current_user
from sqlalchemy import text, inspect
from sqlalchemy.exc import InvalidRequestError
import random
from datetime import datetime




#database connection
local_server=True
app=Flask(__name__)
app.secret_key="vinu007"

#this is for getting unique user access
login_manager=LoginManager(app)
print("this is login_manager",login_manager)
login_manager.login_view='login'

with open(r'C:\Users\vinay\OneDrive\Desktop\DBMS_PROJECT\backend\config.json', 'r') as c:
    params=json.load(c)["params"]

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/realestate'
db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) or Propertyuser.query.get(int(user_id)) or Buyer.query.get(int(user_id))

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, default=lambda: random.randint(1, 1000))
    srfid=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(20))
    dob=db.Column(db.String(20))

class Propertyuser(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, default=lambda: random.randint(1000, 2000))
    pcode=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(50))
    password=db.Column(db.String(20))

class Propertydata(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=lambda: random.randint(2000, 3000))
    pcode=db.Column(db.String(20),unique=True)
    plocation=db.Column(db.String(200))
    ptype=db.Column(db.String(20))  
    bedroom=db.Column(db.Integer)
    dimension=db.Column(db.String(200))
    price=db.Column(db.Integer) 

class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=lambda: random.randint(3000, 4000))
    srfid=db.Column(db.String(20))
    pcode=db.Column(db.String(20))
    ptype=db.Column(db.String(200))
    pbedroom=db.Column(db.Integer)
    plocation=db.Column(db.String(200))
    bname=db.Column(db.String(200))
    bphno=db.Column(db.String(200))
    baddress=db.Column(db.String(200))



class Property_history(db.Model):
    id = db.Column(db.Integer, primary_key=True,default=lambda: random.randint(10000, 200000))
    property_id = db.Column(db.Integer)  # No foreign key
    pcode = db.Column(db.String(20))
    plocation = db.Column(db.String(200))
    ptype = db.Column(db.String(20))
    bedroom = db.Column(db.Integer)
    dimension = db.Column(db.String(200))
    price = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())



@app.route('/property_history')
def property_history():
    history_entries = Property_history.query.all()
    return render_template('trig_history.html', history_entries=history_entries)








def create_dynamic_model(views):
    existing_table = db.metadata.tables.get(views)
    
    if existing_table is not None:
        DynamicTable = type(views, (db.Model,), {"__tablename__": views})
    else:
        class DynamicTable(db.Model):
            __tablename__ = views
            id = db.Column(db.Integer, primary_key=True)
            pcode = db.Column(db.String(20), unique=True)
            plocation = db.Column(db.String(50))
        try:
            db.create_all()
        except InvalidRequestError:
            pass
    return DynamicTable



@app.route('/view')
def display_data():
    dynamic_table_name = 'views'
    DynamicTable = create_dynamic_model(dynamic_table_name)
    data = DynamicTable.query.all()
    columns = inspect(DynamicTable).columns.keys()
    return render_template('view.html', data=data, columns=columns)










@app.route('/propertylogin', methods=['POST', 'GET'])
def propertylogin():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = Propertyuser.query.filter_by(email=email).first()
        print(user, Propertyuser, email)
        if user and user.password == password:
            login_user(user)
            flash("Login Success","info")
            return redirect(url_for('addpropertyinfo'))    
        else:
            flash("Invalid Credentials", "danger")
            return render_template("propertylogin.html")
    return render_template('propertylogin.html')




def fetch_user_data():
    if current_user.is_authenticated:
        print(current_user)
        property_user = Propertyuser.query.filter_by(id=current_user.id).first()
        if property_user:
            user_data = Propertydata.query.filter_by(pcode=property_user.pcode).first()
            return user_data

    return None



@app.route("/addpropertyinfo", methods=['POST', 'GET'])
@login_required
def addpropertyinfo():
    
    current_property = None
    print("Entering addpropertyinfo function")

    if current_user.is_authenticated:
        print("User is authenticated")
        user_data = fetch_user_data()
        
        if request.method == "POST":
            print("Handling POST request in addpropertyinfo function")
            
            pcode = request.form.get('pcode')
            plocation = request.form.get('plocation')
            ptype = request.form.get('ptype')
            bedroom = request.form.get('bedroom')
            dimension = request.form.get('dimension')
            price = request.form.get('price')

            hduser = Propertydata.query.filter_by(pcode=pcode).first()
            
            if hduser:
                flash("Property with this code already exists", "primary")
                # Fetch user data to display in "Your Entered Data" section
                fetch_user_data()
                return render_template("propertydata.html", user_data=user_data)
            
            # Assuming you want to associate the property with the currently logged-in user
            query = Propertydata(pcode=pcode, plocation=plocation, ptype=ptype, bedroom=bedroom, dimension=dimension, price=price)
            db.session.add(query)
            db.session.commit()
            flash("Data Is Added", "primary") 
            # Fetch user data to display in "Your Entered Data" section after adding data
            fetch_user_data()

        print(f"Is authenticated: {current_user.is_authenticated}")
        return render_template('propertydata.html', user_data=user_data)

    else:
        flash("You need to login to add property info", "warning")
        return redirect(url_for('propertylogin'))






@app.route("/")
def home():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/property-grid')
def property_grid():
    return render_template('property-grid.html')

@app.route('/about')
def about():
    return render_template('about.html')






@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method=="POST":
        srfid=request.form.get('srf')
        email=request.form.get('email')
        dob=request.form.get('dob')
        user=User.query.filter_by(srfid=srfid).first()
        emailuser=User.query.filter_by(email=email).first()
        if user or emailuser:
            flash("Email or srfid is already taken!","warning")
            return render_template("usersignup.html")
        new_user = User(srfid=srfid, email=email, dob=dob)
        db.session.add(new_user)
        db.session.commit()
        flash("signin success, Please login", "success")
        return render_template("userlogin.html")

    return render_template('usersignup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        srfid = request.form.get('srf')
        dob = request.form.get('dob')
        user = User.query.filter_by(srfid=srfid).first()
        if user and user.dob == dob:
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials", "danger")
            return render_template("userlogin.html")
    return render_template('userlogin.html')



#admin login
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if(username==params['user'] and password==params['password']):
            session['user']=username
            flash("Login Successful","info")
            return render_template("addProperty.html")
        else:
            flash("invalid credentials!","danger")
    return render_template('admin.html')



#logout user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('home'))

#logout admin
@app.route('/logoutadmin')
def logoutadmin():
    session.pop('user')
    flash("your logout","primary")
    return redirect('/admin')





@app.route('/addPropertyuser', methods=['POST', 'GET'])
def propertyuser():
    if 'user' in session and session['user'] == params['user']:
        if request.method == "POST":
            pcode = request.form.get('pcode')
            email = request.form.get('email')
            password = request.form.get('password')
            emailuser = Propertyuser.query.filter_by(email=email).first()
            
            if emailuser:
                flash("Email is already taken!", "warning")
                return render_template("addProperty.html")

            # Assuming your Propertyuser model has fields pcode, email, and password
            new_user = Propertyuser(pcode=pcode, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash("User added successfully!", "success")
            return render_template("addProperty.html")

    else:
        flash("Login and Try Again", "warning")
        return render_template("addProperty.html")









@app.route("/pedit/<string:id>", methods=['POST','GET'])
@login_required
def pedit(id):

    if request.method == "POST":
        pcode = request.form.get('pcode')
        plocation = request.form.get('plocation')
        ptype = request.form.get('ptype')
        bedroom = request.form.get('bedroom')
        dimension = request.form.get('dimension')
        price = request.form.get('price')

        query = text("UPDATE propertydata SET plocation=:plocation, ptype=:ptype, bedroom=:bedroom, dimension=:dimension, price=:price WHERE pcode=:pcode")
        db.session.execute(query, {"id": id, "pcode": pcode, "plocation": plocation, "ptype": ptype, "bedroom": bedroom, "dimension": dimension, "price": price})
        db.session.commit()

        flash("updated!","info")
        return redirect('/addpropertyinfo')
    user_data=Propertydata.query.filter_by(id=id).first()
    return render_template("pedit.html", user_data=user_data)


@app.route("/pdelete/<string:id>", methods=['POST', 'GET'])
@login_required
def pdelete(id):
    # Assuming "propertydata" is the name of your table
    query = text("DELETE FROM propertydata WHERE id = :id")
    db.session.execute(query, {"id": id})
    db.session.commit()

    flash("Data Deleted!", "danger")
    return redirect('/addpropertyinfo')


@app.route('/buyproperty', methods=['GET', 'POST'])
@login_required
def buy_property():
 
    if request.method == 'POST':
        pcode = request.form.get('pcode')
        print(pcode)
        property = Propertydata.query.filter_by(pcode=pcode).first()

        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        print(name, phone, address)
        new_buyer = Buyer(srfid=current_user.srfid, pcode=pcode, ptype=property.ptype, pbedroom=property.bedroom, plocation=property.plocation, bname=name, bphno=phone, baddress=address)
        db.session.add(new_buyer)
        db.session.commit()

        flash('Reserved! You Can Contact The seller For Further','success')

        # Fetch the buyer information associated with the current user
        buyer_info = Buyer.query.filter_by( srfid=current_user.srfid, pcode=pcode).first()

        return render_template('buy.html', buyer_info=buyer_info)

    else:
        # For GET request, display the available properties
        properties = Propertydata.query.all()
        return render_template('buy.html', properties=properties)




#testing for connection
@app.route("/test")
def test():
    property_history()

    try:
        a=Test.query.all()
        print(a)
        return 'MY DB IS CONNECTED'
    except Exception as e:
        print(e)
        return f'MY DB IS NOT RUNNING {e}'
app.run(debug=True)