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
# def view_expense():
#     try:
#         cur.execute("SELECT * FROM expense")
#         # print by accessing it as a list
#         # mas maganda 'to kapag marami ng parameters ang gamit for printing
#         # for expense in cur:
#         #     print(f"Expense: {expense[1]}")
#         # print by accessing it as a dictionary
#         for (expense_id, expense) in cur:
#             print(f"Expense {expense_id}: {expense}")
#     except mariadb.Error as e:
#         print(f"Error: {e}")

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

def getLastInsertedTransaction():
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
            __holder__ = getLastInsertedTransaction()
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
            __holder__ = getLastInsertedTransaction()
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

        cur.execute("INSERT INTO individual_makes_transaction VALUES (?, ?, ?)", [payer_id, getLastInsertedTransaction(), amount_to_settle])
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
        cur.execute("INSERT INTO individual_makes_transaction VALUES (?, ?, ?)", [payer_id, getLastInsertedTransaction(), amount_to_settle])
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

# Add a group to the database
def add_group():
    # Requests the needed information from the user
    # Loops through each input to ensure that a valid information is entered    
    while True:
        group_name = input("Enter group name: ")
        if group_name.strip(): 
            break  
        else:
            print("Group name cannot be empty. Please try again.")
    
    try:
        cur.execute("INSERT INTO friend_group (group_name, number_of_members) VALUES (?, ?)", [group_name, 1])
        conn.commit()

        cur.execute("SELECT LAST_INSERT_ID()")
        for row in cur:
            group_id = row[0]
            print(group_id)

        cur.execute("INSERT INTO individual_belongs_friend_group (individual_id, group_id) VALUES (?, ?)", [get_userID(), group_id])
        conn.commit()

        print("Group added.")  
    except mariadb.Error as e:
        print(f"Error: {e}")

    while True:
        # Gets the current number of members in the group
        cur.execute("SELECT number_of_members FROM friend_group ORDER BY group_id DESC LIMIT 1")
        number_of_members = cur.fetchone()[0]
        
        choice = input("Do you want to add individuals to the group? (y/n): ")
        if len(choice) != 1:
            print("Invalid input.")
            continue

        if choice.lower() != "y" and choice.lower() != "n":
            print("Please choose either 'y' or 'n' only.")
            continue
        
        if choice.lower() == "n":
            if number_of_members < 2:
                print("Group must have at least two member. Please try again.")
                continue
            else:
                break
        
        view_users()
        # Request for the individual id of the user to be added to the group
        while True:
            try:
                individual_id = int(input("Enter individual id: "))
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue

            cur.execute("SELECT individual_id FROM individual WHERE individual_id = ?", [individual_id])
            if cur.fetchone() is None:
                print("Individual ID not found. Please try again.")
                continue

            cur.execute("SELECT * FROM individual_belongs_friend_group WHERE individual_id = ? AND group_id = ?", [individual_id, group_id])
            if cur.fetchone() is not None:
                print("This individual is already a member of the group.")
                continue
            
            try:
                cur.execute("INSERT INTO individual_belongs_friend_group VALUES (?, ?)", [individual_id, group_id])
                conn.commit()
                cur.execute("UPDATE friend_group SET number_of_members = number_of_members + 1 WHERE group_id = ?", [group_id])
                conn.commit()
                print("Group member added.")
            except mariadb.Error as e:
                print(f"Error: {e}")
            
            break  

# =================== ALL SEARCH ===================
# Search transactions by ID
def search_transactionById(id):
    try:
        cur.execute('SELECT * FROM transaction_history WHERE transaction_id = ?', [id])
        if cur.fetchone() is not None:
            cur.execute("""SELECT transaction_id 'ID', date_issued 'Date Issued', 
                        CASE WHEN is_group = 1 THEN 'Yes' ELSE 'No' END 'Is Group?',
                        payee_id 'Payee ID', number_of_users_involved 'No. of Users Involved',
                        CASE WHEN is_settled = 1 THEN 'Yes' ELSE 'No' END 'Is Settled?',
                        transaction_description 'Description', total_amount 'Total Amount',
                        contribution 'Contribution', type_of_transaction 'Type', group_id 'Group ID'
                        FROM transaction_history WHERE transaction_id = ?""", [id])
            formatTable = from_db_cursor(cur)
            print(formatTable)
            return True
        else:
            print("\nTransaction not found.")
            return False
    except mariadb.Error as e:
        print(f"\nError: {e}")
        return False

