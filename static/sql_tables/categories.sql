DROP TABLE IF EXISTS products;

CREATE TABLE categories (
    ctg_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    ctg_desc     char(25) not null,
    ctg_type     char(1)  not null,
    ctg_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL 
);