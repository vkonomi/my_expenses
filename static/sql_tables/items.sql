DROP TABLE IF EXISTS items;

CREATE TABLE items (
    it_id               INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    IT_ASSOC_SCTG       INTEGER not null,
    it_desc             char(50) not null,
    it_pref_ind         char(01) not null default 'N',
    it_timestamp        TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY(IT_ASSOC_SCTG) REFERENCES subcategories(subctg_id)
);