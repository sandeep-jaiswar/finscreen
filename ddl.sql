CREATE TABLE Sector (
    id SERIAL PRIMARY KEY,
    sector_name VARCHAR(255)
);

CREATE TABLE Industry (
    id SERIAL PRIMARY KEY,
    industry_name VARCHAR(255)
);

CREATE TABLE Exchange (
    id SERIAL PRIMARY KEY,
    exchange_name VARCHAR(255)
);

CREATE TABLE Currency (
    id SERIAL PRIMARY KEY,
    currency_code VARCHAR(10),
    currency_name VARCHAR(100)
);

CREATE TABLE Company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    symbol VARCHAR(50),
    short_name VARCHAR(255),
    long_name VARCHAR(255),
    sector_id INT,
    industry_id INT,
    founded INT CHECK (founded >= 0 AND founded <= EXTRACT(YEAR FROM CURRENT_DATE)),
    total_employees INT,
    exchange_id INT,
    currency_id INT,
    CONSTRAINT fk_sector FOREIGN KEY (sector_id) REFERENCES Sector(id),
    CONSTRAINT fk_industry FOREIGN KEY (industry_id) REFERENCES Industry(id),
    CONSTRAINT fk_exchange FOREIGN KEY (exchange_id) REFERENCES Exchange(id),
    CONSTRAINT fk_currency FOREIGN KEY (currency_id) REFERENCES Currency(id)
);

