create database 180Final;
use 180Final;

create table Users (
userName varchar(200) Primary key,
name varchar(200) not null,
email varchar(200),
password varchar(64),
accountType varchar(20)
);

create table Products (
PID varchar(50) primary key,
Title varchar(5) not null,
Description varchar(400),
WarrantyPeriod int,
nOfItems int,
price float,
addedByUserName varchar(50),
foreign key (addedByUserName) references Users(userName)
);

create table Discounts (
DID varchar(50) primary key,
DiscountAmount float not null,
timeTillActive dateTime
);

create table ProductHasDiscount (
PID varchar(50),
DID varchar(50),
foreign key (PID) references Products(PID),
foreign key (DID) references Discounts(DID)
);

create table ProductImages (
PID varchar(50),
imageURL varchar(200) not null,
foreign key (PID) references Products(PID)
);

create table ProductColor (
PID varchar(50),
color varchar(20) not null,
foreign key (PID) references Products(PID)
);

create table ProductSize (
PID varchar(50),
size varchar(10) not null,
foreign key (PID) references Products(PID)
);


create table Carts (
cartID varchar(50) Primary key,
addedByUserName varchar(50),
foreign key (addedByUserName) references Users(userName)
);

create table CartHasProduct (
cartID varchar(50),
PID varchar(50),
size varchar(50),
color varchar(50),
foreign key (cartID) references Carts(cartID),
foreign key (PID) references Products(PID)
);

create table Reviews (
RID varchar(50) primary key,
rating float,
descript varchar(400),
img varchar(200),
date dateTime,
reviewUserName varchar(50),
foreign key (reviewUserName) references Users(userName)
);

create table Complaints (
CID varchar(50) primary key,
date dateTime,
title varchar(100),
description varchar(400),
demand varchar(400),
status varchar(50),
reviewUserName varchar(50),
foreign key (reviewUserName) references Users(userName)
);

create table ComplaintImages (
CID varchar(50),
imageURL varchar(50),
foreign key (CID) references Complaints(CID)
);

create table Orders (
OID varchar(50) primary key,
status varchar(50),
placedByUserName varchar(50),
foreign key (placedByUserName) references Users(userName)
);

create table Messages (
messageID varchar(50) primary key,
text varchar(400),
imageURL varchar(200),
writerUserName varchar(50), 
receiverUserName varchar(50),
foreign key (writerUserName) references Users(userName),
foreign key (receiverUserName) references Users(userName)
);