DROP TABLE IF EXISTS tr_pending;

CREATE TABLE tr_pending (
    item_key        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userid          char(10) NOT NULL,
    main_ctg        char(02) not null,
    sub_ctg         char (02) not null,
    item_code       integer not null,
    item_value      float(7,2) DEFAULT 0 NOT NULL,
    tr_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL

    --FOREIGN KEY(userid) REFERENCES userids(userid) 
);