CREATE TABLE Address (
    id SERIAL PRIMARY KEY,
    company_id INT,
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    city VARCHAR(100),
    zip VARCHAR(20),
    country VARCHAR(100),
    phone VARCHAR(50),
    fax VARCHAR(50),
    website VARCHAR(255),
    CONSTRAINT fk_company_address FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE Officer (
    id SERIAL PRIMARY KEY,
    company_id INT,
    name VARCHAR(255),
    title VARCHAR(255),
    age INT,
    fiscal_year INT CHECK (fiscal_year >= 1900 AND fiscal_year <= EXTRACT(YEAR FROM CURRENT_DATE)),
    year_born INT CHECK (year_born >= 1900 AND year_born <= EXTRACT(YEAR FROM CURRENT_DATE)),
    CONSTRAINT fk_company_officer FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE Officer_Compensation (
    id SERIAL PRIMARY KEY,
    officer_id INT,
    total_pay DECIMAL(15, 2),
    exercised_value DECIMAL(15, 2),
    unexercised_value DECIMAL(15, 2),
    CONSTRAINT fk_officer_compensation FOREIGN KEY (officer_id) REFERENCES Officer(id)
);

CREATE TABLE Company_Financials (
    id SERIAL PRIMARY KEY,
    company_id INT,
    year INT CHECK (year >= 1900 AND year <= EXTRACT(YEAR FROM CURRENT_DATE)),
    currency_id INT,
    market_cap DECIMAL(15, 2),
    enterprise_value DECIMAL(15, 2),
    total_cash DECIMAL(15, 2),
    total_debt DECIMAL(15, 2),
    total_revenue DECIMAL(15, 2),
    revenue_per_share DECIMAL(15, 2),
    gross_margin DECIMAL(5, 2),
    ebitda_margin DECIMAL(5, 2),
    operating_margin DECIMAL(5, 2),
    profit_margin DECIMAL(5, 2),
    book_value DECIMAL(15, 2),
    debt_to_equity_ratio DECIMAL(5, 2),
    current_ratio DECIMAL(5, 2),
    quick_ratio DECIMAL(5, 2),
    free_cashflow DECIMAL(15, 2),
    operating_cashflow DECIMAL(15, 2),
    CONSTRAINT fk_company_financials FOREIGN KEY (company_id) REFERENCES Company(id),
    CONSTRAINT fk_currency_financials FOREIGN KEY (currency_id) REFERENCES Currency(id)
);


CREATE TABLE Dividend (
    id SERIAL PRIMARY KEY,
    company_id INT ,
    year INT  CHECK (year >= 1900 AND year <= EXTRACT(YEAR FROM CURRENT_DATE)),
    dividend_rate DECIMAL(5, 2),
    dividend_yield DECIMAL(5, 2),
    payout_ratio DECIMAL(5, 2),
    ex_dividend_date DATE,
    five_year_avg_dividend_yield DECIMAL(5, 2),
    trailing_annual_dividend_rate DECIMAL(5, 2),
    trailing_annual_dividend_yield DECIMAL(5, 2),
    CONSTRAINT fk_company_dividend FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE Stock_Price (
    id SERIAL PRIMARY KEY,
    company_id INT ,
    date DATE ,
    previous_close DECIMAL(15, 2),
    open DECIMAL(15, 2),
    day_low DECIMAL(15, 2),
    day_high DECIMAL(15, 2),
    current_price DECIMAL(15, 2),
    fifty_two_week_low DECIMAL(15, 2),
    fifty_two_week_high DECIMAL(15, 2),
    fifty_day_avg DECIMAL(15, 2),
    two_hundred_day_avg DECIMAL(15, 2),
    volume BIGINT,
    average_volume BIGINT,
    CONSTRAINT fk_company_stock_price FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE Risk_Metrics (
    id SERIAL PRIMARY KEY,
    company_id INT ,
    audit_risk DECIMAL(5, 2),
    board_risk DECIMAL(5, 2),
    compensation_risk DECIMAL(5, 2),
    shareholder_rights_risk DECIMAL(5, 2),
    overall_risk DECIMAL(5, 2),
    CONSTRAINT fk_company_risk FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE Performance_Metrics (
    id SERIAL PRIMARY KEY,
    company_id INT ,
    date DATE ,
    week_52_change DECIMAL(5, 2),
    sandp_52_week_change DECIMAL(5, 2),
    beta DECIMAL(5, 2),
    trailing_pe_ratio DECIMAL(5, 2),
    forward_pe_ratio DECIMAL(5, 2),
    peg_ratio DECIMAL(5, 2),
    CONSTRAINT fk_company_performance FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE Analyst_Opinion (
    id SERIAL PRIMARY KEY,
    company_id INT ,
    date DATE ,
    target_high_price DECIMAL(15, 2),
    target_low_price DECIMAL(15, 2),
    target_mean_price DECIMAL(15, 2),
    target_median_price DECIMAL(15, 2),
    recommendation_mean DECIMAL(5, 2),
    recommendation_key VARCHAR(100),
    number_of_analyst_opinions INT,
    CONSTRAINT fk_company_analyst_opinion FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE holder (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    holder_name VARCHAR(255) NOT NULL,
    percentage_owned NUMERIC(5, 2),
    shares BIGINT,
    date_reported DATE,
    change_in_shares BIGINT
);

CREATE TABLE company_action (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL,
    action_date DATE NOT NULL,
    details TEXT
);

CREATE TABLE company_event (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    event_date DATE NOT NULL,
    description TEXT
);

CREATE TABLE insider_transaction (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    insider_name VARCHAR(255) NOT NULL,
    relation VARCHAR(50),
    last_date DATE,
    transaction_type VARCHAR(50),
    ownership_type VARCHAR(50),
    shares_traded BIGINT,
    last_price NUMERIC(15, 2),
    shares_held BIGINT
);

CREATE TABLE stock_split (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    split_date DATE NOT NULL,
    ratio VARCHAR(10) NOT NULL,
    description TEXT
);

CREATE TABLE earnings (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    period VARCHAR(50),
    revenue NUMERIC(15, 2),
    earnings NUMERIC(15, 2),
    eps NUMERIC(15, 2),
    estimate NUMERIC(15, 2),
    surprise NUMERIC(5, 2) -- percentage or actual value
);

CREATE TABLE balance_sheet (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    cash_and_cash_equivalents NUMERIC(15, 2),
    short_term_investments NUMERIC(15, 2),
    net_receivables NUMERIC(15, 2),
    inventory NUMERIC(15, 2),
    total_current_assets NUMERIC(15, 2),
    long_term_investments NUMERIC(15, 2),
    property_plant_equipment NUMERIC(15, 2),
    intangible_assets NUMERIC(15, 2),
    total_assets NUMERIC(15, 2),
    total_liabilities NUMERIC(15, 2),
    total_equity NUMERIC(15, 2)
);

CREATE TABLE income_statement (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    revenue NUMERIC(15, 2),
    cost_of_revenue NUMERIC(15, 2),
    gross_profit NUMERIC(15, 2),
    operating_expense NUMERIC(15, 2),
    operating_income NUMERIC(15, 2),
    net_income NUMERIC(15, 2)
);

CREATE TABLE cash_flow_statement (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    net_cash_from_operating_activities NUMERIC(15, 2),
    net_cash_used_for_investing_activities NUMERIC(15, 2),
    net_cash_from_financing_activities NUMERIC(15, 2),
    free_cash_flow NUMERIC(15, 2),
    dividends_paid NUMERIC(15, 2)
);

CREATE TABLE recommendation (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    recommendation VARCHAR(50), -- e.g., "Buy", "Sell", "Hold"
    source VARCHAR(255), -- e.g., "Analyst", "Agency"
    rating NUMERIC(5, 2)
);

CREATE TABLE historical_data (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    open NUMERIC(15, 2),
    high NUMERIC(15, 2),
    low NUMERIC(15, 2),
    close NUMERIC(15, 2),
    volume BIGINT
);

CREATE TABLE esg_score (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES company(id) ON DELETE CASCADE,
    environmental_score NUMERIC(5, 2),
    social_score NUMERIC(5, 2),
    governance_score NUMERIC(5, 2),
    total_esg_score NUMERIC(5, 2),
    esg_rating VARCHAR(50), -- e.g., "AA", "BBB"
    rating_agency VARCHAR(255), -- e.g., "MSCI", "S&P"
    last_updated DATE
);

