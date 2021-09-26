DROP TABLE IF EXISTS tr_details;

CREATE TABLE tr_details (
    tr_id INTEGER NOT NULL,
    main_ctg char(02) not null,
    sub_ctg  char (02) not null,
    item_code integer not null,
    item_value float(7,2) DEFAULT 0 NOT NULL,
    tr_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    FOREIGN KEY(tr_id) REFERENCES transactions(trans_id) 
);