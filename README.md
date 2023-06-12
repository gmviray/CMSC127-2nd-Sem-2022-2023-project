<a id= "readme-top" name="readme-top"></a>
<h1 align="center"> PENNYWISE </h1>

<p align="center">Pennywise is an expense tracking application for effortless expense management and seamless sharing with friends and family. Say goodbye to the hassle of tracking who owes whom. With Pennywise, you can easily manage your personal and group expenses, making it a piece of cake to keep tabs on the money you borrowed and/or lended over time.</p>

<div align="center">


![MariaDB][mariadb_link]
![Python][python_link]

</div>

### Table of Contents
1. [Getting Started](#getting-started)
    - [Installation](#installation-guide)
    - [Usage](#instruction-guide)
        - ['Add an expense' Functions](#add-expense)
            - Add a Grouped Expense
            - Add a Paired Expense
        - ['Add a friend' Function](#add-friend)
        - ['Add a group' Function](#add-group)
        - ['Delete' Function](#delete_func)
            - Delete a Transaction
            - Delete a Friend
            - Delete a Group
            - Delete a Friend from a Group
        - ['Search for a transaction' Functions](#search_transaction)
            - Search a Transaction through Transaction ID
            - Search a Transaction made with a Group
            - Search a Transaction made without a Group
            - Search a Transaction by Month
        - ['Search for a friend' Functions](#search_friend)
            - Search by ID
            - Search by Name
            - Search by Email
        - ['Search for a group' Functions](#search_group)
            - Search by Group ID
            - Search by Group Name
        - ['View' Functions](#view_func)

2. [Authors](#authors)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started <a id="getting-started" name='getting-started'></a>

### Installation Guide <a id="installation-guide" name='installation-guide'></a>

**Download and install the recent version of MariaDB.**
```sh
https://mariadb.org/download/
```

**Download and install the recent version of MariaDB Connector\C.**
```sh
https://mariadb.com/downloads/connectors/
```

**After installation of MariaDB Connector/C download and install MariaDB Connector/Python with the following command.**
```sh
pip3 install mariadb
```

**Install the necessary libraries.**
```sh
python -m pip install -U git+https://github.com/jazzband/prettytable
```

**Reference guide for prettytable.**
```sh
https://pypi.org/project/prettytable/
```

**Download the setup_mysql.sql. Then, open a terminal and go to the directory of the sql file.**
```sh
cd /Users/YourUsername/File
```

**Log in to the root user of MariaDB.**
```sh
mysql -u root -p
```

**Once you are logged in to the MariaDB server, you can source and execute the setup_mysql.sql.**
```sh
source setup_mysql.sql
```
**If the SQL script file is located in a different directory, you can provide the full file path instead:**
```sh
source /path/to/setup_mysql.sql
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Usage <a id="instruction-guide" name='instruction-guide'></a>

**Open the terminal on your computer. Navigate to the directory where the project files are located using the 'cd' command.**

**Then, run the program.**
```sh
python app.py
```

**The menu will display various options. Select which action you want to perform. Enter the corresponding number as input.**

### **'Add an expense' Functions**<a id="add-expense" name='add-expense'></a>

**1. Add a grouped expense**
```sh
add > add a transaction > expense > (is this a group transaction) y > (enter group id) > (enter payee id) > (enter total amount) > (enter transaction description)
```
Details needed:
```sh
- Group ID
- Payee ID
- Amount of expense shared within the group
- Transaction Description
```

**2. Add a paired expense**
```sh
add > add a transaction > expense > (is this a group transaction) n > (enter payee id) > (enter borrower id) > (enter total amount) > (enter transaction description)
```

Details needed:
```sh
- Payee ID
- Borrower ID
- Amount of expense shared within two people
- Transaction Description
```
### **'Add a friend' Function**<a id="add-friend" name='add-friend'></a>
```sh
add > add a friend > (enter friend's first name) > (enter friend's middle initial, if applicable) > (enter friend's last name) > (enter friend's email)
```
Details needed:
```sh
- First name
- Middle Initial, if applicable
- Last name
- Email
```
### **'Add a group' Function**<a id="add-group" name='add-group'></a>
```sh
add > add a group > (enter group name)
```
If user want to add individuals upon creating the group:
```sh
(enter member's individual id)
```

Details needed:
```sh
- Group Name
- Member's individual id, if user wants to add members to the group
```

### **'Delete' Functions**<a id="delete_func" name='delete_func'></a>
**1. Delete a transaction made with a group**
```sh
delete > delete a transaction > delete transaction made with a group > (enter transaction ID you want to delete)
```
Details needed:
```sh
- transaction ID
```

**2. Delete a transaction made without a group**
```sh
delete > delete a transaction > delete transaction made without a group > (enter transaction ID you want to delete)
```
Details needed:
```sh
- transaction ID
```
**3. Delete a friend**
```sh
delete > delete a friend > (enter friend's ID you want to delete)
```
Details needed:
```sh
- friend's ID
```
**4. Delete a friend from a group**
```sh
delete > delete a friend from a group > (enter your friend's ID you want to delete from a group) > (enter the group's ID you want to remove your friend from)
```
Details needed:
```sh
- friend's ID
- group ID
```
**3. Delete a group**
```sh
delete > delete a group > (enter group's ID you want to delete)
```
Details needed:
```sh
- group ID
```
### **'Search a transaction' Functions**<a id="search_transaction" name='search_transaction'></a>
**1. Search a transaction through transaction ID**
```sh
search > search a transaction > search by transaction ID > (enter transaction ID)
```

Details needed:
```sh
- transaction ID
```
**2. Search a transaction made with a group**
```sh
search > search a transaction > search transaction made with a group > (enter transaction ID)
```
Details needed:
```sh
- transaction ID
```
**3. Search a transaction made without a group**
```sh
search > search a transaction > search transaction made without a group > (enter transaction ID)
```
Details needed:
```sh
- transaction ID
```
**4. Search a transaction by month**
```sh
search > search a transaction > search by month > (enter month (1-12))
```
Details needed:
```sh
- Month's order in a year (1-12)
```
### **'Search a friend' Functions**<a id="search_friend" name='search_friend'></a>
**1. Search by ID**
```sh
search > search a friend > search by ID > (enter individual_id)
```
Details needed:
```sh
- Friend's individual ID
```
**2. Search by Name**
```sh
search > search a friend > search by Name > (enter friend's name)
```
Details needed:
```sh
- Friend's name
```

**3. Search by Email**
```sh
search > search a friend > search by Email > (enter friend's email)
```

Details needed:
```sh
- Friend's email address
```
### **'Search a group' functions**<a id="search_group" name='search_group'></a>
**1. Search by group ID**
```sh
search > search a group > search by group ID > (enter group ID)
```
Details needed:
```sh
- Group ID
```
**1. Search by group Name**
```sh
search > search a group > search by group Name > (enter group name)
```
Details needed:
```sh
- Group Name
```

### **'View' functions**<a id="view_func" name='view_func'></a>
**1. View transactions made within a month**
```sh
view > view transactions made within a month
```
Details needed:
```sh
- None
```

**2. View transactions made with a friend**
```sh
view > view transactions made with a friend > (enter friend's individual ID)
```
Details needed:
```sh
- Friend's individual ID
```

**3. View transactions made with a group**
```sh
view > view transactions made with a group > (enter group ID)
```
Details needed:
```sh
- Group ID
```

**4. View current balance from all expenses**
```sh
view > view current balance from all expenses
```
Details needed:
```sh
- None
```

**5. View all friends with outstanding balance**
```sh
view > view all friends with outstanding balance
```
Details needed:
```sh
- None
```

**6. View all groups**
```sh
view > view all groups
```
Details needed:
```sh
- None
```

**7. View all groups with an outstanding balance**
```sh
view > view all groups with an outstanding balance
```
Details needed:
```sh
- None
```




<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Authors <a id="authors" name='authors'></a>

**Karl Kenneth Owen D. Olipas**

kdolipas@up.edu.ph

**Jerico Luis A. Ungos**

jaungos@up.edu.ph

**Geraldine Marie M. Viray**

gmviray@up.edu.ph

[mariadb_link]: https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white
[python_link]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54