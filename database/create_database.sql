create database if not exists portfolio_mgmt;
use portfolio_mgmt;

create table if not exists transactions (
    ID int not null primary key AUTO_INCREMENT,
    Ticker varchar(45) not null,
    Amount int not null,
    TransactionTimestamp datetime not null,
    PriceAtTransaction decimal(10,2) not null
);

create table if not exists balance (
    UUID int not null primary key,
    LastUpdatedAt datetime not null,
    Balance decimal(10,2) not null
);

insert into balance (UUID, LastUpdatedAt, Balance) values (1, NOW(), 0.0);
insert into balance (UUID, LastUpdatedAt, Balance) values (1, NOW(), 10000.0);

insert into transactions (ID, UUID, Ticker, Amount, TransactionTimestamp, PriceAtTransaction)
values (3, 1, "AAPL", 1000,  NOW(), 204.18);

insert into transactions (ID, UUID, Ticker, Amount, TransactionTimestamp, PriceAtTransaction)
values (4, 1, "AAPL", -5000,  NOW(), 204.18);