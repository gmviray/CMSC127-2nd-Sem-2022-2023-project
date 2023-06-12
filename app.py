from functions import *
from prettytable import PrettyTable

expenses = []
friends = []
groups = []
sub_choice = 0

menuTable = PrettyTable(["PENNYWISE EXPENSE TRACKER"])

while True:
    if check_user() == True:
        add_user()
        pass

    print("\n----- Menu -----")
    # print("1. Expenses")
    # print("2. Friends")
    # print("3. Groups")

    # menuTable.add_row(["Expenses"])
    # menuTable.add_row(["Friends"])
    # menuTable.add_row(["Groups"])



    print("1. Add")
    print("2. Delete")
    print("3. Search")
    print("4. Update")
    print("5. View")
    print("0. Exit App")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\n----- Add -----")
        print("1. Add a transaction")
        print("2. Add a friend")
        print("3. Add a group")

        sub_choice = input("Enter your sub-choice: ")

        if sub_choice == "1":
            add_transaction()

        elif sub_choice == "2":
            add_user()

        elif sub_choice == "3":
            add_group()

    elif choice == "2":
        print("\n----- Delete -----")
        print("1. Delete a transaction")
        print("2. Delete a friend")
        print("3. Delete a group")
        print("4. Delete a friend from a group")

        sub_choice = input("Enter your sub-choice: ")

        if sub_choice == "1":
            expense = input("Enter the expense to delete: ")
            if expense in expenses:
                expenses.remove(expense)
                print("Expense deleted.")
            else:
                print("Expense not found.")

        elif sub_choice == "2":
            friend = input("Enter friend's name to delete: ")
            if friend in friends:
                friends.remove(friend)
                print("Friend deleted.")
            else:
                print("Friend not found.")

        elif sub_choice == "3":
            group = input("Enter group's name to delete: ")
            if group in groups:
                groups.remove(group)
                print("Group deleted.")
            else:
                print("Group not found.")

    elif choice == "3":
        print("\n----- Search -----")
        print("1. Search a transaction")
        print("2. Search a friend")
        print("3. Search a group")

        sub_choice = input("Enter your sub-choice: ")

        if sub_choice == "1":
            search_sub_choice = input("""\n1. Search by transaction ID
2. Search transaction made with a group
3. Search transaction made without a group 
4. Search by month
Enter your sub-choice: """)
            if search_sub_choice == '1':
                transaction_id = input('Enter transaction ID: ')
                search_transactionById(transaction_id)
            elif search_sub_choice == '2' or  search_sub_choice == '3':
                search_transactionMadeWithOrWithoutAGroup(search_sub_choice)
            elif search_sub_choice == '4':
                while True:
                    month = input('Enter month(1-12): ')
                    try:
                        if int(month) > 12 or int(month) < 1:
                            print('Invalid input!')
                        else:
                            search_transactionByMonth(month)
                            break
                    except ValueError:
                        print("Invalid input. Please enter an integer.\n")
                        continue
            else:
                print('Invalid sub-choice!')

        elif sub_choice == "2":
            search_friend()

        elif sub_choice == "3":
            search_sub_choice = input("\n1. Search by group ID\n2. Search Name\nEnter your sub-choice: ")
            if search_sub_choice == '1':
                group_id = input('Enter group ID: ')
                search_groupById(group_id)
            elif search_sub_choice == '2':
                name = input('Enter group name: ')
                search_groupByName(name)
            else:
                print('Invalid sub-choice!')

        else:
            print('\nInvalid choice!')

    elif choice == "4":
        print("\n----- Update -----")
        print("1. Update a transaction description")
        print("2. Update a friend")
        print("3. Update a group name")

        sub_choice = input("Enter your sub-choice: ")

        if sub_choice == "1":
            transaction_id = input('\nEnter transaction ID to be edited: ')
            if search_transactionById(transaction_id):
                search_transactionById(transaction_id)
                while True:
                    transaction_description = input("\nEnter UPDATED description: ")[:1000]  # Limit to 1000 characters
                    if transaction_description.strip():
                        break
                    else:
                        print("Transaction description cannot be empty. Please try again.")
                update_transactionById(transaction_id, transaction_description)
            else:
                print("\nTransaction not found.")

        elif sub_choice == "2":
            friend_id = input("\nEnter friend ID to be edited: ")
            if search_friendById(friend_id):
                update_sub_choice = input("1. Update first name\n2. Update middle initial\n3. Update last name\n4. Update email\nEnter your sub-choice: ")
                if update_sub_choice == '1':
                    while True:
                        updated_name = input("Enter UPDATED first name: ")[:50]  # Limit to 50 characters
                        if updated_name.strip():
                            break
                        else:
                            print("Field cannot be empty. Please try again.")
                    update_friendFirstName(friend_id, updated_name)
                elif update_sub_choice == '2':
                    while True:
                        updated_name = input("Enter UPDATED middle initial: ")[:4]  # Limit to 4 characters
                        if updated_name.strip():
                            break
                        else:
                            print("Field cannot be empty. Please try again.")
                    update_friendMiddleInitial(friend_id, updated_name)
                elif update_sub_choice == '3':
                    while True:
                        updated_name = input("Enter UPDATED last name: ")[:50]  # Limit to 50 characters
                        if updated_name.strip():
                            break
                        else:
                            print("Field cannot be empty. Please try again.")
                    update_friendLastName(friend_id, updated_name)
                elif update_sub_choice == '4':
                    while True:
                        updated_email = input("Enter UPDATED email: ")[:65]  # Limit to 65 characters
                        if updated_email.strip():
                            break
                        else:
                            print("Field cannot be empty. Please try again.")
                    update_friendEmail(friend_id, updated_email)
                else:
                    print('Invalid sub-choice!')

        elif sub_choice == "3":
            group_id = input('\nEnter group ID to be edited: ')
            if search_groupById(group_id):
                while True:
                    group_name = input("\nEnter UPDATED group name: ")[:50]  # Limit to 50 characters
                    if group_name.strip():
                        break
                    else:
                        print("Group name cannot be empty. Please try again.")
                update_groupById(group_id, group_name)
            else:
                print("\nGroup not found.")

        else:
            print('\nInvalid choice!')

    elif choice == "5":
        print("\n----- View -----")
        print("1. View transactions made within a month")
        print("2. View transactions made with a friend")
        print("3. View transactions made with a group")
        print("4. View current balance from all expenses")
        print("5. View all friends with outstanding balance")
        print("6. View all groups")
        print("7. View all groups with an outstanding balance")

        sub_choice = input("Enter your sub-choice: ")

        if sub_choice == "1":
            view_transactionsWithinAMonth()

        elif sub_choice == "2":
            view_transactionsWithFriend()

        elif sub_choice == "3":
            view_transactionsWithGroup()

        elif sub_choice == "4":
            view_balance()

        elif sub_choice == "5":
            view_friendsWithOutstandingBalances()

        elif sub_choice == "6":
            view_groups()

        elif sub_choice == "7":
            view_groupsWithOutstandingBalances()
            # print("Logic to view all groups with an outstanding balance")

    elif choice == "0":
        print("exit")
        break

    else:
        print("Invalid choice. Please try again.")
