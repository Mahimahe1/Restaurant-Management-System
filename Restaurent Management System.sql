create database admin;
use admin;

create table userlogin(userid bigint(200) primary key not null,password varchar(200) not null);
select * from userlogin;

insert into userlogin values(9988771,"Mahi2002@"),(9988661,"Mister33"),(9988551,"Kims"),(9988441,"mister"),(9988221,"kolkol");
create table menu(item_id int primary key not null,item_name varchar(200),price bigint(200),category varchar(100));
select * from menu;

alter table menu add column is_active boolean default True;


delete from  menu where item_id=18;
insert into menu values(1,'Biryani',300,'non-veg'),(2,'bajjis',50,'veg'),(3,'chicken-65',100,'starters'),(4,'Thandoori',500,'non-veg'),
						(5,'fried-rice',100,'veg'),(6,'Aloo-fry',80,'veg'),(7,'chicken-kheema',150,'non-veg'),(8,'kheema',100,'veg'),
                        (9,'phav-bhaji',70,'veg'),(10,'mutton-korma',300,'non-veg'),(11,'sangati',100,'veg'),(12,'chicken-lollipop',200,'non-veg');
alter table menu modify item_id int  auto_increment;

create table userdetails(user_id int auto_increment primary key,name varchar(150),phn_num varchar(150) );
insert into userdetails values(1,'Srinivas',9022341201),(2,'Ram',9087654321),(3,'akthar',8097654321),(4,'jessie',6054321901),
								(5,'seetha',8201348759),(6,'sravani',9008765432),(7,'sowmya',7071234509);
select*from userdetails;
                                
create table cartitems(cart_id int auto_increment primary key,user_id int,item_id int,quantity int default 1,
					added_on timestamp default current_timestamp,
					foreign key (user_id) references userdetails(user_id), foreign key (item_id) references menu(item_id));

select * from cartitems;
delete from cartitems where cart_id in (37,38);
alter table cartitems modify column user_id int not null;
delete from cartitems where cart_id in (29,30);
alter table cartitems add check(quantity>0);

create table orders(order_id int primary key auto_increment, user_id int, total numeric(10,2), order_date timestamp default current_timestamp);


select * from orders;
select date(order_date),order_id from orders group by date(order_date),order_id;

create table bill_details(bill_id int auto_increment primary key,order_id int,item_id int,quantity int, 
price numeric(10,2),foreign key (order_id) references orders(order_id),foreign key (item_id) references menu(item_id));



select*from bill_details;
alter table bill_details add bill_date date;
alter table bill_details modify column bill_date date  default(curdate());
update bill_details set bill_date="2023-07-12" where bill_id in (1,2,3,4,5,6);
select order_id,round(sum(quantity)*sum(price)*0.15) as profit from bill_details group by order_id;