DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS stocks;

CREATE TABLE companies (
    symbol VARCHAR(15) PRIMARY KEY,
    name VARCHAR,
    exchange VARCHAR,
    industry VARCHAR,
    sector VARCHAR,
    market_cap INTEGER,
    book_value DECIMAL(18, 6),
    beta DECIMAL
);

CREATE TABLE stocks (
    date DATETIME NOT NULL,
    symbol VARCHAR(15),
    open DECIMAL(18, 4),
    high DECIMAL(18, 4),
    low DECIMAL(18, 4),
    close DECIMAL(18, 4),
    adj_close DECIMAL(18, 4),
    volume INTEGER DEFAULT 0,
    -- set up a composite PK consisting of symbol and date combination
    CONSTRAINT con_symbol_date PRIMARY KEY(symbol, date),
    FOREIGN KEY (symbol) REFERENCES companies(symbol)
);
