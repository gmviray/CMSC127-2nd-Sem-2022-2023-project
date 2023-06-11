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
        return cur.fetchone()[0]
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
            return "SETTLEMENT"
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
        first_name_checker = first_name.replace(" ", "")  # Remove spaces from first name
        if len(first_name) <= 50 and first_name_checker.isalpha():
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
        last_name_checker = last_name.replace(" ", "")  # Remove spaces from last name
        if len(last_name) <= 50 and last_name_checker.isalpha():
            break
        else:
            print("Invalid input. Please enter a valid last name.")

    while True:
        email = input("Enter email: ")
        if len(email) <= 65 and "@" in email and "." in email:
            break
        else:
            print("Invalid input. Please enter a valid email.")

    balance = 0.00

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
        while True:
            transaction_description = input("Enter transaction description: ")
            if transaction_description.strip(): 
                break  
            else:
                print("Transaction description cannot be empty. Please try again.")

        # Add to the transaction history table
        try:
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
                if payee_id == individual[0]:
                    cur.execute("INSERT INTO individual_makes_transaction VALUES (?, ?, ?)", [individual[0], __holder__, 0])
                    conn.commit()
                    update_balance(individual[0], (total_amount - amount_per_person))
                else:
                    cur.execute("INSERT INTO individual_makes_transaction VALUES (?, ?, ?)", [individual[0], __holder__, -1*amount_per_person])
                    conn.commit()
                    update_balance(individual[0], (-1*amount_per_person))

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

        if payee_id == get_userID():
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
        else:
            borrower_id = get_userID()

        # Ask for the total amount
        total_amount = get_amount()

        # Compute for the amount per person in the group
        amount_per_person = total_amount / 2

        # Ask for the transaction description
        while True:
            transaction_description = input("Enter transaction description: ")
            if transaction_description.strip(): 
                break  
            else:
                print("Transaction description cannot be empty. Please try again.")

        # Add to the transaction history table
        try:
            cur.execute("INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES(CURDATE(), ?, ?, 2, ?, ?, ?, ?, ?, ?)", [isGroup, payee_id, is_settled, transaction_description, total_amount, amount_per_person, transaction_type, None])
            conn.commit()
            __holder__ = getLastInserted()
            print("Expense added.")
        except mariadb.Error as e:
            print(f"Error: {e}")

        # Add to the individual_makes_transaction table
        try:
            cur.execute("INSERT INTO individual_makes_transaction VALUES (?, ?, ?)", [payee_id, __holder__, 0])
            conn.commit()
            update_balance(payee_id, (total_amount - amount_per_person))

            cur.execute("INSERT INTO individual_makes_transaction VALUES (?, ?, ?)", [borrower_id, __holder__, -1*amount_per_person])
            conn.commit()
            update_balance(borrower_id, (-1*amount_per_person))

        except mariadb.Error as e:
            print(f"Error: {e}")

