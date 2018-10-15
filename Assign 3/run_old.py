from flask import Flask, redirect, url_for, request, render_template
import hashlib, uuid
import sys
import re
import pymysql
sys.path.append('./py_scripts')
import insert_db

########################################################################
#---------     CHECK FUNCTIONS ----------------------------------------#


# check_sign_up_user is the data consistency check for user signup tab
def check_sign_up_user(email,password,cpassward):
    if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
        return 0

    if password != cpassward:
        return 0

    return 1

# check_sign_up_restaurant is the data consistency check for restaurant signup tab
def check_sign_up_restaurant(email,password,cpassward,phone,timings):
    if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
        return 0

    if password != cpassward:
        return 0

    for p in phone:
        x = int(p)
        if not (x >=0 and x<=9):
            return 0
    
    time = timings.split('-')
    if len(time) != 2:
        return 0
    for t in time:
        if len(t) != 5:
            return 0
        x = t.split(':')
        if len(x) != 2:
            return 0

        h = int(x[0])
        m = int(x[1])
        if h<0 or h>23 :
            return 0
        if m<0 or m>59 :
            return 0    

    return 1


###################################################################################
#---------     FLASK CODE BEGINS -------------------------------------------------#

app = Flask(__name__)

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        
        if 'submit_login_user' in request.form:
            
            uname = request.form['username']
            p = request.form['password']
            h_p = hashlib.sha224(p).hexdigest()
            
            if request.form['login_type'] == 'user':
                # login user
                match = insert_db.match_user_login(uname,h_p)
                if match == -1:
                    return redirect(url_for('login'))
                else :
                    # insert_db.set_g_res_city('Kolkata')
                    # insert_db.set_g_res_city('d')
                    insert_db.set_g_user_name(uname)

                    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
                    c = db.cursor()
                    query = "select user_id from user where username = '{}'".format(uname)
                    c.execute(query)
                    result = c.fetchall()
                    insert_db.set_g_user_id(result[0]['user_id'])
                    
                    return redirect(url_for('order'))
            else :
                # login restaurant
                match = insert_db.match_restaurant_login(uname,h_p)
                if match == -1:
                    return redirect(url_for('login'))
                else :
                    db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
                    c = db.cursor()
                    query = "select res_id,name from restaurant where username = '{}'".format(uname)
                    c.execute(query)
                    result = c.fetchall()
                    insert_db.set_g_res_id(result[0]['res_id'])
                    insert_db.set_g_res_name(result[0]['name'])
                    
                    return redirect(url_for('restaurant_home'))
        
        
        # sign up user
        if 'submit_sign_up_user' in request.form:
            check = 1
            # while True:
            username = request.form['username']
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            cpassward = request.form['cpassword']

            check = check_sign_up_user(email,password,cpassward)
            if check:
                hashed_password = hashlib.sha224(password).hexdigest()
               
                insert_db.insert_user(username,name,hashed_password,email)
                # break
                # return render_template('login.html')
            # else :
                # return render_template('login.html')


            print "reached2"
        
        # sign up restaurant
        if 'submit_sign_up_restaurant' in request.form:
            print "here"
            check = 1
            username = request.form['username']
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            cpassward = request.form['cpassword']
            phone = request.form['phoneno']
            timings = request.form['timings']
            address = request.form['address']
            city = request.form['city']
            category = request.form['category']
            # check = check_sign_up_restaurant(email,password,cpassward,phone,timings)
            print "check = " + str(check)
            if check:
                timings = timings.split('-')
                start_time = timings[0]
                end_time = timings[1]
                hashed_password = hashlib.sha224(password).hexdigest()
                print "here0"
                insert_db.insert_restaurant(username,name,hashed_password,email,phone,start_time,end_time,category,address,city)
                print "reached3"
    
    return render_template('login.html')
    

