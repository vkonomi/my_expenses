DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts (
    acc_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    acc_name CHAR(15) not null,
    acc_type CHAR(15) not null,
    acc_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL 
);