def search_transactionMadeWithOrWithoutAGroup(choice):
    if choice == '2': is_group = '1'
    else: is_group = '0'

    try:
        cur.execute('SELECT * FROM transaction_history WHERE is_group = ?', [is_group])
        row_nums = cur.fetchone()[0]
        if row_nums > 0:
            cur.execute("SELECT transaction_id 'ID', date_issued 'Date Issued' FROM transaction_history WHERE is_group= ?", [is_group])
            formatTable = from_db_cursor(cur)
            print(formatTable)
            
            id = input('\nEnter transaction ID: ')
            cur.execute("SELECT * FROM transaction_history WHERE is_group= ? AND transaction_id = ?", [is_group, id])
            if cur.fetchone() is not None:
                cur.execute("""SELECT transaction_id 'ID', date_issued 'Date Issued', 
                            CASE WHEN is_group = 1 THEN 'Yes' ELSE 'No' END 'Is Group?',
                            payee_id 'Payee ID', number_of_users_involved 'No. of Users Involved',
                            CASE WHEN is_settled = 1 THEN 'Yes' ELSE 'No' END 'Is Settled?',
                            transaction_description 'Description', total_amount 'Total Amount',
                            contribution 'Contribution', type_of_transaction 'Type', group_id 'Group ID'
                            FROM transaction_history WHERE is_group= ? AND transaction_id = ?""", [is_group, id])
                formatTable = from_db_cursor(cur)
                print(formatTable)
            else:
                print("\nTransaction not found.")
        else:
            if is_group == '1': print("No transaction made with a group yet")
            else: print("No transaction made without a group yet")
    except mariadb.Error as e:
        print(f"\nError: {e}")

# Search transactions by month
def search_transactionByMonth(month):
    try:
        cur.execute('SELECT * FROM transaction_history WHERE MONTH(date_issued) = ?', [month])
        if cur.fetchone() is not None:
            cur.execute("""SELECT transaction_id 'ID', date_issued 'Date Issued', 
                        CASE WHEN is_group = 1 THEN 'Yes' ELSE 'No' END 'Is Group?',
                        payee_id 'Payee ID', number_of_users_involved 'No. of Users Involved',
                        CASE WHEN is_settled = 1 THEN 'Yes' ELSE 'No' END 'Is Settled?',
                        transaction_description 'Description', total_amount 'Total Amount',
                        contribution 'Contribution', type_of_transaction 'Type', group_id 'Group ID'
                        FROM transaction_history WHERE MONTH(date_issued) = ?""", [month])
            formatTable = from_db_cursor(cur)
            print(formatTable)
        else:
            print("\nTransaction not found.")
    except mariadb.Error as e:
        print(f"\nError: {e}")

# Search friend
def search_friend():
    try:
        cur.execute('SELECT COUNT(individual_id) from individual')
        indiv_num = cur.fetchone()[0]
        if indiv_num > 1:
            while True:
                try:
                    choice = input("\n1. Search by ID\n2. Search by Name\n3. Search by Email\nEnter your sub-choice: ")
                    if (int(choice) > 3 or int(choice) < 1):
                        print('Please input valid choice\n')
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter an integer.")
                    continue

            if choice == '1':
                id = input("Enter friend's ID: ")
                search_friendById(id)
            elif choice == '2':
                name = input("Enter friend's name: ")
                search_friendByName(name)
            elif choice == '3':
                email = input("Enter friend's email: ")
                search_friendByEmail(email)
        else:
            print("\nNo friends yet.")
    except mariadb.Error as e:
        print(f"Error: {e}")

