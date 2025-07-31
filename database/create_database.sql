create database if not exists portfolio_mgmt;
use portfolio_mgmt;
create table if not exists transactions (
    ID int not null primary key AUTO_INCREMENT,
    Ticker varchar(45) not null,
    Amount int not null,
    TransactionTimestamp datetime not null,
    PriceAtTransaction decimal(10,2) not null
);