@app.route('/order',methods = ['POST','GET'])
def order():
    city_name = insert_db.get_g_res_city()
    res_data = insert_db.retrieve_restaurant_data(city_name)
    user_name=insert_db.get_g_user_name()
    orders=insert_db.retrieve_order_user(user_name);
    favourites=insert_db.retrieve_favourites(user_name);
    if request.method == 'POST':
        for i,d in res_data.iteritems():
            temp = str(i)
            if temp in request.form:
                insert_db.set_g_res_name(str(d[0]))
                insert_db.set_g_res_id(str(d[3]))
                # print i
                insert_db.set_g_user_name(user_name)
                return redirect(url_for('menu'))
        
        for i,d in orders.iteritems():
            temp = "cancel"+str(d[0])
            if temp in request.form:
                insert_db.remove_order(d[0])
                break
                
        
        if "logout" in request.form:
            return redirect(url_for('login'))

            
    return render_template('order.html',restaurant=res_data,username=user_name,orders=orders,favourites=favourites)
    
@app.route('/menu',methods = ['POST','GET'])
def menu():
    res_name = insert_db.get_g_res_name()
    res_id = insert_db.get_g_res_id()
    menu_data = insert_db.set_menu(res_id)
    user_name=insert_db.get_g_user_name()
    if request.method == 'POST':
        if "place_order" in request.form:
            order_list = []
            for i,d in menu_data.iteritems():
                temp = []
                check_string = "check"+str(i)
                quan_string = "quan"+str(i)
                if request.form.get(check_string):
                    temp.append(d[0])
                    temp.append(int(request.form[quan_string]))
                    order_list.append(temp)

                    # print request.form[quan_string]
            order_id = insert_db.insert_order_list(order_list)
            insert_db.set_g_order_id(order_id)
            return redirect(url_for('bill'))

            
        if "logout" in request.form:
            return redirect(url_for('login'))

    return render_template('menu.html',menu_data=menu_data,username=user_name)

@app.route('/restaurant_home',methods = ['POST','GET'])
def restaurant_home():
    res_name = insert_db.get_g_res_name()
    res_id = insert_db.get_g_res_id()
    
    res_data = insert_db.retrieve_restaurant_data_from_id(res_id)    
    order_data = insert_db.retrieve_order_res(res_id) 
    menu_data = insert_db.retrieve_menu(res_id)
    res_rname=insert_db.retrieve_restaurant_rname(res_id);

    if request.method == 'POST':
        if 'add_item' in request.form:
            insert_db.insert_menu_item(request.form['item_name'], request.form['price'], res_id)
            return redirect(url_for('restaurant_home'))
        
        if "logout" in request.form:
            return redirect(url_for('login'))
        if "save_changes" in request.form:
            resname = request.form['res_name']
            print resname
            email = request.form['email']
            phone = request.form['phone_no']
            start = request.form['start']
            end = request.form['end']
            category = request.form['category']
            insert_db.modify_res_details(res_id, resname, email, phone, start, end, category)
            return redirect(url_for('restaurant_home'))

        for i,d in menu_data.iteritems():
            temp = "delete_item" + str(d[2])
            if temp in request.form:
                insert_db.delete_menu_item(d[2])
                return redirect(url_for('restaurant_home'))
            
        for i, d in order_data.iteritems(): 
            name = "name" + str(d[0])
            temp1 = "save_item" + str(d[0]) 
            temp2 = "cancel_item" + str(d[0])
            if temp1 in request.form:
                insert_db.modify_status_update(d[0], request.form[name])                
                return redirect(url_for('restaurant_home'))
                
            if temp2 in request.form:
                insert_db.remove_order(d[0])
                return redirect(url_for('restaurant_home'))
    if request.method == 'GET':
        pass
    
    return render_template('restaurant_home.html',res_name=res_rname,order_data=order_data,menu_data=menu_data, address = 'blank_address', phone_number = res_data['phone_number'], email_id = res_data['email_id'], start = res_data['start_time'], end = res_data['end_time'], category=res_data['category'])

@app.route('/bill',methods = ['POST','GET'])
def bill():
    order_id = insert_db.get_g_order_id()
    bill_data = insert_db.retrieve_order_data(order_id)
    total = insert_db.retrieve_bill_order_id(order_id)
    return render_template('bill.html',order_id=order_id,bill=bill_data,total=total)


if __name__ == '__main__':
   app.run(host='127.0.0.1',port=5000,debug = True)	