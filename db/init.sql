-- Common passwords from SecLists 100k-most-used-passwords-NCSC.txt
CREATE TABLE common_passwords (password VARCHAR(255) PRIMARY KEY);
LOAD DATA INFILE '/var/lib/mysql-files/passwords.txt'
    IGNORE INTO TABLE common_passwords
    FIELDS ESCAPED BY '' LINES TERMINATED BY '\n' (@p)
    SET password = TRIM(TRAILING '\r' FROM @p);

-- Created users: username and creation time only (no password stored)
CREATE TABLE `2403201` (
    username VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