def add_settlement(transaction_type):
    isGroup = check_grouped()

    # For group settlements
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

        # Choose a payer
        view_group_members(group_id)
        while True:
            try:
                payer_id = int(input("Enter your id: "))
            except ValueError:
                print("Invalid input. Please enter an id.")
                continue
        
            cur.execute("SELECT * FROM individual WHERE individual_id = ? AND individual_id IN (SELECT individual_id FROM individual_belongs_friend_group WHERE group_id = ?)", [payer_id, group_id])
            result = cur.fetchone()

            if result is not None:
                break
            else:
                print("You don't belong to that group. Please try again.")

        # Display all the expenses of the payer that are not yet settled
        query = """
        SELECT transaction_id 'Transaction ID', transaction_description 'Description',
            total_amount 'Total Amount', contribution 'Splitted Amount', payee_id 'Payee ID'
            FROM transaction_history
            WHERE group_id = ? AND payee_id != ?
            AND type_of_transaction = ?
            AND is_settled IS FALSE;
        """

        try:
            cur.execute(query, [group_id, payer_id, "EXPENSE"])
            result = cur.fetchone()
            if result is None:
                print("No expenses to settle.")
                return 
        except mariadb.Error as e:
            print(f"Error: {e}")

        # Display all the transactions that the user has not yet settled
        cur.execute(query, [group_id, payer_id, "EXPENSE"])
        formatTable = from_db_cursor(cur)
        print(formatTable)
        while True:
            # Request for the transaction id to settle
            try:
                transaction_id_to_settle = int(input("Enter transaction id to settle: "))
            except ValueError:
                print("Invalid input. Please enter an id.")
                continue

            cur.execute("SELECT * FROM transaction_history WHERE transaction_id = ? AND group_id = ? AND payee_id != ? AND type_of_transaction = ? AND is_settled IS FALSE", [transaction_id_to_settle, group_id, payer_id, "EXPENSE"])
            result = cur.fetchone()

            if result is not None:
                # Check if the selected transaction is already settled
                cur.execute("SELECT * FROM individual_makes_transaction WHERE transaction_id = ? AND individual_id = ? AND transaction_amount != 0", [transaction_id_to_settle, payer_id])
                result = cur.fetchone()

                if result is None:
                    print("You have already paid for your contribution.")
                    return
                else:
                    break
            else:
                print("Transaction id not found. Please try again.")
                continue

        try:
            cur.execute("SELECT transaction_id 'Transaction ID', -1*transaction_amount 'Outstanding Balance' FROM individual_makes_transaction WHERE transaction_id = ? AND individual_id = ?", [transaction_id_to_settle, payer_id])
            formatTable = from_db_cursor(cur)
            print(formatTable)
        except mariadb.Error as e:
            print(f"Error: {e}")

        # Request for the amount to settle
        while True:
            try:
                amount_to_settle = float(input("Enter amount to settle: "))
            except ValueError:
                print("Invalid input. Please enter an amount.")
                continue

            if amount_to_settle <= 0:
                print("Amount to settle must be greater than 0. Please try again.")
                continue
            elif amount_to_settle > -1*result[2]:
                print("Amount to settle must be less than or equal to the total amount. Please try again.")
                continue
            else:
                break
        
        while True:
            transaction_description = input("Enter transaction description: ")
            if transaction_description.strip(): 
                break  
            else:
                print("Transaction description cannot be empty. Please try again.")

        cur.execute("SELECT payee_id FROM transaction_history WHERE transaction_id = ?", [transaction_id_to_settle])
        payee_id = cur.fetchone()[0]

        # Add the settlement to the transaction history table
        cur.execute("INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES(CURDATE(), ?, ?, 2, ?, ?, ?, ?, ?, ?)", [isGroup, payee_id, True, transaction_description, -1*result[2], amount_to_settle, transaction_type, group_id])
        conn.commit()

        # Add the settlement to the individual_makes_transaction table
        cur.execute("SELECT payee_id FROM transaction_history WHERE transaction_id = ?", [transaction_id_to_settle])
        payee_id = cur.fetchone()[0]

        cur.execute("INSERT INTO individual_makes_transaction VALUES (?, ?, ?)", [payer_id, getLastInserted(), amount_to_settle])
        conn.commit()

        # Update all related information
        cur.execute("UPDATE individual_makes_transaction SET transaction_amount = transaction_amount + ? WHERE transaction_id = ? AND individual_id = ?", [amount_to_settle, transaction_id_to_settle, payer_id])
        conn.commit()
        cur.execute("UPDATE individual SET balance = balance + ? WHERE individual_id = ?", [amount_to_settle, payer_id])
        conn.commit()
        cur.execute("UPDATE individual SET balance = balance - ? WHERE individual_id = (SELECT payee_id FROM transaction_history WHERE transaction_id = ?)", [amount_to_settle, transaction_id_to_settle])
        conn.commit()

        print("Settlement added.")

        # Check if the transaction is already settled
        cur.execute("SELECT * FROM individual_makes_transaction WHERE transaction_id = ?", [transaction_id_to_settle])
        result = cur.fetchall()
        for row in result:
            if row[2] == 0:
                isSettled = True
            else:
                isSettled = False
                break
        
        if isSettled:
            cur.execute("UPDATE transaction_history SET is_settled = TRUE WHERE transaction_id = ?", [transaction_id_to_settle])
            conn.commit()
            print("Transaction is now settled.")
        else:
            print("Transaction is still not yet settled.")

    # For non-group settlements
    else:
        view_users()
        # Request for the payer id
        while True:
            try:
                payer_id = int(input("Enter payer id: "))
            except ValueError:
                print("Invalid input. Please enter an id.")
                continue

            cur.execute("SELECT * FROM individual WHERE individual_id = ?", [payer_id])
            result = cur.fetchone()

            if result is not None:
                break
            else:
                print("Invalid User ID. Please try again.")

        # Check if the user has any outstanding balance with a friend
        query = """
        SELECT * FROM transaction_history
            WHERE payee_id != ?
            AND type_of_transaction = ? 
            AND is_settled IS FALSE 
            AND is_group IS FALSE 
            AND transaction_id IN 
            (SELECT transaction_id FROM individual_makes_transaction 
            WHERE individual_id = ? 
            AND transaction_amount < 0)
        """
        
        try:
            cur.execute(query, [payer_id, "EXPENSE", payer_id])
            result = cur.fetchone()
            
            if result is None:
                print("You don't have any outstanding balance with a friend.")
                return       
        except mariadb.Error as e:
            print(f"Error: {e}")

        # Display all the transactions that the user has not yet settled
        cur.execute("SELECT transaction_id 'Transaction ID', transaction_description 'Description', total_amount 'Total Amount', contribution 'Splitted Amount', payee_id 'Payee ID' FROM transaction_history WHERE payee_id != ? AND type_of_transaction = ? AND is_settled IS FALSE AND is_group IS FALSE", [payer_id, "EXPENSE"])
        formatTable = from_db_cursor(cur)
        print(formatTable)
        while True:
            #  Request for the transaction to settle
            try:
                transaction_id_to_settle = int(input("Enter transaction id to settle: "))
            except ValueError:
                print("Invalid input. Please enter an id.")
                continue

            cur.execute("SELECT * FROM transaction_history WHERE transaction_id = ? AND payee_id != ? AND type_of_transaction = ? AND is_settled IS FALSE AND is_group IS FALSE", [transaction_id_to_settle, payer_id, "EXPENSE"])
            result = cur.fetchone()

            if result is not None:
                break
            else:
                print("Transaction ID not found. Please try again.")
                continue

        try:
            cur.execute("SELECT transaction_id 'Transaction ID', -1*transaction_amount 'Outstanding Balance' FROM individual_makes_transaction WHERE transaction_id = ? AND individual_id = ?", [transaction_id_to_settle, payer_id])
            formatTable = from_db_cursor(cur)
            print(formatTable)
        except mariadb.Error as e:
            print(f"Error: {e}")

        # Request for the amount to settle
        while True:
            try:
                amount_to_settle = float(input("Enter amount to settle: "))
            except ValueError:
                print("Invalid input. Please enter an amount.")
                continue

            cur.execute("SELECT transaction_amount FROM individual_makes_transaction WHERE transaction_id = ? AND individual_id = ?", [transaction_id_to_settle, payer_id])
            current_amount = cur.fetchone()[0]
            if amount_to_settle <= 0:
                print("Amount to settle must be greater than 0. Please try again.")
                continue
            elif amount_to_settle > -1*current_amount:
                print("Amount to settle must be less than or equal to the total amount. Please try again.")
                continue
            else:
                break
        
        while True:
            transaction_description = input("Enter transaction description: ")
            if transaction_description.strip(): 
                break  
            else:
                print("Transaction description cannot be empty. Please try again.")

        # Add the settlement to the transaction history table
        cur.execute("SELECT payee_id FROM transaction_history WHERE transaction_id = ?", [transaction_id_to_settle])
        payee_id = cur.fetchone()[0]

        cur.execute("INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction) VALUES(CURDATE(), ?, ?, 2, ?, ?, ?, ?, ?)", [isGroup, payee_id, True, transaction_description, -1*result[2], amount_to_settle, transaction_type])
        conn.commit()

        # Add the settlement to the individual_makes_transaction table
        cur.execute("INSERT INTO individual_makes_transaction VALUES (?, ?, ?)", [payer_id, getLastInserted(), amount_to_settle])
        conn.commit()

        # Update all related information
        cur.execute("UPDATE individual_makes_transaction SET transaction_amount = transaction_amount + ? WHERE transaction_id = ? AND individual_id = ?", [amount_to_settle, transaction_id_to_settle, payer_id])
        conn.commit()
        cur.execute("UPDATE individual SET balance = balance + ? WHERE individual_id = ?", [amount_to_settle, payer_id])
        conn.commit()
        cur.execute("UPDATE individual SET balance = balance - ? WHERE individual_id = ?", [amount_to_settle, payee_id])
        conn.commit()
        
        print("Settlement added.")
        
        # Check if the transaction is now settled
        cur.execute("SELECT transaction_amount FROM individual_makes_transaction WHERE transaction_id = ? AND individual_id = ?", [transaction_id_to_settle, payer_id])
        updated_balance = cur.fetchone()[0]
        if updated_balance == 0:
            cur.execute("UPDATE transaction_history SET is_settled = TRUE WHERE transaction_id = ?", [transaction_id_to_settle])
            conn.commit()
            print("Transaction is now settled.")
        else:
            print("Transaction is still not yet settled.")

# Add an expense to the database
def add_transaction():
    # Ask for the transaction type
    transaction_type = check_transactionType()

    if transaction_type == "EXPENSE":
        add_expense(transaction_type)
    else: 
        add_settlement(transaction_type)


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