# Search friend by ID
def search_friendById(id):
    try:
        cur.execute('SELECT * FROM individual WHERE individual_id = ? AND is_user = 0', [id])
        if cur.fetchone() is not None:
            cur.execute("""SELECT individual_id 'ID',
                            CONCAT(first_name, ' ', COALESCE(CONCAT(middle_initial, ' '), ''), last_name) 'Full Name',
                            email 'Email', balance 'Balance' FROM individual WHERE individual_id = ? AND is_user = 0""", [id])
            formatTable = from_db_cursor(cur)
            print(formatTable)
            return True
        else:
            print("\nFriend not found.")
            return False
    except mariadb.Error as e:
        print(f"\nError: {e}")
        return False

#  Search friend by Name (First Name/Last Name/Full Name/Full Name without Middle Initial)
def search_friendByName(name):
    try:
        cur.execute("""SELECT * FROM individual WHERE last_name = ? OR first_name = ?
                        OR CONCAT(first_name, ' ', last_name) = ? OR
                        CONCAT(first_name, ' ', COALESCE(middle_initial, ''), ' ', last_name) = ? AND is_user = 0""", [name, name, name, name])
        if cur.fetchone() is not None:
            cur.execute("""SELECT individual_id 'ID',
                            CONCAT(first_name, ' ', COALESCE(CONCAT(middle_initial, ' '), ''), last_name) 'Full Name',
                            email 'Email', balance 'Balance' FROM individual WHERE last_name = ? OR first_name = ?
                            OR CONCAT(first_name, ' ', last_name) = ? OR
                            CONCAT(first_name, ' ', COALESCE(middle_initial, ''), ' ', last_name) = ? AND is_user = 0""", [name, name, name, name])
            formatTable = from_db_cursor(cur)
            print(formatTable)
        else:
            print("\nFriend not found.")
    except mariadb.Error as e:
        print(f"Error: {e}")

# Search friend by Email
def search_friendByEmail(email):
    try:
        cur.execute('SELECT * FROM individual WHERE email = ?', [email])
        if cur.fetchone() is not None:
            cur.execute("""SELECT individual_id 'ID',
                            CONCAT(first_name, ' ', COALESCE(CONCAT(middle_initial, ' '), ''), last_name) 'Full Name',
                            email 'Email', balance 'Balance' FROM individual WHERE email = ? AND is_user = 0""", [email])
            formatTable = from_db_cursor(cur)
            print(formatTable)
        else:
            print("\nFriend not found.")
    except mariadb.Error as e:
        print(f"Error: {e}")

# Search group by ID
def search_groupById(id):
    try:
        cur.execute("SELECT * FROM friend_group WHERE group_id = ?", [id])
        if cur.fetchone() is not None:
            cur.execute("""SELECT group_id 'ID', group_name 'Group Name', number_of_members 'No. of Members'
            FROM friend_group WHERE group_id = ?""", [id])
            formatTable = from_db_cursor(cur)
            print(formatTable)
            return True
        else:
            print("\Group not found.")
            return False
    except mariadb.Error as e:
        print(f"\nError: {e}")
        return False

#  Search group by Name
def search_groupByName(name):
    try:
        cur.execute("""SELECT * FROM friend_group WHERE group_name = ?""", [name])
        if cur.fetchone() is not None:
            cur.execute("""SELECT group_id 'ID', group_name 'Group Name', number_of_members 'No. of Members'
            FROM friend_group WHERE group_name = ?""", [name])
            formatTable = from_db_cursor(cur)
            print(formatTable)
        else:
            print("\Group not found.")
    except mariadb.Error as e:
        print(f"Error: {e}")

# =================== ALL UPDATES ===================
# All update functionalities
def update_balance(individual_id, amount):
    try:
        cur.execute("UPDATE individual SET balance = balance + ? WHERE individual_id = ?", [amount, individual_id])
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")

#  Update transaction description
def update_transactionById(transaction_id, new_description):
    try:
        cur.execute("UPDATE transaction_history SET transaction_description = ? WHERE transaction_id = ?", [new_description, transaction_id])
        conn.commit()
        print("\nTransaction description updated successfully.")
    except mariadb.Error as e:
        print(f"\nError: {e}")

# Update friend's first name
def update_friendFirstName(friend_id, new_first_name):
    try:
        cur.execute("UPDATE individual SET first_name = ? WHERE individual_id = ? AND is_user = 0", [new_first_name, friend_id])
        conn.commit()
        print("\nFriend's first name updated successfully.")
    except mariadb.Error as e:
        print(f"\nError: {e}")

