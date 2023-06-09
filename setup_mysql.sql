DROP DATABASE IF EXISTS moneytracker;

CREATE OR REPLACE USER 'pennywise'@'localhost' IDENTIFIED BY 'ilovecmsc127';
CREATE DATABASE moneytracker;
GRANT ALL ON moneytracker.* TO 'pennywise'@'localhost';

USE moneytracker;

-- Remember to delete this table as this is for practicing purposes only
CREATE TABLE expense (
    expense_id INT(4) NOT NULL AUTO_INCREMENT,
    expense_value DECIMAL(20,2) NOT NULL,
    PRIMARY KEY (expense_id)
);

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
	payer_id INT(9) NOT NULL,
	number_of_users_involved INT(4) NOT NULL,
	is_settled BOOLEAN NOT NULL,
	transaction_description VARCHAR(1000),
	total_amount DECIMAL(20, 2) NOT NULL,
	contribution DECIMAL(20, 2) NOT NULL,
	type_of_transaction VARCHAR(10) NOT NULL,
	group_id INT(9),
    PRIMARY KEY (transaction_id),
    CONSTRAINT transactionHistory_group_id_fk FOREIGN KEY(group_id) REFERENCES friend_group(group_id),
    CONSTRAINT transactionHistory_payer_id_fk FOREIGN KEY(payer_id) REFERENCES individual(individual_id)
);

CREATE TABLE individual_makes_transaction (
	individual_id INT(9) NOT NULL,
	transaction_id INT(9) NOT NULL,
    PRIMARY KEY (individual_id, transaction_id),
    CONSTRAINT individualTransaction_individual_id_fk FOREIGN KEY(individual_id) REFERENCES individual(individual_id),
    CONSTRAINT individualTransaction_transaction_id_fk FOREIGN KEY(transaction_id) REFERENCES transaction_history(transaction_id)
);


-- =================================================================================================
-- Dump Values
-- INSERT 
INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES ("John", "DC", "Doe", "johndoe@email.com", True, 26.25);

INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES ("Jane", "A", "Doe", "janedoe@email.com", False,
    262.25);

INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES ("Taylor", "C", "Batumbakal", "taylorbatumbakal@email.com", False, 26000002.25);

INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES ("Uvuvwevwevwe Onyetenvewve Ugwemubwem", NULL, "Ossas", "uvuvwevwevwe@email.com", False, 34567.25);

INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES ("Hubert Blaine", NULL, "Wolfeschlegelsteinhausenbergerdorff", "hubertblaine@email.com", False, 12678.00);

INSERT INTO friend_group (group_name, number_of_members) VALUES ("spiC3G1rLz", 10);

INSERT INTO friend_group (group_name, number_of_members) VALUES ("Frontrow", 5);

INSERT INTO individual_belongs_friend_group VALUES (1, 1);

INSERT INTO individual_belongs_friend_group VALUES (2, 1);

INSERT INTO individual_belongs_friend_group VALUES (3, 1);
		
INSERT INTO individual_belongs_friend_group VALUES (4, 1);

INSERT INTO individual_belongs_friend_group VALUES (1, 2);

INSERT INTO individual_belongs_friend_group VALUES (5, 2);

INSERT INTO individual_belongs_friend_group VALUES (4, 2);