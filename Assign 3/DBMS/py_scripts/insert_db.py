import pymysql
import datetime

def check_user_exists(username):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query  = "select * from user where username='"+username+"'"
    c.execute(query)
    result = c.fetchall()
    if len(result) > 0 :
        return 1
    else:
         return 0
def check_sysadmin_exists(username):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query  = "select * from sys_admin where username='"+username+"'"
    c.execute(query)
    result = c.fetchall()
    if len(result) > 0 :
        return 1
    else:
         return 0

def check_res_user_exists(username):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query  = "select * from restaurant where username='"+username+"'"
    c.execute(query)
    result = c.fetchall()
    if len(result) > 0 :
        return 1
    else:
         return 0

# it also returns the loc_id if the location is already present
def check_location_exists(address,city):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select loc_id from location where address ='{}' and city='{}'".format(address,city)
    c.execute(query)
    result = c.fetchall()
    if len(result) > 0:
        return (1,int(result[0]['loc_id']))
    else :
        return (0,-1)    



def insert_user(username, name, hashed_password, email_id, address):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    check_exist = check_user_exists(username)
    if check_exist == 1:
        return -1
    
    query  = "select * from user" 
    c.execute(query)
    result = c.fetchall()
    user_id = 0
    for i in range(0, len(result)):
        if(result[i]['user_id'] > user_id):
            user_id = result[i]['user_id'];


    query = "insert into user values('{}','{}','{}','{}','{}','{}')".format(user_id+1,username,name,hashed_password,email_id,address) 
    c.execute(query)
    return 1

def insert_restaurant(username,name,hashed_password,email_id,phone,start_time,end_time,category,address,city,image_link):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    # check location and find loc_id
    (flag,loc_id) = check_location_exists(address,city)
    
    if flag == 0:
        # if no loc_id then create entry in location table
        insert_location(address,city)
        (flag,loc_id) = check_location_exists(address,city)


    # insert into restaurant table
    
    query  = "select * from restaurant" 
    c.execute(query)
    result = c.fetchall()
    res_id=0
    for i in range(0, len(result)):
        if(result[i]['res_id'] > res_id):
            res_id = result[i]['res_id'];
    
    
    query = "insert into restaurant values({},'{}','{}','{}','{}','{}',{},'{}','{}','{}','{}')".format(res_id+1,username,name,hashed_password,email_id,phone,loc_id,start_time,end_time,category,image_link)
    c.execute(query)    
    
    insert_located_in(res_id,loc_id)
    return 1

