import csv

with open('users.csv',mode='r') as file:  #read and store users.csv to user_data
    csv_reader=csv.DictReader(file)
    user_data=[]
    for row in csv_reader:
        user_data.append(row)
    file.close()
with open('inventory.csv',mode='r') as file: #read and store inventory.csv to product_data
    csv_reader=csv.DictReader(file)
    product_data=[]
    for row in csv_reader:
        product_data.append(row)
    file.close()
for data in product_data:
    print(data)

with open('transaction.csv',mode='r') as file:  #read and store transaction.csv to product_data
    csv_reader=csv.DictReader(file)
    transaction_data=[]
    for row in csv_reader:
        transaction_data.append(row)
    file.close()

def validate(p_id): # validate unique product id 
    p_temp=False
    for product in product_data:
        if product['product_id'] != p_id:
            p_temp=True
    return p_temp

def product_validate(id,quantity): #validate for id and quantity available in inventory
    p_temp=False
    for product in product_data:
        if product['product_id'] == id:
            if int(product['quantity']) >= int(quantity): 
                p_temp=True
                return p_temp
            else:
                print("there is no enough quantity to sold")
                return "there is no enough quantity to sold"
        else:
            print("product id not exist in inventory")
            return "product id not exist in inventory" 
    return p_temp

class Admin:
    # def __init__():
    #     pass
    def add_product(self): #add product to inventory
        while True:
            id=input("add product id: ")
            a=validate(id) #call validate function for unique product id
            if a:
                name=input("add product name: ")
                quantity=int(input("add product quantity: "))
                price=int(input("enter product price: "))
                dict={}
                dict['id']=id
                dict['name']=name
                dict['quantity']=quantity
                dict['price']=price
                with open('users.csv',mode='a') as file:  #write data to inventory.csv
                    writer=csv.DictWriter(file,fieldnames=['id','name','quantity','price'])
                    writer.writerow(dict)
                    file.close()
                    print(dict)
                exit()
                return True
            else:
                print(f"id:{id} is already in inventory.use different id")
    def add_employee(self): #add new employee to user.csv
        e_name=input("to add employee enter employee name: ")
        e_password=input("add employee password: ")
        e_role=input("add employee role: ")
        dict={}
        dict['username']=e_name
        dict['password']=e_password
        dict['role']=e_role
        with open('users.csv',mode='a') as file:
            writer=csv.DictWriter(file,fieldnames=['username','password','role'])
            writer.writerow(dict)
            file.close()
        return True
    def view_transaction(self): #show all the data from transaction.csv file
        print("employee_username | producct_id | quantity_sold | total_amount ")
        for i in transaction_data:
            if i != None:
                print (f"{i['employee_username']} | {i['producct_id']} | {i['quantity_sold']} | {i['total_amount']}")
            else:
                print("there is no transaction history to show")
    def update_product_stock(self): #update stock of perticular product based on id
        id=input("enter id to update product")
        quantity=int(input("enter quntity that you want to add:"))

        product_list=[]
        for product in product_data:       
            if(product['product_id']==id): #update data of perticular product
                product_quantity=int(product['quantity'])+quantity
                row={'product_id':product['product_id'] ,
                    'product_name':product['product_name'],
                    'quantity':product_quantity,
                    'price':product['price'],
                }
            else:
                product_quantity=int(product[quantity])+quantity
                row={'product_id':product['product_id'] ,
                    'product_name':product['product_name'],
                    'quantity':product_quantity,
                    'price':product['price'],}

            product_list.append(row)

            with open('inventory.csv',mode='w') as file:
                writer=csv.DictWriter(file,delimiter=',',fieldnames=['product_id','product_name','quantity','price'])
                writer.writeheader()
                writer.writerows(product_list)