# Update friend's middle initial
def update_friendMiddleInitial(friend_id, new_middle_initial):
    try:
        cur.execute("UPDATE individual SET middle_initial = ? WHERE individual_id = ? AND is_user = 0", [new_middle_initial, friend_id])
        conn.commit()
        print("\nFriend's middle initial updated successfully.")
    except mariadb.Error as e:
        print(f"\nError: {e}")

# Update friend's last name
def update_friendLastName(friend_id, new_last_name):
    try:
        cur.execute("UPDATE individual SET last_name = ? WHERE individual_id = ? AND is_user = 0", [new_last_name, friend_id])
        conn.commit()
        print("\nFriend's last name updated successfully.")
    except mariadb.Error as e:
        print(f"\nError: {e}")

# Update friend's email
def update_friendEmail(friend_id, new_email):
    try:
        cur.execute("UPDATE individual SET email = ? WHERE individual_id = ? AND is_user = 0", [new_email, friend_id])
        conn.commit()
        print("\nFriend's email updated successfully.")
    except mariadb.Error as e:
        print(f"\nError: {e}")

# Update group name
def update_groupById(group_id, new_group_name):
    try:
        cur.execute("UPDATE friend_group SET group_name = ? WHERE group_id = ?", [new_group_name, group_id])
        conn.commit()
        print("\nGroup name updated successfully.")
    except mariadb.Error as e:
        print(f"\nError: {e}")

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

# View current balance
def view_balance():
    try:
        cur.execute("SELECT balance FROM individual WHERE individual_id = ?", [get_userID()])
        balance = cur.fetchone()[0]

        if balance == 0:
            print("Overall, you are all cleared up.")
        elif balance > 0:
            print(f"Overall, you are owed ₱{balance}.")
        else:
            print(f"Overall, you owe ₱{balance}.")

    except mariadb.Error as e:
        print(f"Error: {e}")

# View all transactions made within a month from the current date
def view_transactionsWithinAMonth():
    try:
        cur.execute("SELECT * FROM transaction_history WHERE DATEDIFF(CURDATE(), date_issued) <= 30")
        if cur.fetchone() is None:
            print("No expenses made within a month.")
        else:
            cur.execute("SELECT * FROM transaction_history WHERE DATEDIFF(CURDATE(), date_issued) <= 30")
            formatTable = from_db_cursor(cur)
            print(formatTable)
    
    except mariadb.Error as e:
        print(f"Error: {e}")

