# Connect the mariadb connector to this app.py file
import mariadb
import sys

# Extra imports
from prettytable import PrettyTable
from prettytable import from_db_cursor


# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="pennywise",
        password="ilovecmsc127",
        host="localhost",
        port=3306,
        database="moneytracker"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


# Variable for prettytable
formatTable = PrettyTable()

# ========================================================
# Dummy functions to test the connection
# Create a function to add an expense
# def add_expense():
#     expense = input("Enter the expense: ")
#     try:
#         cur.execute("INSERT INTO expense (expense_value) VALUES (?)", [expense])
#         conn.commit()
#         print("Expense added.")
#     except mariadb.Error as e:
#         print(f"Error: {e}")

def view_expense():
    try:
        cur.execute("SELECT * FROM expense")
        # print by accessing it as a list
        # mas maganda 'to kapag marami ng parameters ang gamit for printing
        # for expense in cur:
        #     print(f"Expense: {expense[1]}")
        # print by accessing it as a dictionary
        for (expense_id, expense) in cur:
            print(f"Expense {expense_id}: {expense}")
    except mariadb.Error as e:
        print(f"Error: {e}")

# uncomment to test some functions
# add_expense()
# view_expense()

# ========================================================
# All functions to be implemented

# =================== ALL GETS/COUNTS ===================
# All get/count functionalities
def count_groupMembers(group_id):
    try:
        cur.execute("SELECT number_of_members FROM friend_group WHERE group_id = ?", [group_id])
        for (count) in cur:
            return count[0]
    except mariadb.Error as e:
        print(f"Error: {e}")


def get_userID():
    try:
        cur.execute("SELECT individual_id FROM individual WHERE is_user IS TRUE")
        print(cur.fetchone()[0])
        for (user_id) in cur:
            return user_id[0]
    except mariadb.Error as e:
        print(f"Error: {e}")

def get_amount():
    while True:
        try:
            total_amount = int(input("Enter total amount: "))
            return total_amount
        except ValueError:
            print("Invalid input. Please enter an amount.")
            continue

def getLastInserted():
    try:
        cur.execute("SELECT transaction_id FROM transaction_history ORDER BY transaction_id DESC LIMIT 1")
        for (last_inserted) in cur:
            return last_inserted[0]
    except mariadb.Error as e:
        print(f"Error: {e}")

# =================== ALL CHECKS ===================
# All check functionalities

# Checks if the added user is the first user in the database
def check_user():
    cur.execute("SELECT * FROM individual")
    
    if cur.fetchone() is None:
        return True
    else:
        return False
    
# Check if it is a group or non-group expense
def check_grouped():
    while True:
        isGroupInput = input("Is this a group transaction? (y/n): ")
        if len(isGroupInput) != 1:
            print("Invalid input.")
            continue

        if isGroupInput.lower() != "y" and isGroupInput.lower() != "n":
            print("Invalid input!")
            continue

        if isGroupInput.lower() == "y":
            return True
        else:
            return False
        
def check_transactionType():
    while True:
        print("----- Transaction Type -----")
        print("1. Expense")
        print("2. Payment")
        transactionTypeInput = input("Enter your transaction's type: ")

        if transactionTypeInput == "1":
            return "EXPENSE"
        elif transactionTypeInput == "2":
            return "PAYMENT"
        else:
            print("Invalid input.")
            continue

# =================== ALL ADD ===================
# All add functionalities

