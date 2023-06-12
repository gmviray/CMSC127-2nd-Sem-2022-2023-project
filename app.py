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

    print("\n╔═══════════════════════╗")
    print("║         MENU          ║")
    print("╠═══════════════════════╣")
    print("║ [1] Add               ║")
    print("║ [2] Delete            ║")
    print("║ [3] Search            ║")
    print("║ [4] Update            ║")
    print("║ [5] View              ║")
    print("║ [0] Exit              ║")
    print("╚═══════════════════════╝")

    choice = input("\n>> Enter your choice: ")

    if choice == "1":
        print("\n╔═══════════════════════╗")
        print("║         ADD           ║")
        print("╠═══════════════════════╣")
        print("║ [1] Add a transaction ║")
        print("║ [2] Add a friend      ║")
        print("║ [3] Add a group       ║")
        print("║ [0] Back to Menu      ║")
        print("╚═══════════════════════╝")

        sub_choice = input("\n>> Enter your choice: ")

        if sub_choice == "1":
            add_transaction()

        elif sub_choice == "2":
            add_user()

        elif sub_choice == "3":
            add_group()
        
        elif sub_choice == "0":
            print("\n╔═══════════════════════╗")
            print("║     BACK TO MENU      ║")
            print("╚═══════════════════════╝")

    elif choice == "2":
        print("\n╔═══════════════════════╗")
        print("║        DELETE         ║")
        print("╠═══════════════════════╣")
        print("║ [1] Delete a          ║")
        print("║     transaction       ║")
        print("║ [2] Delete a friend   ║")
        print("║ [3] Delete a friend   ║")
        print("║     from a group      ║")
        print("║ [4] Delete a group    ║")
        print("║ [0] Back to Menu      ║")
        print("╚═══════════════════════╝")

        sub_choice = input("\n>> Enter your choice: ")

        if sub_choice == "1":
            delete_transactionMadeWithOrWithoutAGroup(choice)
        elif sub_choice == "2":
            delete_friend()
        elif sub_choice == "3":
            delete_friendFromGroup()
        elif sub_choice == "4":
            delete_group()
        elif sub_choice == "0":
            print("\n╔═══════════════════════╗")
            print("║     BACK TO MENU      ║")
            print("╚═══════════════════════╝")
        else:
            print("\n╔═══════════════════════╗")
            print("║    Invalid choice.    ║")
            print("╚═══════════════════════╝")
            # print('Invalid sub-choice!')

    elif choice == "3":
        print("\n╔═══════════════════════╗")
        print("║        SEARCH         ║")
        print("╠═══════════════════════╣")
        print("║ [1] Search a          ║")
        print("║     transaction       ║")
        print("║ [2] Search a friend   ║")
        print("║ [3] Search a group    ║")
        print("║ [0] Back to Menu      ║")
        print("╚═══════════════════════╝")

        sub_choice = input("\n>> Enter your choice: ")

        if sub_choice == "1":
            print("\n╔═══════════════════════╗")
            print("║       SEARCH BY       ║")
            print("║    TRANSACTION ID     ║")
            print("╠═══════════════════════╣")
            print("║ [1] Search transaction║")
            print("║     made with a group ║")
            print("║ [2] Search transaction║")
            print("║     made without group║")
            print("║ [3] Search by month   ║")
            print("║ [0] Back to Menu      ║")
            print("╚═══════════════════════╝")
            search_sub_choice = input("\n>> Enter your choice: ")
            if search_sub_choice == '1':
                transaction_id = input('>> Enter transaction ID: ')
                search_transactionById(transaction_id)
            elif search_sub_choice == '2' or  search_sub_choice == '3':
                search_transactionMadeWithOrWithoutAGroup(search_sub_choice)
            elif search_sub_choice == '4':
                while True:
                    month = input('>> Enter month(1-12): ')
                    try:
                        if int(month) > 12 or int(month) < 1:
                            print("\n╔═══════════════════════╗")
                            print("║    Invalid input.     ║")
                            print("╚═══════════════════════╝")
                            # print('Invalid input!')
                        else:
                            search_transactionByMonth(month)
                            break
                    except ValueError:
                        print("\n╔═══════════════════════╗")
                        print("║     Invalid input.    ║")  
                        print("║     Please enter      ║")  
                        print("║      an integer.      ║")    
                        print("╚═══════════════════════╝")
                        continue
            elif search_sub_choice == "0":
                print("\n╔═══════════════════════╗")
                print("║     BACK TO MENU      ║")
                print("╚═══════════════════════╝")
            else:
                print("\n╔═══════════════════════╗")
                print("║    Invalid choice.    ║")
                print("╚═══════════════════════╝")
                # print('Invalid sub-choice!')

        elif sub_choice == "2":
            search_friend()

        elif sub_choice == "3":
            print("\n╔═══════════════════════╗")
            print("║ [1] Search by group ID║")
            print("║ [2] Search Name       ║")
            print("║ [0] Back to Menu      ║")
            print("╚═══════════════════════╝")
            search_sub_choice = input("\n>> Enter your choice: ")
            if search_sub_choice == '1':
                group_id = input('>> Enter group ID: ')
                search_groupById(group_id)
            elif search_sub_choice == '2':
                name = input('>> Enter group name: ')
                search_groupByName(name)
            elif search_sub_choice == "0":
                print("\n╔═══════════════════════╗")
                print("║     BACK TO MENU      ║")
                print("╚═══════════════════════╝")
            else:
                print("\n╔═══════════════════════╗")
                print("║    Invalid choice.    ║")
                print("╚═══════════════════════╝")
                # print('Invalid sub-choice!')
        elif sub_choice == "0":
            print("\n╔═══════════════════════╗")
            print("║     BACK TO MENU      ║")
            print("╚═══════════════════════╝")
        else:
            print("\n╔═══════════════════════╗")
            print("║    Invalid choice.    ║")
            print("╚═══════════════════════╝")
            # print('\nInvalid choice!')

    elif choice == "4":
        print("\n╔═══════════════════════╗")
        print("║        UPDATE         ║")
        print("╠═══════════════════════╣")
        print("║ [1] Update a          ║")
        print("║     transaction       ║")
        print("║     description       ║")
        print("║ [2] Update a friend   ║")
        print("║ [3] Update a group    ║")
        print("║     name              ║")
        print("║ [0] Back to Menu      ║")
        print("╚═══════════════════════╝")
        # print("\n----- Update -----")
        # print("1. Update a transaction description")
        # print("2. Update a friend")
        # print("3. Update a group name")

        sub_choice = input("\n>> Enter your choice: ")

        if sub_choice == "1":
            transaction_id = input('\n>> Enter transaction ID to be edited: ')
            if search_transactionById(transaction_id):
                search_transactionById(transaction_id)
                while True:
                    transaction_description = input("\n>> Enter UPDATED description: ")[:1000]  # Limit to 1000 characters
                    if transaction_description.strip():
                        break
                    else:
                        print("\n╔═══════════════════════╗")
                        print("║ Description cannot be ║")
                        print("║   empty. Please try   ║")
                        print("║        again.         ║")
                        print("╚═══════════════════════╝")
                update_transactionById(transaction_id, transaction_description)
            else:
                print("\n╔═══════════════════════╗")
                print("║ Transaction not found.║")    
                print("╚═══════════════════════╝")

        elif sub_choice == "2":
            friend_id = input("\n>> Enter friend ID to be edited: ")
            if search_friendById(friend_id):
                print("\n╔═══════════════════════╗")
                print("║ [1] Update first name ║")
                print("║ [2] Update middle     ║")
                print("║     initial           ║")
                print("║ [3] Update last name  ║")
                print("║ [4] Update email      ║")
                print("║ [0] Back to Menu      ║")
                print("╚═══════════════════════╝")
                update_sub_choice = input("\nEnter your choice: ")
                if update_sub_choice == '1':
                    while True:
                        updated_name = input(">> Enter UPDATED first name: ")[:50]  # Limit to 50 characters
                        if updated_name.strip():
                            break
                        else:
                            print("\n╔═══════════════════════╗")
                            print("║    Field cannot be    ║")
                            print("║   empty. Please try   ║")
                            print("║        again.         ║")
                            print("╚═══════════════════════╝")
                            # print("Field cannot be empty. Please try again.")
                    update_friendFirstName(friend_id, updated_name)
                elif update_sub_choice == '2':
                    while True:
                        updated_name = input(">> Enter UPDATED middle initial: ")[:4]  # Limit to 4 characters
                        if updated_name.strip():
                            break
                        else:
                            print("\n╔═══════════════════════╗")
                            print("║    Field cannot be    ║")
                            print("║   empty. Please try   ║")
                            print("║        again.         ║")
                            print("╚═══════════════════════╝")
                    update_friendMiddleInitial(friend_id, updated_name)
                elif update_sub_choice == '3':
                    while True:
                        updated_name = input(">> Enter UPDATED last name: ")[:50]  # Limit to 50 characters
                        if updated_name.strip():
                            break
                        else:
                            print("\n╔═══════════════════════╗")
                            print("║    Field cannot be    ║")
                            print("║   empty. Please try   ║")
                            print("║        again.         ║")
                            print("╚═══════════════════════╝")
                    update_friendLastName(friend_id, updated_name)
                elif update_sub_choice == '4':
                    while True:
                        updated_email = input("Enter UPDATED email: ")[:65]  # Limit to 65 characters
                        if updated_email.strip():
                            break
                        else:
                            print("\n╔═══════════════════════╗")
                            print("║    Field cannot be    ║")
                            print("║   empty. Please try   ║")
                            print("║        again.         ║")
                            print("╚═══════════════════════╝")
                    update_friendEmail(friend_id, updated_email)
                elif update_sub_choice == "0":
                    print("\n╔═══════════════════════╗")
                    print("║     BACK TO MENU      ║")
                    print("╚═══════════════════════╝")
                else:
                    print("\n╔═══════════════════════╗")
                    print("║    Invalid choice.    ║")
                    print("╚═══════════════════════╝")

        elif sub_choice == "3":
            group_id = input('\n>> Enter group ID to be edited: ')
            if search_groupById(group_id):
                while True:
                    group_name = input("\n>> Enter UPDATED group name: ")[:50]  # Limit to 50 characters
                    if group_name.strip():
                        break
                    else:
                        print("\n╔═══════════════════════╗")
                        print("║ Group name cannot be  ║")
                        print("║  empty. Please try    ║")
                        print("║       again.          ║")
                        print("╚═══════════════════════╝")
                        # print("Group name cannot be empty. Please try again.")
                update_groupById(group_id, group_name)
            else:
                print("\n╔═══════════════════════╗")
            print("║   Group not found.    ║")
            print("╚═══════════════════════╝")
        elif sub_choice == "0":
            print("\n╔═══════════════════════╗")
            print("║     BACK TO MENU      ║")
            print("╚═══════════════════════╝")
        else:
            print("\n╔═══════════════════════╗")
            print("║    Invalid choice.    ║")
            print("╚═══════════════════════╝")

    elif choice == "5":
        print("\n╔═══════════════════════╗")
        print("║         VIEW          ║")
        print("╠═══════════════════════╣")
        print("║ [1] View transactions ║")
        print("║     made within       ║")
        print("║     a month           ║")
        print("║ [2] View transactions ║")
        print("║     made with         ║")
        print("║     a friend          ║")
        print("║ [3] View transactions ║")
        print("║     made with         ║")
        print("║     a group           ║")
        print("║ [4] View current      ║")
        print("║     balance from all  ║")
        print("║     expenses          ║")
        print("║ [5] View all friends  ║")
        print("║     with outstanding  ║")
        print("║     balance           ║")
        print("║ [6] View all groups   ║")
        print("║ [7] View all groups   ║")
        print("║     with outstanding  ║")
        print("║     balance           ║")
        print("║ [0] Back to Menu      ║")
        print("╚═══════════════════════╝")

        sub_choice = input("\n>> Enter your choice: ")

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
        print("\n╔═══════════════════════╗")
        print("║         EXIT.         ║")
        print("╚═══════════════════════╝")
        close_connection()
        break

    else:
        print("\n╔═══════════════════════╗")
        print("║    Invalid choice.    ║")
        print("║   Please try again.   ║")
        print("╚═══════════════════════╝")
