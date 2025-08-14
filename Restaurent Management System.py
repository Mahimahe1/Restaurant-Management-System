import mysql.connector as db
import matplotlib.pyplot as p 
con=db.connect(user="root",password="Mahi2002@",host="localhost",database="admin")
cur=con.cursor(buffered=True)


def showmenu():
    cur.execute("select item_id,item_name,price,category from menu where is_active=%s",[True])
    data=cur.fetchall()
    print("-"*60)
    print(f"{'Item id':^15} {'Item-Name':^20} ₹{'Price':^10} {'Categeory':^10}")
    print("~"*60)
    for i in data:
        item_id=i[0]
        item_name=i[1]
        price=i[2]
        categeory=i[3]
        print(f" {item_id :<15} {item_name:<20} {price:<10} {categeory:<10}")


def userarea():
    def load_data():
        cur.execute("select * from userdetails")
        return cur.fetchall()

    def register():
        if issignup():
            con.commit()
            print("Succesfully created\nenter your login creditionals")
            data=load_data()
            return login()
        
        
    def login():
        data = load_data()  
        user_id = None  

        while True:
            username = input("Enter username: ")
            if not username:
                print("Username cannot be empty. Please try again.")
                continue
            for match in data:
                if match[1] == username:  
                    user_id = match[0]    
                    break
        

            else:
                print("Invalid username! Try again.")
                while True:
                    choice = input("Do you want to:\n1. Try logging in again\n2. Go to signup\n3. Exit\nSelect option: ")
                    if choice=="1":
                        return login()
                        
                    elif choice == '2':
                        return register()  
                    elif choice == '3':
                        print("Exiting login...")
                        return None  
                    else:
                        print("Invalid option..please check .")
                        continue
                    
            break  

        while True:
            password = input("Enter phone_number: ")  
            for match in data:
                if match[1] == username and match[2] == password:
                    print("                 ........Logging in.......")
                    return user_id  

            
            print("Invalid phone number! Try again.")
            choice = input("Options:\n1. Retry password\n2. Exit login\nSelect: ")
            if choice == '2':
                print("          ......Exiting login......")
                return None  # User can exit login if they wish kada
            

    def issignup():
        newusername = input("Enter New username: ")
        while True:
            newpassword = input("Enter new phone_number: ")

            if not newpassword.isdigit():
                print("Phone number must contain only digits. Try again.")
                continue 
            if len(newpassword) != 10:
                print("Phone number must be exactly 10 digits. Try again.")
                continue

            if int(newpassword[0]) < 6:
                print("Phone number must start with a digit 6 or above. Try again.")
                continue

            data = load_data()
            for match in data:
                if match[1] == newusername and match[2] == newpassword:
                    print("User already exists. Please login instead.")
                    login()
                    return False

            cur.execute("INSERT INTO userdetails(name, phn_num) VALUES (%s, %s)", [newusername, newpassword])
            con.commit()
            return True



    print("             ~~~~  Welcome to ANDHRA RESTAURENT~~")
    print("1.login\n2.signup")
    def log():
        n=input("select option:")
        if n=="1":
            return login()
            
        elif n=="2":
            print("Create your new account:")
            if issignup():
                con.commit()
                print("Succesfully created\nenter your login creditionals")
                data=load_data()
                return login()
        else:
            print("Please select valid option")
            return log()

    user_id=log()   # returns the userid


    print("                              ....WELCOME....   ")

        
    def order(user_id):
        showmenu()
        print("""Would you like to add.....
                        1.yes
                        2.No""")
        while True:
            n=input("Choose one to Proceed:")
            if n=="1":
                item_id=input("Enter the item id you want to add:")
                if not item_id.isdigit():
                    print("enter valid item id")
                    order(user_id)
                cur.execute("select item_id  from menu where item_id=%s",[item_id])
                data=cur.fetchone()
                if data:
                    
                    def count(user_id):
                        quantity=input("enter quantity you want:")
                        if not quantity.isdigit():
                            print("Valid quantity")
                            count(user_id)
                        
                        
                        
                        if quantity>"0":
                            cur.execute("insert into cartitems(user_id,item_id,quantity) values(%s,%s,%s)",[user_id,item_id,quantity])
                            con.commit()
                            print("Item added to cart")
                            userblock(user_id)
                        else:
                            print("Enter quantity greater than 1")
                            count(user_id)
                    count(user_id)   
                else:
                    print("Item not available")
                    userblock(user_id)
            elif n=="2":
                userblock(user_id)
            else:
                print("Invalid option...")


    def modifyconfirm(user_id):
        choice=input("confirm!!-")
        if choice=="1":
            dele=input("enter item id you want to delete:")
            cur.execute("select count(*) from cartitems where item_id=%s and user_id=%s",[dele,user_id])
            data=cur.fetchone()
            
            if data[0]>0:
                cur.execute("delete from cartitems where item_id=%s and user_id=%s",[dele,user_id])
                con.commit()
                print("Item deleted successfully..")
                userblock(user_id)


            else:
                
                print("item not available in cart\\would you like to add new items??")
                
                print("1.yes proceed\n2.no stay()\n3.Main menu")
                while True:
                    choice=int(input("choose to "))
                    if choice==1:
                        order(user_id)
                    elif choice==2:
                        modify(user_id)
                    elif choice==3:
                        userblock(user_id)
                    else:
                        print("Invalid Option")
                        continue
        elif choice=="2":
            userblock(user_id)
        else:
            print("Invalid input")
            
            modifyconfirm(user_id)

    def modify(user_id): # argument to get the return value
        cur.execute("select c.user_id,c.item_id,m.item_name,c.quantity from cartitems c join menu m on c.item_id=m.item_id where user_id=%s",[user_id])
        data=cur.fetchall()
        print(" "*20,"YOUR CART....")
        print('-'*50)
        print(f"{'item_id':^10}{'item_name':^10}{'quantity':^10}")
        print('-'*50)
        for i in data:
            id=i[1]
            name=i[2]
            quantity=i[3]
            print(f"{id:^10}{name:^10}{quantity:^10}")
        print(" "*10,"select the items above to modify..")

        print("would you like to modify...\n1.yes\n2.No")
        
        modifyconfirm(user_id)
        

    def billing(user_id): #billing
        print("Generating bill...\n")
        cur.execute("select m.item_id, m.item_name, m.price, c.quantity  from cartitems c inner join menu m on c.item_id = m.item_id where c.user_id =%s",[user_id])
        items=cur.fetchall()
                        #select and fetch to see
        if not  items:
            print("your cart is empty")
            userblock(user_id)
        
        #calculate and show
        total=0
        print('Bill')
        print(f"Item{" "*16} Price{" "*5} Quantity{" "*5} Subtotal{" "*10} ")
        print("~"*50)
        
        for item in items:
            Item=item[1]
            price=item[2]
            quantity=item[3]
            subtotal=price*quantity
            
            total=total+subtotal
            print(f"{Item:<20} Rs{price:<10} {quantity:<10} {subtotal:<10}")

        Gst=total*0.1
        total=total+Gst
        print("~" * 50)
        print(f"{'Gst':<42} +  Rs{Gst}")
        print(f"{'Total':<42} Rs{total}")
        print("-" * 50)
        print("would you like to checkout\n1.yes\n2.No\n")
        
        confirm=input("Choose your option:")
        if confirm=="1":
            cur.execute("insert into orders(user_id,total) values(%s,%s) ",[user_id,total])  #inserting data into bill form
            con.commit()
            id=cur.lastrowid
            
            for item in items:
                Item=item[0]
                price=item[2]
                quantity=item[3]   # inserting data like to each order item
                cur.execute("insert into bill_details(order_id,item_id,quantity,price) values(%s,%s,%s,%s)",[id,Item,quantity,price])
                con.commit()

            cur.execute("delete from cartitems where user_id=%s",[user_id])
            con.commit()
            print("Check out Complete!!!!  ")
            userblock(user_id)
        elif confirm=="2":
            print("Check out Cancelled... Try Again")
            userblock(user_id)
        else:
            print("please select yes or No ")
            billing(user_id)


    def userblock(user_id):
        print("""  
                   1.Add items
                   2.modify cart
                   3.checkout
                   4.menu
                   5.exit""")
        choose=int(input("Choose one Option to get:"))
        if choose==1:
            print()
            print()
            print('You choose to add to cart option!')
            order(user_id)
        elif choose==2:
            print()
            modify(user_id) 
        elif choose==3:
            print()
            billing(user_id) 
        elif choose==4:
            print()
            showmenu()
            userblock(user_id)
        elif choose==5:
            print("Exiting...")
            local()

        else:
            print("Invalid select... Try again")


    if user_id:
        userblock(user_id)
    else:
        print("login failed")



