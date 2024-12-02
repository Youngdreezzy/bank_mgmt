import mysql.connector as sql # For connecting your Python program to a MySQL database,
import random       # To generate random numbers or given words 
import pwinput   # To hide password character

import datetime     # For default date/time
import time
from datetime import time




mycon = sql.connect(
    host = "127.0.0.1",
    user = "root",
    password = "",
    database = "bank_db"
)
mycursor = mycon.cursor()
mycon.autocommit = True


# mycursor.execute("CREATE DATABASE bank_db")
# print('Successfully Created')


# mycursor.execute("CREATE TABLE customer(customer_id INT PRIMARY KEY AUTO_INCREMENT, fullname VARCHAR(50), email VARCHAR(50) UNIQUE, phone VARCHAR(14),gender VARCHAR(10), account_number VARCHAR(10) UNIQUE, address VARCHAR(500), date_created DATETIME DEFAULT CURRENT_TIMESTAMP)")
# print('Table Created')



import random
import datetime
import time
import pwinput  # Ensure you install this using `pip install pwinput`
from colorama import init, Fore, Back

class bankapp:
    def __init__(self):
        self.mode = "Bank App"
        self.email = ''
        self.fullname = ''
        self.account_number = '' 
        self.balance = 0
        self.mydate = datetime.datetime.now()

    
    def dashboard(self):
        print(
            '''
            OPTION:
                1. Sign Up
                2. Sign in
                3. Forgot password
                4. Exit 
            '''
        )
        option = input('Option: ')
        if option == '1':
            print('Loading...')
            time.sleep(2)
            self.register()
        elif option == '2':
            print('Loading...')
            time.sleep(3)
            self.login()
        elif option == '3':
            print('Loading...')
            time.sleep(2)
            self.forgot()
        elif option == '4':
            time.sleep(1)
            print('Thank you for banking with us. Goodbye...')
            time.sleep(2)
            exit()

    def dashboard2(self):
        print(
            f'''
            Name: {self.fullname}
            Balance: #{self.balance:.2f}

            OPTION:
            1. Deposit
            2. Withdraw
            3. Check Balance
            4. Transfer
            5. Transaction History
            6. Change password
            7. Exit/Home
            '''
        )

        option = input("Option: ")
        time.sleep(1)
        if option == '1':
            self.deposit()
        elif option == '2':
            self.withdraw()
        elif option == '3':
            self.acct_balance()
        elif option == '4':
            self.transfer()
        elif option == '5':
            self.transactions()
        elif option == '6':
            self.change()
        elif option == '7':
            print('Signing out...')
            time.sleep(2)
            self.dashboard()
        else:
            print('Invalid input, try again!')
            return self.dashboard2()

    def register(self):
        print(" *** Welcome to Holla Bank ***\n")
        fullname = input('Fullname: ')
        email = input('Email: ')
        password = input('Password: ')
        phone = input('Phone Number: ')
        gender = input('Gender: ')
        address = input('Address: ')
        acct = random.randint(2020000000, 2029999999)
        balance = 0

        query = """
        INSERT INTO customer (fullname, email, phone, gender, account_number, address, account_balance, password) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (fullname, email, phone, gender, acct, address, balance, password)
        mycursor.execute(query, values)

        print('Processing...')
        time.sleep(3)
        print(f"Registration Successful\nHello {fullname}, Your account number is {acct}")
        self.dashboard()

    def deposit(self):
        query = "SELECT account_balance FROM customer WHERE email = %s"
        val = (self.email,)
        mycursor.execute(query, val)
        detail = mycursor.fetchone()
        balance = detail[0]

        self.dep = float(input('Enter Amount to deposit: '))
        new_balance = balance + self.dep

        # Update customer balance
        query2 = "UPDATE customer SET account_balance = %s WHERE email = %s"
        val2 = (new_balance, self.email)
        mycursor.execute(query2, val2)
        self.balance = new_balance

        # Log the transaction
        query3 = "INSERT INTO transactions (type, amount, sender, email) VALUES (%s, %s, %s, %s)"
        val3 = ('Deposit', self.dep, self.fullname, self.email)
        mycursor.execute(query3, val3)

        print('Processing...')
        time.sleep(3)
        print(f'Your deposit of #{self.dep:.2f} is successful!\nYour current balance is #{self.balance:.2f}.')
        option = input('\nPress Enter to go to your dashboard or 1 to Logout')
        if option == '1':
            self.dashboard()
        else:
            self.dashboard2()

    def withdraw(self):
        query = "SELECT account_balance FROM customer WHERE email = %s"
        val = (self.email,)
        mycursor.execute(query, val)
        detail = mycursor.fetchone()
        balance = detail[0]

        self.withd = float(input('Enter Amount to withdraw: '))
        if self.withd > balance:
            print("Insufficient funds!")
            return self.dashboard2()

        new_balance = balance - self.withd

        # Update customer balance
        query2 = "UPDATE customer SET account_balance = %s WHERE email = %s"
        val2 = (new_balance, self.email)
        mycursor.execute(query2, val2)
        self.balance = new_balance

        # Log the transaction
        query3 = "INSERT INTO transactions (type, amount, sender, email) VALUES (%s, %s, %s, %s)"
        val3 = ('Withdrawal', self.withd, self.fullname, self.email)
        mycursor.execute(query3, val3)

        print('Processing...')
        
        time.sleep(2)
        
        print(f'Your withdrawal of#{self.withd:.2f} is successful!\n' f'Your current balance is #{self.balance:.2f}.')

        self.dashboard2()

    def acct_balance(self):
        print('Loading...')
        time.sleep(2)
        print(f'\nDear {self.fullname}, your account balance is: #{self.balance:.2f}\nThank you for banking with us!')

        self.option = input('\nPress Enter to return to the dashboard or press 1 to exit: ')
        if self.option == '1':
            print("Signing out...")
            time.sleep(2)
            exit()
        else:
            self.dashboard2()

    def transfer(self):
        self.transf_account = input("Enter the recipient's Account Number: ")
        try:
            amount = float(input("Enter the amount to transfer: "))
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return

        if amount > self.balance:
            print("Insufficient funds.")
            return

        
        query = "SELECT fullname, email FROM customer WHERE account_number = %s"
        val = (self.transf_account,)
        mycursor.execute(query, val)
        recipient = mycursor.fetchone()

        # Verify recipient account exists
        if recipient is None:
            print("Recipient account not found.")
            return

        recipient_name, recipient_email = recipient

        # Update balances for sender and recipient
        self.balance -= amount
        update_sender = "UPDATE customer SET account_balance = account_balance - %s WHERE account_number = %s"
        update_recipient = "UPDATE customer SET account_balance = account_balance + %s WHERE account_number = %s"
        mycursor.execute(update_sender, (amount, self.account_number))
        mycursor.execute(update_recipient, (amount, self.transf_account))

        # keeping log of the transaction
        query3 = "INSERT INTO transactions (type, amount, sender, receiver, email) VALUES (%s, %s, %s, %s, %s)"
        val3 = ('Transfer', amount, self.fullname, recipient_name, self.email)
        mycursor.execute(query3, val3)

        print(f"Successfully transferred #{amount:.2f} to {recipient_name}.\nYour new balance is #{self.balance:.2f}.")
        self.dashboard2()

    def transactions(self):
        print('Fetching....')
        time.sleep(3)
        print(f"\nTransaction History for {self.fullname}:\n")
        query = "SELECT type, amount, sender, receiver, date_time FROM transactions WHERE email = %s"
        val = (self.email,)
        mycursor.execute(query, val)
        history = mycursor.fetchall()

        if not history:
            print("No transaction history found.")
        else:
            print("Type      Amount      Sender        Receiver        Date/Time")
            print('-'*70)
            for record in history:
                typee, amount, sender, receiver, date_time = record
                receiver = receiver if receiver else "N/A"
                print(f"{typee:<10} {amount:<10} {sender:<15} {receiver:<15} {date_time}")

        input("\nPress Enter to return to the dashboard.")
        self.dashboard2()

    def login(self):
        self.email = input('Email: ')
        password = pwinput.pwinput()

        query = "SELECT fullname, email, password, account_number, account_balance FROM customer WHERE email = %s AND password = %s"
        val = (self.email, password)
        mycursor.execute(query, val)
        details = mycursor.fetchone()

        if details:
            self.fullname = details[0]
            self.account_number = details[3] 
            self.balance = details[4]
            print('Login successful')
            self.dashboard2()
        else:
            print("Incorrect email or password!\nKindly input the correct details.")
            self.login()

    def change(self):
        email = input('Email: ').strip()
        exPassword = input('Old Password: ').strip()
        freshPassword = input('New Password: ').strip()

        query = "UPDATE customer SET password = %s WHERE password = %s AND email = %s"
        val = (freshPassword, exPassword, email)
        mycursor.execute(query,val)
        print('Password Succesfully Updated')
        input('Press Enter to return to the homepage.')
        self.dashboard()

    def forgot(self):
        
        email = input('Email: ').strip()

        query = "SELECT password FROM customer WHERE email = %s"
        val = (email,)
        mycursor.execute(query,val)
        psw = mycursor.fetchone()

        while not psw:
            print('Incorrect email, Try again: ')
            email = input('Email: ').strip()
            return
        
        else:
            freshPassword = input('New Password: ').strip()
            retrypsw = input('Enter New Password Again: ').strip()
            while freshPassword != retrypsw:
                print('Password do not match, Try again')
            else:
                print('Correct')
        
        query2 = "UPDATE customer SET password = %s WHERE email = %s"
        val3 = (freshPassword, email)
        mycursor.execute(query2,val3)
        print('Password Successfully Modified')
        input('Press Enter to return to the homepage.')

        self.dashboard()


        


    def forgot(self):
        while True:
            email = input("Email: ").strip()

    # Trying to Check if the email exists in the database
            query = "SELECT password FROM customer WHERE email = %s"
            val = (email,)
            mycursor.execute(query, val)
            psw = mycursor.fetchone()

            if not psw:
                print("Incorrect email. Please try again.")
            else:
                break

    # Trying to Get a new password from the user
        while True:
            freshPassword = input("New Password: ").strip()
            retrypsw = input("Enter New Password Again: ").strip()

            if freshPassword != retrypsw:
                print("Passwords do not match. Please try again.")
            else:
                break

    # Trying to Update the password in the database
        query2 = "UPDATE customer SET password = %s WHERE email = %s"
        val2 = (freshPassword, email)
        mycursor.execute(query2, val2)
        print("Password successfully modified.")

        input("Press Enter to return to the homepage.")
        self.dashboard()







mydash = bankapp()
mydash.dashboard()












# mycursor.execute('USE bank_db')
# mycursor.execute('''
#     CREATE TABLE transactions (
#         trans_id INT PRIMARY KEY AUTO_INCREMENT,
#         type VARCHAR(7),
#         amount FLOAT(16),
#         date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
#         sender VARCHAR(50),
#         receiver VARCHAR(50),
#         email VARCHAR(50)
#     )
# ''')
# print('table created')

# mycursor.execute("ALTER TABLE transactions MODIFY COLUMN type VARCHAR(20)")
# print('Altered')


# mycursor.execute('SELECT account_number FROM customer')
# for column in mycursor:
#     print(column)


# mycursor.execute("ALTER TABLE customer ADD (account_balance FLOAT(15))")
# print('Column Added!')

# mycursor.execute("ALTER TABLE customer ADD (password VARCHAR(18))")
# print('column added')

# mycursor.execute("ALTER TABLE customer ADD COLUMN (Transaction_history VARCHAR(150))")
# print('Column added!')

# tran_id     type    amount      datetime        sender      receiver       owner's_email