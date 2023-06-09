# Connect the mariadb connector to this app.py file
import mariadb
import sys

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
        isGroupInput = input("Is this a group expense? (y/n): ")
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
            return "expense"
        elif transactionTypeInput == "2":
            return "payment"
        else:
            print("Invalid input.")
            continue

# =================== ALL ADD ===================
# All add functionalities

# Add a user to the database
def add_user():
    # @TODO: add validation for the user's inputs
    # Requests the needed information from the user
    first_name = input("Enter first name: ")
    middle_initial = input("Enter middle initial: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    balance = int(input("Enter initial balance: "))

    is_user = check_user()

    # Adds the user to the database
    try:
        cur.execute("INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES (?, ?, ?, ?, ?, ?)", [first_name, middle_initial, last_name, email, is_user, balance])
        conn.commit()
        print("User added.")
    except mariadb.Error as e:
        print(f"Error: {e}")


# Add an expense to the database
def add_expense():
    # Add to the transaction history table
    # Request the needed information from the user
    
    # @TODO: add validation for the user's inputs
    isGroup = check_grouped()
    if isGroup:
        # Choose a group
        view_groups()
        group_id = int(input("Enter group id: "))
        
        # Choose the group member who paid
        view_group_members(group_id)
        payer_id = int(input("Enter payee id: "))

        # Ask for the total amount
        total_amount = int(input("Enter total amount: "))
        # Compute for the amount per person in the group
        amount_per_person = total_amount / count_groupMembers(group_id)
        
        # Ask for the transaction type
        transaction_type = check_transactionType()

        if transaction_type == "expense":
            is_settled = False
        else:
            # @TODO: Add a check if the payment is settled
            is_settled = True

        # Ask for the transaction description
        transaction_description = input("Enter transaction description: ")

        # Add to the transaction history table
        try:
            cur.execute("INSERT INTO transaction_history (date_issued, is_group, payer_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES(CURDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?)", [isGroup, payer_id, count_groupMembers(group_id), is_settled, transaction_description, total_amount, amount_per_person, transaction_type, group_id])
            conn.commit()
            __holder__ = getLastInserted()
            print("Expense added.")
        except mariadb.Error as e:
            print(f"Error: {e}")

        # Add to the individual_makes_transaction table
        # For each member in the group, add to the individual_makes_transaction table
        try:
            cur.execute("SELECT individual_id FROM individual_belongs_friend_group WHERE group_id = ?", [group_id])
            members = cur.fetchall()
            for individual_id in members:
                cur.execute("INSERT INTO individual_makes_transaction (individual_id, transaction_id) VALUES (?, ?)", [individual_id[0], __holder__])
                conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
    else:
        # Choose a user
        view_users()
        payer_id = int(input("Enter payee id: "))

        # Ask for the total amount
        total_amount = int(input("Enter total amount: "))

        # Ask for the transaction type
        transaction_type = check_transactionType()

        if transaction_type == "expense":
            is_settled = False
        else:
            # @TODO: Add a check if the payment is settled
            is_settled = True

# =================== ALL VIEWS ===================
# View all users in the database
def view_users():
    try:
        cur.execute("SELECT * FROM individual")
        for (individual) in cur:
                print(f"User {individual[0]}: {individual[1]} {individual[2]}. {individual[3]} - {individual[4]}")
    except mariadb.Error as e:
        print(f"Error: {e}")

# View all the groups in the database
def view_groups():
        try:
            cur.execute("SELECT * FROM friend_group")
            for (group) in cur:
                print(f"Group {group[0]}: {group[1]}")
        except mariadb.Error as e:
            print(f"Error: {e}")

# View all the members of a certain group in the database
def view_group_members(group_id):
    # Print all the members of the group
        try:
            cur.execute("SELECT * FROM individual WHERE individual_id IN (SELECT individual_id FROM individual_belongs_friend_group WHERE group_id = ?)", [group_id])
            for (individual) in cur:
                print(f"User {individual[0]}: {individual[1]} {individual[2]}. {individual[3]} - {individual[4]}")
        except mariadb.Error as e:
            print(f"Error: {e}")


# Close Connection
def close_connection():
    conn.close()