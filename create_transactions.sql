CREATE TABLE Transactions (
    ID int not null primary key,
    Ticker varchar(45) not null,
    Amount int not null,
    TransactionTimestamp datetime not null,
    PriceAtTransaction decimal not null
);