# Add a user to the database
def add_user():
    # Requests the needed information from the user
    # Loops through each input to ensure that a valid information is entered    
    while True:
        first_name = input("Enter first name: ")
        first_name = first_name.replace(" ", "")  # Remove spaces from first name
        if len(first_name) <= 50 and first_name.isalpha():
            break
        else:
            print("Invalid input. Please enter a valid first name.")

    while True:
        middle_initial = input("Enter middle initial (press Enter for no middle initial): ")
        if len(middle_initial) <= 4:
            break
        else:
            print("Invalid input. Please enter a middle initial or leave it blank for no middle initial.")

    while True:
        last_name = input("Enter last name: ")
        last_name = last_name.replace(" ", "")  # Remove spaces from last name
        if len(last_name) <= 50 and last_name.isalpha():
            break
        else:
            print("Invalid input. Please enter a valid last name.")

    while True:
        email = input("Enter email: ")
        if len(email) <= 65 and "@" in email and "." in email:
            break
        else:
            print("Invalid input. Please enter a valid email.")

    while True:
        try:
            balance = float(input("Enter initial balance: "))
            balance_str = str(balance)
            if len(balance_str) <= 23 and len(balance_str.split('.')[-1]) <= 2:
                break
            else:
                print("Invalid input. Please enter a valid balance with a maximum of 20 digits and 2 decimal places.")
        except ValueError:
            print("Invalid input. Please enter a valid balance as a number.")

    is_user = check_user()

    # Adds the user to the database
    try:
        # If the user has no middle initial, insert it as NULL to the database
        if middle_initial == "":
            cur.execute("INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES (?, ?, ?, ?, ?, ?)", [first_name, None, last_name, email, is_user, balance])
        else:
            cur.execute("INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES (?, ?, ?, ?, ?, ?)", [first_name, middle_initial, last_name, email, is_user, balance])
        conn.commit()
        print("User added.")
    except mariadb.Error as e:
        print(f"Error: {e}")

def add_expense(transaction_type):
    is_settled = False

    # @TODO: add validation for the user's inputs
    isGroup = check_grouped()

    # For group expenses
    if isGroup:
        # Choose a group
        view_groups()
        while True:
            try:
                group_id = int(input("Enter group id: "))
            except ValueError:
                print("Invalid input. Please enter an id.")
                continue

            cur.execute("SELECT * FROM friend_group WHERE group_id = ?", [group_id])
            result = cur.fetchone()

            if result is not None:
                break
            else:
                print("Group id not found. Please try again.")
        
        # Choose the group member who paid
        view_group_members(group_id)
        while True:
            try:
                payee_id = int(input("Enter payee id: "))
            except ValueError:
                print("Invalid input. Please enter an id.")
                continue
        
            cur.execute("SELECT * FROM individual WHERE individual_id = ? AND individual_id IN (SELECT individual_id FROM individual_belongs_friend_group WHERE group_id = ?)", [payee_id, group_id])
            result = cur.fetchone()

            if result is not None:
                break
            else:
                print("User id not found. Please try again.")

        # Ask for the total amount
        total_amount = get_amount()

        # Compute for the amount per person in the group
        amount_per_person = total_amount / count_groupMembers(group_id)

        # Ask for the transaction description
        transaction_description = input("Enter transaction description: ")

        # Add to the transaction history table
        try:
            if transaction_description == "":
                cur.execute("INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES(CURDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?)", [isGroup, payee_id, count_groupMembers(group_id), is_settled, None, total_amount, amount_per_person, transaction_type, group_id])
            else:
                cur.execute("INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES(CURDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?)", [isGroup, payee_id, count_groupMembers(group_id), is_settled, transaction_description, total_amount, amount_per_person, transaction_type, group_id])
            conn.commit()
            __holder__ = getLastInserted()
            print("Expense added.")
        except mariadb.Error as e:
            print(f"Error: {e}")

        # For each member in the group, add to the individual_makes_transaction table and update individual balance
        try:
            cur.execute("SELECT individual_id FROM individual_belongs_friend_group WHERE group_id = ?", [group_id])
            members = cur.fetchall()
            for individual in members:
                cur.execute("INSERT INTO individual_makes_transaction (individual_id, transaction_id) VALUES (?, ?)", [individual[0], __holder__])
                conn.commit()

                if payee_id == individual[0]:
                    update_balance(individual[0], (-1*total_amount))
        except mariadb.Error as e:
            print(f"Error: {e}")
    
    # For non-group expenses
    else:
        # Choose a payee
        view_users()
        while True:
            try:
                payee_id = int(input("Enter payee id: "))
            except ValueError:
                print("Invalid input. Please enter an id.")
                continue
        
            cur.execute("SELECT * FROM individual WHERE individual_id = ?", [payee_id])
            result = cur.fetchone()

            if result is not None:
                break
            else:
                print("User id not found. Please try again.")

        # Choose a borrower
        view_users()
        while True:
            try:
                borrower_id = int(input("Enter borrower id: "))
            except ValueError:
                print("Invalid input. Please enter an id.")
                continue
        
            if borrower_id == payee_id:
                print("You cannot borrow from yourself. Please enter a payer id again.")
                continue
            
            cur.execute("SELECT * FROM individual WHERE individual_id = ?", [borrower_id])
            result = cur.fetchone()

            if result is not None:
                break
            else:
                print("User id not found. Please try again.")

        # Ask for the total amount
        total_amount = get_amount()

        # Compute for the amount per person in the group
        amount_per_person = total_amount / 2

        # Ask for the transaction description
        transaction_description = input("Enter transaction description: ")

        # Add to the transaction history table
        try:
            if transaction_description == "":
                cur.execute("INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES(CURDATE(), ?, ?, 2, ?, ?, ?, ?, ?, ?)", [isGroup, payee_id, is_settled, None, total_amount, amount_per_person, transaction_type, None])
            else:
                cur.execute("INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES(CURDATE(), ?, ?, 2, ?, ?, ?, ?, ?, ?)", [isGroup, payee_id, is_settled, transaction_description, total_amount, amount_per_person, transaction_type, None])
            conn.commit()
            __holder__ = getLastInserted()
            print("Expense added.")
        except mariadb.Error as e:
            print(f"Error: {e}")

        # Add to the individual_makes_transaction table
        try:
            cur.execute("INSERT INTO individual_makes_transaction (individual_id, transaction_id) VALUES (?, ?)", [payee_id, __holder__])
            conn.commit()

            cur.execute("INSERT INTO individual_makes_transaction (individual_id, transaction_id) VALUES (?, ?)", [borrower_id, __holder__])
            conn.commit()

            update_balance(payee_id, (-1*total_amount))
        except mariadb.Error as e:
            print(f"Error: {e}")