def Adminarea():
    def load_data():
        cur.execute("select * from userlogin")
        return cur.fetchall()


    def login():
        data=load_data()
        while True:
            userid=input("Enter adminid: ")
            if not userid.isalnum():
                print("Invalid user input....")
                continue

            for match in data:
                if str(match[0])==userid:
                    userid=True

                    while True:
                        password=input("Enter password: ")
                        if match[1]==password:
                            print(" "*10,"Logging in...")
                            return
                        else:
                            print("INvalid password.. Try again")
                    
            else:
            
                print("Admin not Found....Try Again")

    def countitems():
        while True:
            count=input("enter item you want to add:")
            if not count.replace("-","").replace(" ","").isalpha():
                print("enter valid item_name")
                continue

            cur.execute("select count(*) from menu where item_name=%s and is_active=%s",[count,True])
            itemcount=cur.fetchone()

            return count,itemcount[0]>0
        

    def deleteitems():
        while True:
            count=input("enter item id  you want to delete/modify:")
            if not count.isdigit():
                print("enter valid item_id")
                continue

            cur.execute("select count(*) from menu where item_id=%s and is_active=%s",[count,True])
            itemcount=cur.fetchone()

            if itemcount[0]>0:
                return count, True 
            else:
                print("Item is not available...Choose on Menu")


    def modify_menu():
        count,exists=deleteitems()
        if exists:
            print("""           what you want to modify--
                                    1.ITEM NAME
                                    2.PRICE
                                    3.CATEGORY
                                    4.ALL
                                    5.MAIN MENU..""")
            while True:
                choose=input("Choose your Option::")
                if choose=="1":
                    while True:
                        
                        item_name=input("Enter new item_name:")
                        if item_name.replace(" ","").replace(",","").isalpha():
                            cur.execute("select item_name from menu where item_name=%s",[item_name])

                            data=cur.fetchone()
                            if data:
                                print("Item is already existed ...")
                                continue
                            
                            cur.execute("update menu set item_name=%s where item_id=%s",[item_name,count])
                            con.commit()
                            break
                        else:
                            print("Enter Valid item name..")
                            continue

                elif choose=="2":
                    new_price=input("Enter new price:")
                    if not new_price.isdigit() and int(new_price)<0:
                        print("Enter valid NewPrice")
                    cur.execute("update menu set price=%s where item_id=%s",[new_price,count])
                    con.commit()

                elif choose=="3":
                    new_category=input("Enter new category:")
                    if not new_category.replace(" ","").replace("-","").isalpha():
                        print("Please Enter Valid category name")
                    cur.execute("update menu set category=%s where item_id=%s",[new_category,count])
                    con.commit()

                elif choose=="4":
                    while True:
                        item_name=input("Enter new item_name:")
                        if item_name.replace(" ","").replace(",","").isalpha():
                            cur.execute("select item_name from menu where item_name=%s",[item_name])
                            data=cur.fetchone()
                            if data:
                                print("Item is already existed ...")
                            else:
                                break
                        else:
                            print("Enter valif item name..")
                            continue
                        
                    while True:
                        new_price=input("Enter new price:")
                        if not new_price.isdigit() or int(new_price)<=0:
                            print("Enter valid NewPrice")
                        else:
                            break

                    while True:
                        new_category=input("Enter new category:")
                        if  not new_category.replace(" ","").replace("-","").isalpha():
                            print("Please Enter Valid category name")
                        else:
                            break
                    cur.execute("update menu set item_name=%s,price=%s,category=%s where item_id=%s",[item_name,new_price,new_category,count])
                    con.commit()

                elif choose=="5":
                    print("Main Menu...")
                    return userfunction()
                else:
                    print("Invalid Choice")
                    continue
                    
                print("Modification Complete..")
                return userfunction()
            
    print(" "*30,"Welcome to the ANDHRA RESTAURENT ")

    print("Please Login via creditonals")

    login()

    def userfunction():
        print("""           
                            1.Add Menu
                            2.Delete Menu
                            3.Modify Menu
                            4.View All Orders
                            5.Day Wise Profit
                            6.view Menu
                            7.Exitt""")
        option=input("choose your option:")
        
        if option=="1":
            showmenu()
            count,exists=countitems()
            if exists:
                print("Item is already existed::\nwould like to modify or update kindly choose 2:")
                userfunction()

            else:
                while True:
                    price=input("Add price:")
                    if price.isdigit() and int(price)>0:
                        while True:
                            category=input("select category,veg/nonveg/starters::")
                            if not category.replace(" ","").replace("-","").isalpha():
                                print("Please Enter Valid category name")
                                continue
                            cur.execute("insert into menu(item_name,price,category) values(%s,%s,%s)",[count,price,category])
                            con.commit()
                            print("Item Added Succesfully....")
                            userfunction()
                    else:
                        print("Invalid Price ")
    
        elif option=="2":
            showmenu()
            count,exists=deleteitems()
            if exists:
                
                #cur.execute("delete from bill_details where item_id = %s", [count])
                cur.execute("update menu set is_active=False where item_id=%s",[count])
                con.commit()
                print("Item is marked as Inactive")
                #cur.execute("delete from menu where item_id=%s",[count])
                #con.commit()
                #print("Item deleted Succesfully")
                userfunction()

        elif option=="3":
            showmenu()
            modify_menu()

        elif option=="4":
            cur.execute("""select o.order_id, d.name,o.total , date(o.order_date) ,group_concat(concat(m.item_name,"x",quantity) order by b.item_id separator ",") from orders o join bill_details b on o.order_id=b.order_id  join menu m on b.item_id=m.item_id join userdetails d on o.user_id=d.user_id group by o.order_id,o.total,date(o.order_date)""")
            data=cur.fetchall()
            print(" "*30,'All Orders')
            print(f"orderid{" "*5} username{" "*7} item/quantity{" "*20} Total{" "*10} OrderDate{" "*14} ")
            print("-"*100)
            from datetime import datetime 
            import textwrap 
            if not data:
                print("No Orders Yet")
            else:
                for details in data:
                    
                    order_id=details[0]
                    user_id=details[1]
                    item_id=details[2]
                    item_name=details[3].strftime("%d-%m-%Y ")
                    wrapped=details[4]
                    quantity= textwrap.wrap(wrapped, width=40)

                
                    print(f"{order_id:<10}   {user_id:<15} {quantity[0]:<30}  {item_id:<20} {item_name:<30} ")#{quantity:<11} {total:<10} {order_date:<30} ")
                    for line in quantity[1:]:
                        print(f"{'':<28} {line:<35}")
                    print("~"*100)    
                        
                
                    
            userfunction()
        
        
        elif option=="5":
            from datetime import datetime  
            
            cur.execute("select bill_date,round(sum(quantity*price)*0.15) as profit from bill_details group by bill_date;")
            profit=cur.fetchall()
            print("DAY WISE PROFITS")
            print()
            print("~"*30)
            print(f"  DATE{" "*10} PROFIT{" "*5}")
            print("-"*30)
            x_data=[]
            y_data=[]
            if profit:
                for i in profit:
                    date=i[0].strftime("%Y-%m-%d ")
                    profit=i[1]
                    print(f"{date:<17} Rs{profit:<10}")
                    x_data=x_data+[date]
                    y_data=y_data+[int(profit)]
                print("~"*30)  
                print(y_data)
                p.plot(x_data,y_data)
                p.xlabel("Date")
                p.ylabel("Profit RS")
                p.title("Day Wise Profit")
                p.show()
                
            else:
                print("No Orders Yet")

            userfunction()

        elif option=="6":
            showmenu()
            userfunction()
            
        elif option=="7":
            print("\033[92mlogging out....\033[0m")
            local()
            
        else:
            print("Invalid option.please try again")
            userfunction()

    userfunction()



def local():
    print("""Hi... Welcome To My Restaurent...
                Please login
                1.ADMIN
                2.USER
                3.Exit""")
    while True:
        choo=input("CHoose your Option:")
        if choo=="1":
            Adminarea()
            break
        elif choo=="2":
            userarea()
            break
        elif choo=="3":
            exit()
        else: 
            print("INVALID Option ....Try Again")
            continue

local()

con.commit()
cur.close()

con.close()
