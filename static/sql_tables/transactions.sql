DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    trans_id INTEGER PRIMARY KEY NOT NULL,
    trans_type CHAR(1) not null,
    trans_descr VARCHAR(100),
    trans_total_value float(8,2) not null default 0,
    trans_account integer not null,
    trans_exec_date DATE NOT NULL,
    trans_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL 
);