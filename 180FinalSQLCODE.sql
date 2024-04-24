create database 180Final;
use 180Final;

create table Users (
userName varchar(200) Primary key unique,
name varchar(200) not null,
email varchar(200) unique,
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

insert into Users () values ("Customer1", "John Doe", "ThisMaEmail@email.com", "Cpass", "Customer");
insert into Users () values ("Customer2", "Jane Doe", "ThisMaEmail2@email.com", "Cpass2", "Customer");
insert into Users () values ("Admin1", "Jimmy Smith", 'AdminEmail@email.com', "Apass", "Admin");
insert into Users () values ("Admin2", "Jenny Smith", 'AdminEmail2@email.com', "Apass2", "Admin");
insert into Users () values ("Vendor1", "Jack Williams", "VendorEmail@email.com", "Vpass", "Vendor");
insert into Users () values ("Vendor2", "Jess Williams", "VendorEmail2@email.com", "Vpass2", "Vendor");

insert into Discounts () values ("D1", 10.99, "2025-12-25");
insert into Discounts () values ("D2", 30.99, "2025-08-20");
insert into Discounts () values ("D3", 5.50, "2026-12-25");
insert into Discounts () values ("D4", 1.01, "2026-11-24");
insert into Discounts () values ("D5", 100.50, "2029-01-01");


insert into Products () values ("P1", "T Shirt", "Blank T Shirt", 60, 1000, 15.99, "Vendor1");
insert into ProductHasDiscount () values ("P1", "D3");
insert into ProductImages () values ("P1", "https://i.pinimg.com/originals/90/fb/9d/90fb9d912e9663ca4ed575dee7dd73ac.jpg");
insert into ProductImages () values ("P1", "https://th.bing.com/th/id/R.aadb191cfe6b30d00adcac7c22d03e64?rik=ono2hOn%2bEJdl3w&riu=http%3a%2f%2fwww.clipartbest.com%2fcliparts%2f9cz%2fpyp%2f9czpypoRi.jpg&ehk=JFqRvCMJWIki3ByyBQGStXLeFwFLR6XVgXEaorm7ldM%3d&risl=&pid=ImgRaw&r=0");
insert into ProductImages () values ("P1", "https://th.bing.com/th/id/OIP.AhQLquhuHk34cIM4K5lJGAHaHa?rs=1&pid=ImgDetMain");
insert into ProductColor () values ("P1", "White");
insert into ProductColor () values ("P1", "Light Green");
insert into ProductColor () values ("P1", "Blue");
insert into ProductSize () values ("P1", "S");
insert into ProductSize () values ("P1", "M");
insert into ProductSize () values ("P1", "L");

insert into Products () values ("P2", "Ring", "Ring with or without gemstone", 90, 15, 549.99, "Vendor2");
insert into ProductImages () values ("P2", "https://ae01.alicdn.com/kf/HTB1JJnfHVXXXXa8XXXXq6xXFXXXZ/2016-Fashion-Jewelry-women-s-Simple-Purple-Stone-Plated-Engagement-Rings-Wedding-Jewelry-R003.jpg");
insert into ProductImages () values ("P2", "https://th.bing.com/th/id/OIP.knQKIsLLNhXwRIQtyL2SNgHaHa?rs=1&pid=ImgDetMain");
insert into ProductImages () values ("P2", "https://cdn10.bigcommerce.com/s-7plbcvh/products/3008/images/13210/Pink_Tourmaline_Engagement_Ring_14K_Rose_Gold_3.25_Carat_Pave_Halo_Handmade_Certified_1__84308.1463595121.1280.1280.jpg?c=2");
insert into ProductColor () values ("P2", "Amethyst");
insert into ProductColor () values ("P2", "Emerald");
insert into ProductColor () values ("P2", "Pink Diamond");
insert into ProductSize () values ("P2", "S");
insert into ProductSize () values ("P2", "M");
insert into ProductSize () values ("P2", "L");

insert into Products () values ("P3", "Silly Putty", "Tin of silly putty", 30, 400, 9.99, "Vendor1");
insert into ProductHasDiscount () values ("P3", "D4");
insert into ProductImages () values ("P3", "https://m.media-amazon.com/images/I/71NrauOEq8L.__AC_SX300_SY300_QL70_FMwebp_.jpg");
insert into ProductImages () values ("P3", "https://m.media-amazon.com/images/I/81df1+j0L8L._AC_SY879_.jpg");
insert into ProductImages () values ("P3", "https://m.media-amazon.com/images/I/81I+4KFvVaL._AC_SX679_.jpg");
insert into ProductColor () values ("P3", "Liquid Glass");
insert into ProductColor () values ("P3", "Super Illusions Super Scarab");
insert into ProductColor () values ("P3", "Cosmic Star Dust");
insert into ProductSize () values ("P3", "S");

insert into Products () values ("P4", "Sweatpants", "Men's Casual Fleece Jogger Sweatpants Cotton Active Running Hiking Elastic Pocket Pants", 60, 300, 49.99, "Vendor");
insert into ProductHasDiscount () values ("P4", "D2");
insert into ProductImages () values ("P4", "https://m.media-amazon.com/images/I/81H4qBgcRlL._AC_SY550_.jpg");
insert into ProductImages () values ("P4", "https://m.media-amazon.com/images/I/81HuEpiQwZL._AC_SY550_.jpg");
insert into ProductImages () values ("P4", "https://m.media-amazon.com/images/I/818muyLArmL._AC_SY550_.jpg");
insert into ProductColor () values ("P4", "Grey");
insert into ProductColor () values ("P4", "Yellow");
insert into ProductColor () values ("P4", "Blue");
insert into ProductSize () values ("P4", "S");
insert into ProductSize () values ("P4", "M");
insert into ProductSize () values ("P4", "L");

insert into Products () values ("P5", "Flavored Water 12pk", "A pack of 12 bottle of flavored water", 5, 100, 8.99, "Vendor");
insert into ProductImages () values ("P5", "https://m.media-amazon.com/images/I/81ca3M+VQAL._SX679_PIbundle-12,TopRight,0,0_AA679SH20_.jpg");
insert into ProductImages () values ("P5", "https://m.media-amazon.com/images/I/81WHVSp9DbL._SX679_.jpg");
insert into ProductImages () values ("P5", "https://m.media-amazon.com/images/I/81OqsPWi-SL._SX679_.jpg");
insert into ProductColor () values ("P5", "Kiwi Strawberry");
insert into ProductColor () values ("P5", "Grape");
insert into ProductColor () values ("P5", "Watermelon");
insert into ProductSize () values ("P5", "12pk");