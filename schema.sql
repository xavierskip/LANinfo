create table '{table}'(
    ip      TEXT PRIMARY KEY,
    mac     TEXT UNIQUE,
    name    TEXT,
    comment TEXT,
    time    DATE,
    lastdate DATE
);
