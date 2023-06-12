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
-- =====================================================================

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


-- =================================================================================================
-- Dump Values
-- INSERT 
INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES ("John", "DC", "Doe", "johndoe@email.com", True, 0);

INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES ("Jane", "A", "Doe", "janedoe@email.com", False, 0);

INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES ("Taylor", "C", "Batumbakal", "taylorbatumbakal@email.com", False, 0);

INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES ("Uvuvwevwevwe Onyetenvewve Ugwemubwem", NULL, "Ossas", "uvuvwevwevwe@email.com", False, 0);

INSERT INTO individual (first_name, middle_initial, last_name, email, is_user, balance) VALUES ("Hubert Blaine", NULL, "Wolfeschlegelsteinhausenbergerdorff", "hubertblaine@email.com", False, 0);

INSERT INTO friend_group (group_name, number_of_members) VALUES ("spiC3G1rLz", 4);

INSERT INTO friend_group (group_name, number_of_members) VALUES ("Frontrow", 3);

INSERT INTO individual_belongs_friend_group VALUES (1, 1);

INSERT INTO individual_belongs_friend_group VALUES (2, 1);

INSERT INTO individual_belongs_friend_group VALUES (3, 1);
		
INSERT INTO individual_belongs_friend_group VALUES (4, 1);

INSERT INTO individual_belongs_friend_group VALUES (1, 2);

INSERT INTO individual_belongs_friend_group VALUES (5, 2);

INSERT INTO individual_belongs_friend_group VALUES (4, 2);

-- =================================================================================================
-- Nongroup expense
INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES ("2023-04-25", FALSE, 1, 5, FALSE, "Expense # 1", 2650.00, 530.00, "EXPENSE", NULL);

INSERT INTO individual_makes_transaction VALUES (1, 1, 0);

UPDATE individual SET balance = balance + 2120 WHERE individual_id = 1;

INSERT INTO individual_makes_transaction VALUES (2, 1, -530.00);

UPDATE individual SET balance = balance - 530 WHERE individual_id = 2;

INSERT INTO individual_makes_transaction VALUES (3, 1, -530.00);

-- UPDATE individual SET balance = balance - 530 WHERE individual_id = 3;

-- INSERT INTO individual_makes_transaction VALUES (4, 1, -530.00);

UPDATE individual SET balance = balance - 530 WHERE individual_id = 4;

INSERT INTO individual_makes_transaction VALUES (5, 1, -530.00);

UPDATE individual SET balance = balance - 530 WHERE individual_id = 5;
-- =================================================================================================
-- Nongroup Settlement
INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES ("2023-05-26", FALSE, 1, 2, TRUE, "Payment # 1", 2650.00, 530.00, "SETTLEMENT", NULL);

INSERT INTO individual_makes_transaction VALUES (2, 2, 530.00);

UPDATE individual_makes_transaction SET transaction_amount = (SELECT transaction_amount FROM individual_makes_transaction WHERE transaction_id = 2 AND individual_id = 2) + transaction_amount WHERE individual_id = 2 AND transaction_id = 1;

UPDATE individual SET balance = balance + 530 WHERE individual_id = 2;

UPDATE individual SET balance = balance - 530 WHERE individual_id = 1;

-- =================================================================================================
-- Group expense
INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES ("2023-06-04", TRUE, 5, 3, FALSE, "Expense # 2", 150.00, 50.00, "EXPENSE", 2);

INSERT INTO individual_makes_transaction VALUES (1, 3, -50);

UPDATE individual SET balance = balance - 50 WHERE individual_id = 1;

INSERT INTO individual_makes_transaction VALUES (5, 3, 0);

UPDATE individual SET balance = balance + 100 WHERE individual_id = 5;

INSERT INTO individual_makes_transaction VALUES (4, 3, -50);

UPDATE individual SET balance = balance - 50 WHERE individual_id = 4;

-- =================================================================================================
-- Group Settlement
INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES ("2023-06-05", TRUE, 5, 2, FALSE, "Payment # 2", 150.00, 40.00, "SETTLEMENT", 2);

INSERT INTO individual_makes_transaction VALUES (1, 4, 50);

UPDATE individual_makes_transaction SET transaction_amount = (SELECT transaction_amount FROM individual_makes_transaction WHERE transaction_id = 4 AND individual_id = 1) + transaction_amount WHERE individual_id = 1 AND transaction_id = 3;

UPDATE individual SET balance = balance + 50 WHERE individual_id = 1;

UPDATE individual SET balance = balance - 50 WHERE individual_id = 5;


INSERT INTO transaction_history (date_issued, is_group, payee_id, number_of_users_involved, is_settled, transaction_description, total_amount, contribution, type_of_transaction, group_id) VALUES ("2023-06-12", FALSE, 3, 5, FALSE, "Expense # 3", 5000.00, 2500.00, "EXPENSE", NULL);
INSERT INTO individual_makes_transaction VALUES (3, 5, 0);
UPDATE individual SET balance = balance + 2500 WHERE individual_id = 3;
INSERT INTO individual_makes_transaction VALUES (1, 5, -2500.00);
UPDATE individual SET balance = balance - 2500 WHERE individual_id = 1;