# View all transactions made with a friend
def view_transactionsWithFriend():
    view_users()
    while True:
        try:
            individual_id = int(input("Enter individual id: "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            continue

        if individual_id == get_userID():
            print("You cannot be your own friend.")
            continue

        cur.execute("SELECT individual_id FROM individual WHERE individual_id = ?", [individual_id])
        if cur.fetchone() is None:
            print("Individual ID not found. Please try again.")
            continue

        break

    try:
        cur.execute("SELECT * FROM transaction_history WHERE group_id IS NULL AND transaction_id IN (SELECT transaction_id FROM individual_makes_transaction WHERE individual_id = ?)", [individual_id])
        if cur.fetchone() is None:
            print("No expenses made with this friend.")
        else:
            cur.execute("SELECT * FROM transaction_history WHERE group_id IS NULL AND transaction_id IN (SELECT transaction_id FROM individual_makes_transaction WHERE individual_id = ?)", [individual_id])
            formatTable = from_db_cursor(cur)
            print(formatTable)

    except mariadb.Error as e:
        print(f"Error: {e}")

# View all transactions made with a group
def view_transactionsWithGroup():
    view_groups()
    while True:
        try:
            group_id = int(input("Enter group id: "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            continue

        cur.execute("SELECT group_id FROM friend_group WHERE group_id = ?", [group_id])
        if cur.fetchone() is None:
            print("Group ID not found. Please try again.")
            continue
        
        break

    try:
        cur.execute("SELECT * FROM transaction_history WHERE group_id = ?", [group_id])
        if cur.fetchone() is None:
            print("No expenses made with this group.")
        else:
            cur.execute("SELECT * FROM transaction_history WHERE group_id = ?", [group_id])
            formatTable = from_db_cursor(cur)
            print(formatTable)

    except mariadb.Error as e:
        print(f"Error: {e}")

# View all friends with outstanding balances
def view_friendsWithOutstandingBalances():
    query = """
    SELECT transaction_id, individual_id,
        payee_id, is_group,
        CASE
        WHEN individual_id IN 
        (SELECT payee_id FROM individual_makes_transaction i
        NATURAL JOIN transaction_history t
        WHERE is_group IS FALSE
        AND (individual_id = 1 OR payee_id = 1)
        AND transaction_amount < 0
        ORDER BY i.transaction_id)
        THEN `inside`.transaction_amount +
        -1*(SELECT transaction_amount FROM individual_makes_transaction i
        NATURAL JOIN transaction_history t
        WHERE is_group IS FALSE
        AND transaction_amount < 0
        AND individual_id = 1
        AND payee_id = `inside`.individual_id
        ORDER BY i.transaction_id)
        ELSE `inside`.transaction_amount
        END 'Total Outsanding Balance'
        FROM (SELECT * FROM individual_makes_transaction i
        NATURAL JOIN transaction_history t
        WHERE is_group IS FALSE
        AND (individual_id != 1 OR payee_id = 1)
        AND transaction_amount < 0
        ORDER BY i.transaction_id) AS inside
        GROUP BY individual_id
    """

    try:
        cur.execute(query)
        if cur.fetchone() is None:
            print("No friends with outstanding balances.")
        else:
            cur.execute("""
            SELECT individual_id 'Individual ID', CONCAT(first_name, ' ', CASE WHEN middle_initial IS NULL THEN '' ELSE CONCAT(middle_initial, '. ') END, last_name) 'Full Name',
                email 'Email', `Total Outsanding Balance`
                FROM individual NATURAL JOIN (SELECT transaction_id, individual_id,
                payee_id, is_group,
                CASE
                WHEN individual_id IN 
                (SELECT payee_id FROM individual_makes_transaction i
                NATURAL JOIN transaction_history t
                WHERE is_group IS FALSE
                AND (individual_id = 1 OR payee_id = 1)
                AND transaction_amount < 0
                ORDER BY i.transaction_id)
                THEN `inside`.transaction_amount +
                -1*(SELECT transaction_amount FROM individual_makes_transaction i
                NATURAL JOIN transaction_history t
                WHERE is_group IS FALSE
                AND transaction_amount < 0
                AND individual_id = 1
                AND payee_id = `inside`.individual_id
                ORDER BY i.transaction_id)
                ELSE `inside`.transaction_amount
                END 'Total Outsanding Balance'
                FROM (SELECT * FROM individual_makes_transaction i
                NATURAL JOIN transaction_history t
                WHERE is_group IS FALSE
                AND (individual_id != 1 OR payee_id = 1)
                AND transaction_amount < 0
                ORDER BY i.transaction_id) AS inside
                GROUP BY individual_id) AS outside
                """)
            formatTable = from_db_cursor(cur)
            print(formatTable)

    except mariadb.Error as e:
        print(f"Error: {e}")

# View all groups with outstanding balances
def view_groupsWithOutstandingBalances():
    query = """
    SELECT fg.group_id, fg.group_name, SUM(th.total_amount - COALESCE(SUM(imt.transaction_amount), 0)) AS balance
    FROM friend_group fg
    INNER JOIN transaction_history th ON th.group_id = fg.group_id
    LEFT JOIN individual_makes_transaction imt ON imt.transaction_id = th.transaction_id AND imt.individual_id = %s
    WHERE th.is_settled = 0
    AND th.payee_id = %s
    GROUP BY fg.group_id, fg.group_name
    """

    try:
        cur.execute(query, [get_userID(), get_userID()])
        rows = cur.fetchall()

        if not rows:
            print("No groups with outstanding balances")
        else:
            for row in rows:
                group_id, group_name, balance = row
                print("Group ID:", group_id)
                print("Group Name:", group_name)
                print("Outstanding Balance:", balance)
                print()

    except mariadb.Error as e:
        print(f"Error: {e}")

# Close Connection
def close_connection():
    conn.close()