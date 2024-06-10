import psycopg2

    
conn=psycopg2.connect(
    user="postgres",
    dbname="myduka",
    password="brina5511",
    host="localhost",
    port=5432
)
cur=conn.cursor()

def get_data(table_name):
    select=f"select * from {table_name}"
    cur.execute(select)
    results=cur.fetchall()
    return results

# get_data("sales")

# def insert_products(values):
#     insert=f"insert into products(name,buying_price,selling_price,stock_quantity)values{values}"
#     cur.execute(insert)
#     conn.commit()
#product_value=("milk",20,50,3)
# insert_products(product_value)




def insert_products(values):
    insert="""insert into products
    (name,buying_price,selling_price,stock_quantity)values(%s,%s,%s,%s)"""
    cur.execute(insert,values)
    conn.commit()
# product_value=("cookies",20,50,2)
# insert_products(product_value)
# get_data("products")
# get_data("sales")

def insert_sales(values):
    insert="""insert into sales(pid,quantity,created_at)values(%s,%s,now())"""
    cur.execute(insert,values)
    conn.commit()

# display profit per product
def total_profit():

    profit="select products.name, sum((selling_price-buying_price)*quantity) as profit from products join sales on sales.pid=products.id group by products.name;"
    cur.execute(profit)
    data=cur.fetchall()
    return data


# display profit per day
# select date(created_at)as now_date,sum((selling_price-buying_price)*quantity)as profit from sales join products on products.id=sales.pid group by now_date order by now_date desc;
def day_profit():
    profit=" select  date(created_at)as day,sum((selling_price-buying_price)*quantity)as profit from products join sales on sales.pid=products.id group by day;"
    cur.execute(profit)
    new_data=cur.fetchall()
    return new_data

#  display sales per products
def products_name():
    name="select products.name, sum(selling_price * quantity)as sales from products join sales on sales.pid=products.id group by products.name;"
    cur.execute(name)
    data=cur.fetchall()
    return(data)

#  sales per day
def sales_name():
    s_name="select date(created_at)as day,sum(selling_price *quantity )as sales from products join sales on sales.pid=products.id group by day;"
    cur.execute(s_name)
    data=cur.fetchall()
    return(data)
#  check email
def check_email(email):
    query="select * from users where email=%s"
    cur.execute(query,(email,))
    data=cur.fetchone()
    return(data)
    
     #insert user 
def  insert_user(values):
    insert_user="insert into users(full_name,email,password)values(%s,%s,%s);"
    cur.execute(insert_user,values)
    conn.commit()
    # check email existance
def ch_email(email):
       query="select * from users where email=%s"
       cur.execute(query,(email,))
       data=cur.fetchall()
       return data
# check email,password existance
def check_email_pass(email,password):
    query="select * from users where email=%s and password=%s"
    cur.execute(query,(email,password))
    data=cur.fetchall()
    return data








