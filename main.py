from flask import Flask,render_template,request,redirect,url_for,flash,session
from database import get_data,insert_products,insert_sales,total_profit,day_profit,products_name,sales_name,insert_user,check_email,ch_email,check_email_pass
# flask instance
app=Flask(__name__)
app.secret_key = "world"

def check_login():
    if "email" not in session:
        return redirect(url_for(login))


@app.route('/')
def hello():
    return render_template("index.html")

# @app.route('/home')
# def home():
#     return "hello brian"

# create for products

@app.route('/sales')
def sales():
    if "email" not in session:
        return redirect(url_for('login'))
    products=get_data('products')
    sales=get_data('sales')
    return render_template("sales.html",sale=sales,prods=products)


@app.route('/products')
def products():
    if "email" not in session:
        return redirect(url_for('login'))
    products=get_data('products')
    # print(products)
    return render_template("products.html",prods=products)




@app.route('/dashboard')
def dashboard():
    if "email" not in session:
        return redirect(url_for('login'))
    dash_profit=total_profit()
    names_profit=[]
    value_profit=[]
    for i in dash_profit:
        names_profit.append(str(i[0]))
        value_profit.append(float(i[1]))


    pay_profit=day_profit()
    p_profit=[]
    products_profit=[]
    for i in pay_profit:
        p_profit.append(str(i[0]))
        products_profit.append(float(i[1]))


        
    
    #  route to display sales per products
    new_products=products_name()
    p_products=[]
    v_products=[]
    for i in new_products:
         p_products.append(str(i[0]))
         v_products.append(float(i[1]))
     #   sales per day
    new_sales=sales_name()
    p_sales=[]
    v_sales=[]
    for i in new_sales:
        p_sales.append(str(i[0]))
        v_sales.append(float(i[1]))


    return render_template("dashboard.html",names_profit=names_profit,value_profit=value_profit,
                           p_profit=p_profit,products_profit=products_profit,p_products=p_products,v_products=v_products,p_sales=p_sales,v_sales=v_sales)






# adding products
@app.route("/Add_products",methods=["POST","GET"])
def add_prods():
    p_name=request.form["product_name"]
    b_price=request.form["buying_price"]
    s_price=request.form["selling_price"]
    s_quantity=request.form["stock_quantity"]
    new_prod=(p_name,b_price,s_price,s_quantity)
    insert_products(new_prod)
    flash(f"{s_quantity}{p_name}added successfully")
    return redirect(url_for("products"))

@app.route("/Add_sales",methods=["POST","GET"])
def add_sale():
    p_product_id=request.form["product_id"]
    s_quantity=request.form["stock_quantity"]
    new_sale=(p_product_id,s_quantity)
    insert_sales(new_sale)
    # flash(f())
    return  redirect(url_for("sales"))



#  route for register
@app.route("/register",methods=["POST","GET"])
def register():
    #  get form data
    if request.method=="POST":
        f_name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
    #  insert user
        c_email=check_email(email)
        if c_email==None:
            new_user=(f_name,email,password)
            insert_user(new_user)
            flash("register successful","success")
            return redirect(url_for("login"))
        else :
            flash("email already exist","success")
            
    return render_template("register.html")

@app.route("/login",methods=["POST","GET"])
def login():
    
     # get form data
        if request.method=="POST":
            email=request.form["email"]
            password=request.form["password"]

# check email existance
            c_email=(ch_email)(email)

            if len(c_email)<1:
                flash("try again")
                return redirect(url_for("register "))
            else:
                ch_pass=check_email_pass(email,password)
                if len(ch_pass)<1:
                    flash("incorrect email or password","danger")
                else:
                    session["email"]=email

                    flash("login successful","success")
                    return redirect(url_for("dashboard"))
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("email",None)
    flash("logout successfully",'success')
    return redirect(url_for("login"))





app.run(debug=True)


# CREATE TABLE users (id SERIAL PRIMARY KEY,full_name VARCHAR(50)  NOT NULL,email VARCHAR(100) UNIQUE NOT NULL,password VARCHAR(100) NOT NULL);