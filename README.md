<a name="readme-top"></a>
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

**For the 'add' functions**

**For the 'delete' functions**

**For the 'search' functions**

**For the 'view' functions**

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