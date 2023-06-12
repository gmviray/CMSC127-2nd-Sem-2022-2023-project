DROP DATABASE IF EXISTS moneytracker;

CREATE OR REPLACE USER 'pennywise'@'localhost' IDENTIFIED BY 'ilovecmsc127';
CREATE DATABASE moneytracker;
GRANT ALL ON moneytracker.* TO 'pennywise'@'localhost';

USE moneytracker;

CREATE TABLE individual (
    individual_id INT(9) NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    middle_initial VARCHAR(4),
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(65) NOT NULL,
    is_user BOOLEAN NOT NULL,
    balance DECIMAL(20,2) NOT NULL,
    PRIMARY KEY (individual_id)
);

CREATE TABLE friend_group (
    group_id INT(9) NOT NULL AUTO_INCREMENT,
    group_name VARCHAR(50) NOT NULL,
    number_of_members INT(4) NOT NULL,
    PRIMARY KEY (group_id)
);

CREATE TABLE individual_belongs_friend_group (
    individual_id INT(9) NOT NULL,
    group_id INT(9) NOT NULL,
    PRIMARY KEY (individual_id, group_id),
    CONSTRAINT individualBelongs_individual_id_fk FOREIGN KEY(individual_id) REFERENCES individual(individual_id),
    CONSTRAINT individualBelongs_group_id_fk FOREIGN KEY(group_id) REFERENCES friend_group(group_id)
);

CREATE TABLE transaction_history (
    transaction_id INT(9) NOT NULL AUTO_INCREMENT,
    date_issued DATE NOT NULL,
    is_group BOOLEAN NOT NULL,
	payee_id INT(9) NOT NULL,
	number_of_users_involved INT(4) NOT NULL,
	is_settled BOOLEAN NOT NULL,
	transaction_description VARCHAR(1000) NOT NULL,
	total_amount DECIMAL(20, 2) NOT NULL,
	contribution DECIMAL(20, 2) NOT NULL,
	type_of_transaction VARCHAR(10) NOT NULL,
	group_id INT(9),
    PRIMARY KEY (transaction_id),
    CONSTRAINT transactionHistory_group_id_fk FOREIGN KEY(group_id) REFERENCES friend_group(group_id),
    CONSTRAINT transactionHistory_payee_id_fk FOREIGN KEY(payee_id) REFERENCES individual(individual_id)
);

CREATE TABLE individual_makes_transaction (
	individual_id INT(9) NOT NULL,
	transaction_id INT(9) NOT NULL,
    transaction_amount DECIMAL(20, 2) NOT NULL,
    PRIMARY KEY (individual_id, transaction_id),
    CONSTRAINT individualTransaction_individual_id_fk FOREIGN KEY(individual_id) REFERENCES individual(individual_id),
    CONSTRAINT individualTransaction_transaction_id_fk FOREIGN KEY(transaction_id) REFERENCES transaction_history(transaction_id)
);