class Employee:
    username=""
    def __init__(self,username):
        self.username=username  
    def login(self,username,password): #authenticate user with username,password
        temp_pass=False
        temp_username=False
        for user in user_data:
            if username==user['username']:
                if password==user['password']:
                    print('login success')
                    return True
                else:
                    return("Wrong Password. Please enter the correct password.")
            else:
                return("plese ask administration for registration")
    def view_product_list(self): #display all product from inventory
        print("product_id | producct_name | quantity | price ")
        for i in product_data:
            if i != None:
                print (f"{i['product_id']} | {i['product_name']} | {i['quantity']} | {i['price']}")
            else:
                print("there is no transaction history to show")
    def sell_product(self): #sell product based on id,quantity
        while True:
            id=input("id of product: ")
            quantity=int(input("quantity of product: "))
            value_validate=product_validate(id,quantity)
            if value_validate==True:
                for product in product_data:
                    if product['product_id'] == id:
                        total_amount=quantity*int(product['price'])
                        break
                    else:
                        print("can't find product")
                dict={}
                dict['employee_username']=username
                dict['producct_id']=id
                dict['quantity_sold']=quantity
                dict['total_amount']=total_amount
                with open('transaction.csv',mode='a') as file:
                    writer=csv.DictWriter(file,fieldnames=['employee_username','producct_id','quantity_sold','total_amount'])
                    writer.writerow(dict)
                    file.close()
                    print(dict)
                #update quantity of product in inventory based on sales data
                update_quantity_list=[]
                for product in product_data:       
                    if(product['product_id']==id):
                        new_quantity=int(product['quantity'])-quantity
                        row={'product_id':product['product_id'] ,
                            'product_name':product['product_name'],
                            'quantity':new_quantity,
                            'price':product['price'],
                        }
                    else:
                        product_quantity=int(product[quantity])+quantity
                        row={'product_id':product['product_id'] ,
                            'product_name':product['product_name'],
                            'quantity':product_quantity,
                            'price':product['price'],}

                    update_quantity_list.append(row)

                    with open('inventory.csv',mode='w') as file:
                        writer=csv.DictWriter(file,delimiter=',',fieldnames=['product_id','product_name','quantity','price'])
                        writer.writeheader()
                        writer.writerows(update_quantity_list)
                    break
                else:
                    print(value_validate)
    def view_transactions(self): #diplay all the sales made by user
        total_sale=0
        for data in transaction_data:
            if(data['employee_username']==username):
                total_sale=total_sale+int(data['total_amount'])
            print(f"{username},your total sale:{total_sale}")

#create menu for user 
while True:
    print("----------------------")
    print("select the role:")
    print("1.ADMIN")
    print("2.EMPLOYEE")
    print("3.exit")
    print("----------------------")
    role=int(input("enter your choice:"))
    if(role==1):
        #authenticate administrator
        username=input("enter username: ")
        password=input("enter password: ")
        if(username == 'admin' and password == 'admin'):
            while True:

                print("----------------------")
                print("Admin functionality: \n 1.Add new Product\n 2.Update product stock \n 3.Add new Employee \n 4.View transaction \n 5.log out" )
                print("----------------------")
                admin_choice=int(input("select what you want to do:"))
                object_admin=Admin()
                match admin_choice:  #select functionality based on admin choice
                    case 1:
                        print("Add new product")
                        if object_admin.add_product(): #call add product from admin class
                            print("product added sucsessfully")
                        else:
                            print("oops!!! something went wrong")
                    case 2:
                        print("Update product stock")
                        object_admin.upate_product_stock() #call update product stock from admin class
                    case 3:
                        print("Add new Employee")
                        if object_admin.add_employee(): #call add employee methon
                            print("employee added sucsessfully")
                        else:
                            print("oops!!! something went wrong")
                    case 4:
                        print("View transaction") #call view transaction methon
                        object_admin.view_transaction()
                    case 5:
                        print("log out")  #log out the existing user
                        break
                    case _:
                        print("invalid choise")
        else: 
            print("wrong username or password")
    elif (role==2):
        username=input("enter user name: ")
        password=input("enter password: ")
        value_login=object_employee.login(username,password) #call login method to authenticate user
        if value_login==True:
            while True:
                print("log in sucsess")
                print("----------------------")
                print("User functionality: \n 1.View Product list \n 2.Sell a product and Store transaction details \n 3.View Personal Sales Summary \n 4.log out" )
                print("----------------------")
                user_choice=int(input("select what you want to do:"))
                object_employee=Employee(username)
                match user_choice: #select functionality based on user choice
                        case 1:
                            print("View Product list")
                            object_employee.view_product_list()
                        case 2:
                            print("Sell a product and store transaction")
                            object_employee.sell_product()
                        case 3:
                            print("View Personal Sales Summary")
                            object_employee.view_transactions()  
                        case 4:
                            print("log out")
                            break
                        case _:
                            print("invalid choise")
        else:
            print(value_login)
    elif (role==3):
        exit() #make exit from infinite loop
    else:
        print("enter valid choice.")
