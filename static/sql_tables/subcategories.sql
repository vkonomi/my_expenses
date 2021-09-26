DROP TABLE IF EXISTS subproducts;

CREATE TABLE subcategories (
    subctg_id       INTEGER PRIMARY KEY AUTOINCREMENT not null,
    assoc_ctg   INTEGER not null,
    subctg_desc     char(25) not null,
    subctg_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY(assoc_ctg) REFERENCES categories(ctg_id) 
);

