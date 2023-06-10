from functions import *

expenses = []
friends = []
groups = []
sub_choice = 0

while True:
    if check_user() == True:
        add_user()
        pass

    print("\n----- Menu -----")
    print("1. Add")
    print("2. Delete")
    print("3. Search")
    print("4. Update")
    print("5. View")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\n----- Add -----")
        print("1. Add an expense")
        print("2. Add a friend")
        print("3. Add a group")

        sub_choice = input("Enter your sub-choice: ")

        if sub_choice == "1":
            add_transaction()

        elif sub_choice == "2":
            add_user()
            view_users()

        elif sub_choice == "3":
            group = input("Enter group's name: ")
            groups.append(group)
            print("Group added.")

    elif choice == "2":
        print("\n----- Delete -----")
        print("1. Delete an expense")
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
        print("1. Search an expense")
        print("2. Search a friend")
        print("3. Search a group")

        sub_choice = input("Enter your sub-choice: ")

        if sub_choice == "1":
            expense = input("Enter expense to search: ")
            if expense in expenses:
                print("Expense found.")
            else:
                print("Expense not found.")

        elif sub_choice == "2":
            friend = input("Enter friend's name to search: ")
            if friend in friends:
                print("Friend found.")
            else:
                print("Friend not found.")

        elif sub_choice == "3":
            group = input("Enter group's name to search: ")
            if group in groups:
                print("Group found.")
            else:
                print("Group not found.")

    elif choice == "4":
        print("----- Update -----")
        print("1. Update an expense")
        print("2. Update a friend")
        print("3. Update a group")

        sub_choice = input("Enter your sub-choice: ")

        if sub_choice == "1":
            expense = input("Enter expense to update: ")
            if expense in expenses:
                new_expense = input("Enter new expense: ")
                index = expenses.index(expense)
                expenses[index] = new_expense
                print("Expense updated.")
            else:
                print("Expense not found.")

        elif sub_choice == "2":
            friend = input("Enter friend's name to update: ")
            if friend in friends:
                new_friend = input("Enter new friend's name: ")
                index = friends.index(friend)
                friends[index] = new_friend
                print("Friend updated.")
            else:
                print("Friend not found.")

        elif sub_choice == "3":
            group = input("Enter group's name to update: ")
            if group in groups:
                new_group = input("Enter new group's name: ")
                index = groups.index(group)
                groups[index] = new_group
                print("Group updated.")
            else:
                print("Group not found.")

    elif choice == "5":
        print("\n----- View -----")
        print("1. View expenses made within a month")
        print("2. View expenses made with a group")
        print("3. View expenses made with a friend")
        print("4. View current balance from all expenses")
        print("5. View all friends with outstanding balance")
        print("6. View all groups")
        print("7. View all groups with an outstanding balance")

        sub_choice = input("Enter your sub-choice: ")

        if sub_choice == "1":
            print("Logic to view expenses made within a month")

        elif sub_choice == "2":
            print("Logic to view expenses made with a group")

        elif sub_choice == "3":
            print("Logic to view expenses made with a friend")

        elif sub_choice == "4":
            print("Logic to view current balance from all expenses")

        elif sub_choice == "5":
            print("Logic to view all friends with outstanding balance")

        elif sub_choice == "6":
            view_groups()

        elif sub_choice == "7":
            print("Logic to view all groups with an outstanding balance")

    elif choice == "0":
        print("exit")
        break

    else:
        print("Invalid choice. Please try again.")
