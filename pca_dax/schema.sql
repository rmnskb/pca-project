DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS stocks;

CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(15) UNIQUE NOT NULL,
    name VARCHAR,
    exchange VARCHAR,
    industry VARCHAR,
    sector VARCHAR,
    market_cap INTEGER,
--     dividend_rate DECIMAL(2, 6),
--     dividend_yield DECIMAL(2, 6),
    book_value DECIMAL(18, 6),
--     price_to_book DECIMAL(2, 6),
    beta DECIMAL
);

CREATE TABLE stocks (
    stock_value_id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(15) NOT NULL,
--     company_id INTEGER NOT NULL,
    date DATETIME NOT NULL,
    open DECIMAL(18, 4),
    high DECIMAL(18, 4),
    low DECIMAL(18, 4),
    close DECIMAL(18, 4),
    adj_close DECIMAL(18, 4),
    volume INTEGER,
    UNIQUE(symbol, date)
--     FOREIGN KEY (company_id) REFERENCES companies (id)
);
