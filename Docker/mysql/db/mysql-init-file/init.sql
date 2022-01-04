create user 'root'@'%' identified with mysql_native_password by '1234';
grant all privileges on *.* to 'root'@'%';

CREATE DATABASE IF NOT EXISTS sogong;
use sogong;

CREATE TABLE owner(
		onum INT AUTO_INCREMENT,
		id VARCHAR(100),
		pw VARCHAR(100),
		oname VARCHAR(100),
		PRIMARY KEY(onum));

CREATE TABLE region(
		rid INT AUTO_INCREMENT,
		rname VARCHAR(100),
		stage INT,
		PRIMARY KEY(rid));

CREATE TABLE businessType(
		bid INT AUTO_INCREMENT,
		bname VARCHAR(100),
		PRIMARY KEY(bid));

CREATE TABLE shop(
		sid INT AUTO_INCREMENT,
		bid INT,
		sname VARCHAR(100),
		rid INT,
		maxPeople INT,
		onum INT,
		PRIMARY KEY(sid),
		FOREIGN KEY (rid) references region(rid),
		FOREIGN KEY (bid) references businessType(bid),
		FOREIGN KEY (onum) references owner(onum) on update cascade on delete cascade);

CREATE TABLE trial(
		tid INT AUTO_INCREMENT,
		tnum INT, 
		sid INT,
		PRIMARY KEY (tid),
		FOREIGN KEY (sid) references shop(sid));

INSERT INTO region(rname, stage) VALUES ('Seoul', 3);
INSERT INTO region(rname, stage) VALUES ('Daejeon', 3);
INSERT INTO region(rname, stage) VALUES ('Daegu', 2);
INSERT INTO region(rname, stage) VALUES ('Busan', 3);
INSERT INTO region(rname, stage) VALUES ('Gwangju', 2);
INSERT INTO region(rname, stage) VALUES ('Ulsan', 2);
INSERT INTO region(rname, stage) VALUES ('Jeju', 1);

INSERT INTO businessType(bname) VALUES ('HOTEL');
INSERT INTO businessType(bname) VALUES ('ACADEMY');
INSERT INTO businessType(bname) VALUES ('RESTAURANT');
INSERT INTO businessType(bname) VALUES ('GYM');
INSERT INTO businessType(bname) VALUES ('BAR');

INSERT INTO owner(id, pw, oname) VALUES ('dong', '1234', 'ldh');
INSERT INTO owner(id, pw, oname) VALUES ('oh', '1234', 'ohg');
INSERT INTO owner(id, pw, oname) VALUES ('soo', '1234', 'cjs');

INSERT INTO shop(bid, sname, rid, maxPeople, onum) VALUES (2, 'etoos', 1, 30, 1);
INSERT INTO shop(bid, sname, rid, maxPeople, onum) VALUES (4, 'healchang', 3, 50, 2);
INSERT INTO shop(bid, sname, rid, maxPeople, onum) VALUES (5, 'Daebak', 7, 20, 2);
INSERT INTO shop(bid, sname, rid, maxPeople, onum) VALUES (3, 'Starbucks', 2, 20, 2);
INSERT INTO shop(bid, sname, rid, maxPeople, onum) VALUES (1, 'jisooTel', 4, 100, 3);
INSERT INTO shop(bid, sname, rid, maxPeople, onum) VALUES (2, 'jiCademy', 1, 30, 3);
INSERT INTO shop(bid, sname, rid, maxPeople, onum) VALUES (3, 'jisTaurant', 2, 100, 3);
INSERT INTO shop(bid, sname, rid, maxPeople, onum) VALUES (4, 'jiBAR', 5, 100, 3);

INSERT INTO trial(tnum, sid) VALUES (10, 1);
INSERT INTO trial(tnum, sid) VALUES (32, 2);
INSERT INTO trial(tnum, sid) VALUES (4, 3);
INSERT INTO trial(tnum, sid) VALUES (27, 4);
INSERT INTO trial(tnum, sid) VALUES (60, 2);
INSERT INTO trial(tnum, sid) VALUES (1, 1);