def insert_located_in(res_id,loc_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "insert into located_in values({},{})".format(res_id,loc_id)
    c.execute(query)

    return 1

def insert_location(address,city):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query  = "select * from location" 
    c.execute(query)
    result = c.fetchall()
    loc_id = len(result) + 1

    query = "insert into location values({},'{}','{}')".format(loc_id,address,city)
    c.execute(query)

    return 1

def match_user_login(username,hashed_password):
    check_user = check_user_exists(username)
    if check_user == 0:
        return -1

    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "select hashed_password from user where username = '{}'".format(username)
    c.execute(query)
    result = c.fetchall()
    hp_retrieved = result[0]['hashed_password']   
    if hp_retrieved == hashed_password:
        return 1
    else :
        return -1

def match_sysadmin_login(username,hashed_password):
    check_admin = check_sysadmin_exists(username)
    if check_admin == 0:
        return -1

    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "select hashed_password from sys_admin where username = '{}'".format(username)
    c.execute(query)
    result = c.fetchall()
    hp_retrieved = result[0]['hashed_password']   
    if hp_retrieved == hashed_password:
        return 1
    else :
        return -1


def match_restaurant_login(username,hashed_password):
    check_res_user = check_res_user_exists(username)
    if check_res_user == 0:
        return -1

    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "select hashed_password from restaurant where username = '{}'".format(username)
    c.execute(query)
    result = c.fetchall()
    hp_retrieved = result[0]['hashed_password']   
    if hp_retrieved == hashed_password:
        return 1
    else :
        return -1

def retrieve_loc_id_city(city):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "select loc_id,address from location where city='{}'".format(city)
    c.execute(query)
    result = c.fetchall()

    ans = []
    for r in result:
        temp = []
        temp.append(int(r['loc_id']))
        temp.append(str(r['address']))
        ans.append(temp)

    return ans


def retrieve_restaurant_data_nothing():
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "select name,username,res_id,loc_id,image_link from restaurant"
    c.execute(query)
    result = c.fetchall()

    res_data = {}

    if len(result) == 0:
        return res_data

    i = 0
    for r in result:
        query  = "select address from location where loc_id = {}".format(r['loc_id'])
        c.execute(query)
        
        x = c.fetchall()
        address = x[0]['address']

        temp = []
        temp.append(r['name'])
        temp.append(r['username'])
        temp.append(r['res_id'])
        temp.append(address)
        temp.append(r['image_link'])
        res_data[i] = temp
        i = i + 1

    return res_data



def retrieve_restaurant_data_only_city(city):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    loc_id_address_list = retrieve_loc_id_city(city)
    res_data = {}
    for l in loc_id_address_list:
        t1 = l[0]
        t2 = l[1]
        query = "select name,username,res_id,image_link from restaurant where loc_id = {}".format(t1)
        c.execute(query)
        result = c.fetchall()
        if len(result) == 0:
            continue
        
        i = 0
        for r in result:
            temp = []
            temp.append(r['name'])
            temp.append(r['username'])
            temp.append(r['res_id'])
            temp.append(t2)
            temp.append(r['image_link'])
            res_data[i] = temp
            i = i + 1
    return res_data

def retrieve_restaurant_data_only_cat(category):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    
    query = "select name,username,res_id,loc_id,image_link from restaurant where category = '{}'".format(category)
    c.execute(query)
    result = c.fetchall()

    res_data = {}

    if len(result) == 0:
        return res_data

    i = 0
    for r in result:
        query  = "select address from location where loc_id = {}".format(r['loc_id'])
        c.execute(query)
        
        x = c.fetchall()
        address = x[0]['address']

        temp = []
        temp.append(r['name'])
        temp.append(r['username'])
        temp.append(r['res_id'])
        temp.append(address)
        temp.append(r['image_link'])
        res_data[i] = temp
        i = i + 1

    return res_data
    

def retrieve_restaurant_data(city,category):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    loc_id_address_list = retrieve_loc_id_city(city)

    if category == "Select a category" and city == "Select a city" :
        return retrieve_restaurant_data_nothing()
    elif category == "Select a category":
        #print ""
        return retrieve_restaurant_data_only_city(city)
    
    elif city == "Select a city":
        #print ""
        return retrieve_restaurant_data_only_cat(category)
 
    #print "HERERERERERER I AM"
    #print loc_id_address_list
    res_data = {}
    for l in loc_id_address_list:
        t1 = l[0]
        t2 = l[1]
        query = "select name,username,res_id,image_link from restaurant where loc_id = {} and category = '{}'".format(t1,category)
        #print query
        c.execute(query)
        result = c.fetchall()
        if len(result) == 0:
            continue
        
        i = 0
        for r in result:
            temp = []
            temp.append(r['name'])
            temp.append(r['username'])
            temp.append(r['res_id'])
            temp.append(t2)
            temp.append(r['image_link'])
            res_data[i] = temp
            i = i + 1

        
    
    #print res_data
    
    return res_data

def retrieve_order_res(res_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select order_id, dest_address, status from orders where res_id={}".format(res_id)
    c.execute(query)
    result = c.fetchall()
    
    order_data = {}
    i = 0
    for r in result:
        temp = []
        temp.append(r['order_id'])
        temp.append(r['dest_address'])
        temp.append(r['status'])
        order_data[i] = temp
        i = i + 1

    return order_data


def retrieve_menu(res_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select name, price, food_id from menu where res_id={}".format(res_id)
    c.execute(query);
    result = c.fetchall()
    
    res_data = {}
    i = 0
    for r in result:
        temp = []
        temp.append(r['name'])
        temp.append(r['price'])
        temp.append(r['food_id'])
        res_data[i] = temp
        i = i + 1
    return res_data


def insert_menu_item(name, price, res_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "select * from menu"
    c.execute(query)
    result = c.fetchall()

    max_food_id=1
    for i in range(0, len(result)):
        if(result[i]['food_id'] > max_food_id):
            max_food_id = result[i]['food_id'];
    query = "insert into menu values({}, '{}', {}, {})".format(max_food_id+1, name, price, res_id)
    c.execute(query)


def retrieve_bill_order_id(order_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select bill from orders where order_id={}".format(order_id)
    c.execute(query)
    result = c.fetchall()
    
    return int(result[0]['bill'])

def retrieve_order_data(order_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select food.food_id as item_id, name as item_name, quantity, price from food, menu where food.order_id={} and food.food_id=menu.food_id".format(order_id)
    c.execute(query)
    result = c.fetchall()
        

    res_data = {}
    i = 0
    for r in result:
        temp = []
        temp.append(r['item_id'])
        temp.append(r['item_name'])
        temp.append(r['quantity'])
        temp.append(r['price'])
        res_data[i] = temp
        i = i + 1

    return res_data   

def set_menu(res_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select food_id, name, price from  menu where res_id={}".format(res_id)
    c.execute(query)
    result = c.fetchall()
        
    menu_data = {}
    i = 0
    for r in result:
        temp = []
        temp.append(r['food_id'])
        temp.append(r['name'])
        temp.append(r['price'])
        menu_data[i] = temp
        i = i+1
    return menu_data 




def modify_status_update(order_id, status):

    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "update orders set status = '{}' where order_id = {}".format(status, order_id)
    c.execute(query)

def remove_order(order_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "delete from orders where order_id = {}".format(order_id)
    #print query
    c.execute(query)

    query = "delete from food where order_id = {}".format(order_id)
    #print query
    c.execute(query)



def insert_order_list(order_list):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    user_id = get_g_user_id()
    res_id = get_g_res_id()
    status = "Order Placed"

    query = "select address from user where user_id={}".format(user_id)
    c.execute(query)
    result = c.fetchall()
    dest_address = result[0]['address']
    
    purchase_date = str(datetime.date.today())

    # generate bill
    bill = 0
    for o in order_list:
        query = "select price from menu where res_id={} and food_id={}".format(res_id,int(o[0]))
        c.execute(query)
        result = c.fetchall()
        price = int(result[0]['price'])
        bill = bill + (int(o[1])*price)

    
    #print "HUHUHUH"
    order_id = insert_order(status, user_id, res_id, dest_address, purchase_date, bill)
    
    for o in order_list:
        insert_food(int(o[0]), int(o[1]), order_id)

    return order_id

def insert_order(status, user_id, res_id, dest_address, purchase_date, bill):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()


    #print "hahahahahahahah"

    query = "select * from orders"
    c.execute(query)
    result = c.fetchall()
    max_order_id=1
    for i in range(0, len(result)):
        if(result[i]['order_id'] > max_order_id):
            max_order_id = result[i]['order_id'];
    #print "present = " + str(len(result))
   
    query = "insert into orders values({}, '{}', {}, {}, '{}', '{}', {})".format(max_order_id+1, status, user_id, res_id, dest_address, purchase_date, bill)
    #print query
    c.execute(query)

    return (max_order_id+1)
    
def insert_food(food_id, quantity, order_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    #print "hhhhhhhhhhhhhhhhhhhhhhhhhh"
    query = "insert into food values({}, {}, {})".format(food_id, order_id, quantity)
    
    c.execute(query)

    return 1



def retrieve_restaurant_data_from_id(res_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select * from restaurant where res_id={}".format(res_id)
    c.execute(query)
    result = c.fetchall()
    
    return result[0]



def insert_food_item(food_id, name, price):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    res_id = get_g_res_id()

    query = "insert into menu values({}, {}, {}, {})".format(food_id, quantity, order_id, res_id)
    c.execute(query)

    return 1
    
def delete_food_item(food_id, price):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    res_id = get_g_res_id()

    query = "delete from menu where food_id = {}".format(food_id)
    c.execute(query)

    return 1


def modify_res_details(res_id, resname, email_id, phone_number, start_time, end_time, category):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "update restaurant set email_id='{}', name='{}', phone_number='{}', start_time='{}', end_time='{}', category='{}' where res_id={}".format(email_id, resname, phone_number, start_time, end_time, category, res_id)
    #print query
    c.execute(query)


def delete_menu_item(food_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "delete from menu where food_id={}".format(food_id)
    c.execute(query)





def set_g_res_id(res_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "delete from g_res_id"
    c.execute(query)

    query = "insert into g_res_id values('{}')".format(res_id)
    c.execute(query)

def get_g_res_id():
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select * from g_res_id"
    c.execute(query)
    result = c.fetchall()
    return result[0]['res_id']



def set_g_res_city(city_name):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "delete from g_res_city"
    c.execute(query)

    query = "insert into g_res_city values('{}')".format(city_name)
    c.execute(query)

def get_g_res_city():
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select * from g_res_city"
    c.execute(query)
    result = c.fetchall()
    return result[0]['city_name']



def set_g_res_name(res_name):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "delete from g_res_name"
    c.execute(query)
    query = "insert into g_res_name values('{}')".format(res_name)
    c.execute(query)


def get_g_res_name():
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    
    query = "select * from g_res_name"
    c.execute(query)
    result = c.fetchall()
    return result[0]['res_name']



def set_g_res_cat(category):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "delete from g_res_cat"
    c.execute(query)
    query = "insert into g_res_cat values('{}')".format(category)
    c.execute(query)


def get_g_res_cat():
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    
    query = "select * from g_res_cat"
    c.execute(query)
    result = c.fetchall()
    return result[0]['category']






def retrieve_restaurant_rname(res_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    
    query = "select name from restaurant where res_id={}".format(res_id)
    c.execute(query)
    result = c.fetchall()
    return result[0]['name']


def set_g_user_name(user_name):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "delete from g_user_name"
    c.execute(query)
    query = "insert into g_user_name values('{}')".format(user_name)
    c.execute(query)


def get_g_user_name():
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    
    query = "select * from g_user_name"
    c.execute(query)
    result = c.fetchall()
    return result[0]['user_name']




def set_g_user_id(user_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "delete from g_user_id"
    c.execute(query)
    query = "insert into g_user_id values('{}')".format(user_id)
    c.execute(query)


def get_g_user_id():
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    
    query = "select * from g_user_id"
    c.execute(query)
    result = c.fetchall()
    return result[0]['user_id']


def set_g_order_id(order_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()

    query = "delete from g_order_id"
    c.execute(query)
    query = "insert into g_order_id values('{}')".format(order_id)
    c.execute(query)

def get_g_order_id():
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    
    query = "select * from g_order_id"
    c.execute(query)
    result = c.fetchall()
    return result[0]['order_id']



def retrieve_order_user(username):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select user_id from user where username='{}'".format(username)
    c.execute(query)
    result = c.fetchall()
    user_id=result[0]['user_id']
    
    c = db.cursor()
    query = "select order_id, name,dest_address, status from orders,restaurant where user_id={} and orders.res_id=restaurant.res_id".format(user_id)
    c.execute(query)
    result = c.fetchall()
    
    order_data = {}
    i = 0
    for r in result:
        temp = []
        temp.append(r['order_id'])
        temp.append(r['name'])
        temp.append(r['dest_address'])
        temp.append(r['status'])
        order_data[i] = temp
        i = i + 1

    return order_data
def retrieve_favourites(username):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select user_id from user where username='{}'".format(username)
    c.execute(query)
    result = c.fetchall()
    user_id=result[0]['user_id']
    
    c = db.cursor()
    query = "select distinct restaurant.name as r,menu.name as m from orders,restaurant,menu,food where user_id={} and orders.res_id=restaurant.res_id and orders.order_id=food.order_id and food.food_id=menu.food_id and orders.res_id=menu.res_id".format(user_id)
    c.execute(query)
    result = c.fetchall()
    
    order_data = {}
    i = 0
    for r in result:
        temp = []
        temp.append(r['m'])
        temp.append(r['r'])
     
        order_data[i] = temp
        i = i + 1

    return order_data


def retrieve_address_from_res_id(res_id):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    c = db.cursor()
    query = "select address from restaurant, location where restaurant.loc_id = location.loc_id and restaurant.res_id = {}".format(res_id)
    
    c.execute(query)
    result = c.fetchall()
    
    return result[0]['address']
    


def delete_user(username):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select user_id from user where username='{}'".format(username)
    c.execute(query)
    result = c.fetchall()
    if len(result) == 0:
        return
    #print "here yyy"
    user_id=result[0]['user_id']

    query = "delete from user where user_id = {}".format(user_id)
    c.execute(query)
    query = "delete from orders where user_id = {}".format(user_id)
    c.execute(query)

    return 1
def delete_res(username):
    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
    c = db.cursor()
    query = "select res_id from restaurant where username='{}'".format(username)
    c.execute(query)
    result = c.fetchall()
    if len(result) == 0:
        return
    res_id=result[0]['res_id']

    query = "delete from restaurant where res_id = {}".format(res_id)
    c.execute(query)
    query = "delete from orders where res_id = {}".format(res_id)
    c.execute(query)
    query = "delete from located_in where res_id = {}".format(res_id)
    c.execute(query)
    query = "delete from menu where res_id = {}".format(res_id)
    c.execute(query)

    return 1
def main():
    # print check_user_exists('abcd')
    # print insert_user('qqq','qqq','qqq','qqq')
    # print check_location_exists('b','a')
    pass

if __name__=="__main__":
    main()
    



 
