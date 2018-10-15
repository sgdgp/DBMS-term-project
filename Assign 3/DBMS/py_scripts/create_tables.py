import pymysql

db = pymysql.connect("10.5.18.101","14CS10061","btech14","14CS10061",cursorclass=pymysql.cursors.DictCursor )
c = db.cursor()

c.execute('drop table if exists user')
c.execute('drop table if exists sys_admin')
c.execute('drop table if exists restaurant')
c.execute('drop table if exists orders')
c.execute('drop table if exists food')
c.execute('drop table if exists menu')
c.execute('drop table if exists location')
c.execute('drop table if exists located_in')



c.execute('create table user(\
user_id int,\
username varchar(20),\
name varchar(20),\
hashed_password varchar(100),\
email_id varchar(50),\
address varchar(100),\
primary key(user_id)\
)')
c.execute('create table sys_admin(username varchar(20),hashed_password varchar(100))')


c.execute('create table restaurant(\
res_id int,\
username varchar(100),\
name varchar(50),\
hashed_password varchar(100),\
email_id varchar(50),\
phone_number varchar(13),\
loc_id int,\
start_time varchar(5),\
end_time varchar(5),\
category varchar(100),\
image_link varchar(300),\
primary key(res_id)\
)')

c.execute('create table orders(\
order_id int,\
status varchar(50),\
user_id int,\
res_id int,\
dest_address varchar(100),\
purchase_date varchar(10),\
bill int,\
primary key(order_id)\
)')

    
c.execute('create table food(\
food_id int,\
order_id int,\
quantity int,\
primary key (food_id)\
)')


c.execute('create table menu(\
food_id int,\
name varchar(50),\
price int,\
res_id int,\
primary key(food_id,order_id)\
)')

c.execute('create table location(\
loc_id int,\
address varchar(200),\
city varchar(100),\
primary key(loc_id)\
)')

c.execute('create table located_in(\
res_id int,\
loc_id int\
)')