# Add an expense to the database
def add_transaction():
    # Ask for the transaction type
    transaction_type = check_transactionType()

    if transaction_type == "EXPENSE":
        add_expense(transaction_type)


# =================== ALL UPDATES ===================
# All update functionalities
def update_balance(individual_id, amount):
    try:
        cur.execute("UPDATE individual SET balance = balance + ? WHERE individual_id = ?", [amount, individual_id])
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")

# =================== ALL VIEWS ===================
# View all users in the database
def view_users():
    try:
        cur.execute("SELECT individual_id 'Individual ID', CONCAT(first_name, CASE WHEN middle_initial IS NULL THEN '' ELSE middle_initial END, last_name) 'Full Name', email 'Email' FROM individual")
        formatTable = from_db_cursor(cur)
        print(formatTable)
        # for (individual) in cur:
        #         print(f"User {individual[0]}: {individual[1]} {individual[2]}. {individual[3]} - {individual[4]}")
    except mariadb.Error as e:
        print(f"Error: {e}")

# View all the groups in the database
def view_groups():
        try:
            cur.execute("SELECT group_id 'Group ID', group_name 'Group Name', number_of_members 'Number of Members' FROM friend_group")
            # formatTable.field_names = ["Group ID", "Group Name", "Number of Members"]
            formatTable = from_db_cursor(cur)
            print(formatTable)
            # for (group) in cur:
            #     print(f"Group {group[0]}: {group[1]}")
        except mariadb.Error as e:
            print(f"Error: {e}")

# View all the members of a certain group in the database
def view_group_members(group_id):
    # Print all the members of the group
        try:
            cur.execute("SELECT individual_id 'Individual ID', CONCAT(first_name, CASE WHEN middle_initial IS NULL THEN '' ELSE middle_initial END, last_name) 'Full Name', email 'Email' FROM individual WHERE individual_id IN (SELECT individual_id FROM individual_belongs_friend_group WHERE group_id = ?)", [group_id])
            formatTable = from_db_cursor(cur)
            print(formatTable)
            # for (individual) in cur:
            #     print(f"User {individual[0]}: {individual[1]} {individual[2]}. {individual[3]} - {individual[4]}")
        except mariadb.Error as e:
            print(f"Error: {e}")

# Close Connection
def close_connection():
    conn.close()