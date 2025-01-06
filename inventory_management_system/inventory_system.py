import csv
import re

def read_csv(filename):
    try:
        with open(filename, mode='r') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []
def write_to_csv(filename, data, fieldnames):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
def append_to_csv(filename, data, fieldnames):
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerows(data)

#validation function
def validate_field(field):
    return field.isnumeric()

def validdate_user(username):
    for user in user_data:
        if(user['username']==username):
            return False
    return True

def validate_product_id(p_id, product_data):
    return all(product['product_id'] != p_id for product in product_data)

def validate_product_quantity(id, quantity, product_data):
    for product in product_data:
        if product['product_id'] == id:
            if int(product['quantity']) >= int(quantity):
                return True
            return "Not enough quantity available."
    return "Product ID does not exist in inventory."

def validate_username(username):
    pattern = r"^[a-zA-Z0-9]{5,20}$"
    return bool(re.match(pattern, username))

def validate_password(password):
    pattern = r"(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$"
    return bool(re.match(pattern, password))

# Admin class
class Admin:
    def __init__(self, product_data, transaction_data):
        self.product_data = product_data
        self.transaction_data = transaction_data

    def add_product(self):
        id = input("Add product ID: ")
        if not validate_field(id):
            print("enter numeric value in field")
            return
        if not validate_product_id(id, self.product_data):
            print(f"Product ID {id} already exists. Use a different ID.")
            return

        name = input("Add product name: ")
        quantity = input("Add product quantity: ")
        if validate_field(quantity):
            price = input("Enter product price: ")
            if validate_field(price):
                new_product = {
                    'product_id': id,
                    'product_name': name,
                    'quantity': quantity,
                    'price': price
                }
                self.product_data.append(new_product)
                write_to_csv('inventory.csv', self.product_data, ['product_id', 'product_name', 'quantity', 'price'])
                print("Product added successfully.")
            else:
                print("price must be numeric values.")
        else:
            print("Quantity must be numeric values.")

    def add_employee(self):
        username = input("Enter employee username (5-20 alphanumeric characters,start with alphabet): ")
        if validate_username(username):
            if validdate_user(username):
                password = input("Enter password (min 8 chars,1 Uppercase letter,1 number: ")
                # if print(validate_password(password)):
                if validate_password(password):
                    role = input("Enter employee role (clerk/manager/assistant):")
                    new_employee = {
                        'username': username,
                        'password': password,
                        'role': role
                    }
                    append_to_csv('users.csv', [new_employee], ['username', 'password', 'role'])
                    print("Employee added successfully.")

                else:
                    print("invalid password format")
            else:
                print("username alreay exist.You can't add same user twice")
        else:
            print("Invalid username format.")

    def view_transaction(self):
        if not self.transaction_data:
            print("No transaction history to show.")
            return

        print("employee_username | product_id | quantity_sold | total_amount")
        for transaction in self.transaction_data:
            print(f"{transaction['employee_username']} | {transaction['product_id']} | {transaction['quantity_sold']} | {transaction['total_amount']}")

    def update_product_stock(self):
        id = input("Enter product ID to update: ")
        if not validate_field(id):
            print("id must be numeric.")
            return
        quantity = input("Enter quantity to add: ")
        if not validate_field(quantity):
            print("Quantity must be numeric.")
            return

        for product in self.product_data:
            if product['product_id'] == id:
                product['quantity'] = str(int(product['quantity']) + int(quantity))
                write_to_csv('inventory.csv', self.product_data, ['product_id', 'product_name', 'quantity', 'price'])
                print("Product stock updated successfully.")
                return

        print("Product ID not found.")

# Employee class
class Employee:
    def __init__(self, username, product_data, transaction_data):
        self.username = username
        self.product_data = product_data
        self.transaction_data = transaction_data
        # self.password=password
    def log_in(self,username,password):
        #import pdb;pdb.set_trace()
        temp=True
        for user in user_data:
            print(user)
            if user['username'] != username:
                temp="Username not found.please ask administration for registration"
            else:
                if user['password'] != password:
                    temp="Wrong Password. Please enter the correct password."
                else:
                    temp=True
                    return temp              
        return temp
    def view_product_list(self):
        print("product_id | product_name | quantity | price")
        for product in self.product_data:
            print(f"{product['product_id']} | {product['product_name']} | {product['quantity']} | {product['price']}")

    def sell_product(self):
        id = input("Enter product ID: ")
        if not validate_field(id):
            print("Id must be numeric.")
            return
        quantity = input("Enter quantity: ")
        if not validate_field(quantity):
            print("Quantity must be numeric.")
            return

        validation_result = validate_product_quantity(id, quantity, self.product_data)
        if validation_result is not True:
            print(validation_result)
            return

        for product in self.product_data:
            if product['product_id'] == id:
                total_amount = int(quantity) * int(product['price'])
                product['quantity'] = str(int(product['quantity']) - int(quantity))
                transaction = {
                    'employee_username': self.username,
                    'product_id': id,
                    'quantity_sold': quantity,
                    'total_amount': str(total_amount)
                }
                self.transaction_data.append(transaction)
                append_to_csv('transaction.csv', [transaction], ['employee_username', 'product_id', 'quantity_sold', 'total_amount'])
                write_to_csv('inventory.csv', self.product_data, ['product_id', 'product_name', 'quantity', 'price'])
                print("Product sold successfully.")
                return

    def view_transactions(self):
        total_sales=0
        for transaction in self.transaction_data:
            if transaction['employee_username'] == self.username:
                total_sales = total_sales+int(transaction['total_amount'])
        print(f"Total sales by {self.username}: {total_sales}")

#read data from csv and store in list
product_data = read_csv('inventory.csv')
transaction_data = read_csv('transaction.csv')
user_data = read_csv('users.csv')

#main menu for user
while True:
    print("----------------------")
    print("Select the role:")
    print("1. Admin")
    print("2. Employee")
    print("3. Exit")
    print("----------------------")

    role = input("Enter your choice: ")

    if role == '1':
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username == 'admin' and password == 'admin':
            admin = Admin(product_data, transaction_data)
            while True:
                print("----------------------")
                print("Admin functionality:")
                print("1. Add new Product")
                print("2. Update product stock")
                print("3. Add new Employee")
                print("4. View Transactions")
                print("5. Log Out")
                print("----------------------")
                choice = input("Select an option: ")
                match choice:
                    case '1':
                        admin.add_product()
                    case '2':
                        admin.update_product_stock()
                    case '3':
                        admin.add_employee()
                    case '4':
                        admin.view_transaction()
                    case '5':
                        break
                    case _:
                        print("Invalid choice.")
        else:
            print("Invalid admin credentials.")

    elif role == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        employee = Employee(username, product_data, transaction_data)
        verify=employee.log_in(username,password)
        if(verify==True):  
            while True:
                    print("----------------------")
                    print("Employee functionality:")
                    print("1. View Product List")
                    print("2. Sell Product")
                    print("3. View Personal Sales Summary")
                    print("4. Log Out")
                    print("----------------------")
                    choice = input("Select an option: ")
                    match choice:
                        case '1':
                            employee.view_product_list()
                        case '2':
                            employee.sell_product()
                        case '3':
                            employee.view_transactions()
                        case '4':
                            break
                        case _:
                            print("Invalid choice.")
                            break
        else:
            print(verify)
    elif role == '3':
        print("Exiting system.")
        break

    else:
        print("Invalid choice. Please try again.")
