create database auctionms;
use auctionms;

drop table if exists bid;
drop table if exists biditem;
drop table if exists user;
drop table if exists item;
drop table if exists category;

CREATE TABLE `category` (
`id` bigint NOT NULL AUTO_INCREMENT,                                                                                    
`name` varchar(50) NOT NULL,                                                                                            
`description` longtext,                                                                                                 
PRIMARY KEY (`id`)                                                                                                    
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

 CREATE TABLE `item` (
 `id` bigint NOT NULL AUTO_INCREMENT,                                                                                    
 `name` varchar(50) NOT NULL,                                                                                            
 `description` longtext,                                                                                                
 `category_id` bigint NOT NULL,                                                                                         
 PRIMARY KEY (`id`),                                                                                                     
 KEY `item_category_id_03b07192_fk_category_id` (`category_id`),                                                         
 CONSTRAINT `item_category_id_03b07192_fk_category_id` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)        
 ) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `biditem` (                                                                                      
`id` bigint NOT NULL AUTO_INCREMENT,                                                                                    
`base_price` int unsigned NOT NULL,                                                                                     
`is_sold` tinyint(1) NOT NULL,                                                                                         
 `item_id` bigint NOT NULL,                                                                                              
 PRIMARY KEY (`id`),                                                                                                     
 UNIQUE KEY `item_id` (`item_id`),                                                                                       
 CONSTRAINT `biditem_item_id_28e1c28e_fk_item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),                      
 CONSTRAINT `biditem_chk_1` CHECK ((`base_price` >= 0))                                                                
 ) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `user` (                                                                                           
`id` bigint NOT NULL AUTO_INCREMENT,                                                                                   
 `phone_number` bigint unsigned DEFAULT NULL,                                                                           
 `age` smallint unsigned NOT NULL,                                                                                       
 `first_name` varchar(40) NOT NULL,                                                                                     
 `last_name` varchar(40) NOT NULL,                                                                                       
 `password` varchar(500) DEFAULT NULL,                                                                                   
 `name` varchar(81) GENERATED ALWAYS AS (concat(`first_name`,_utf8mb4' ',`last_name`)) STORED,                           
 `email` varchar(45) DEFAULT NULL,                                                                                      
 PRIMARY KEY (`id`),                                                                                                    
 UNIQUE KEY `email_UNIQUE` (`email`),                                                                                    
 CONSTRAINT `user_chk_1` CHECK ((`phone_number` >= 0)),                                                                  
 CONSTRAINT `user_chk_2` CHECK ((`age` >= 0))                                                                          
 ) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

 CREATE TABLE `bid` (                                                                                            
 `id` bigint NOT NULL AUTO_INCREMENT,                                                                                    
 `amount` int unsigned NOT NULL,                                                                                         
 `bid_item_id` bigint NOT NULL,                                                                                          
 `user_id` bigint NOT NULL,                                                                                              
 `time_of_bid` datetime DEFAULT CURRENT_TIMESTAMP,                                                                       
 `status` enum('pending','approved','rejected') DEFAULT 'pending',                                                       
 PRIMARY KEY (`id`),                                                                                                     
 KEY `bid_bid_item_id_b7e210ee_fk_biditem_id` (`bid_item_id`),                                                           
 KEY `bid_user_id_f3c1a638_fk_user_id` (`user_id`),                                                                      
 CONSTRAINT `bid_bid_item_id_b7e210ee_fk_biditem_id` FOREIGN KEY (`bid_item_id`) REFERENCES `biditem` (`id`),            
 CONSTRAINT `bid_user_id_f3c1a638_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),                          
 CONSTRAINT `bid_chk_1` CHECK ((`amount` >= 0))                                                                        
 ) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
 
 delimiter &&
create procedure getCurrentBid (IN bidItemID int) 
begin 
	select max(amount) as maxBidAmount from bid where bid_item_id = bidItemID; 
end &&
call getCurrentBid(2);
select * from bid;

delimiter &&
create procedure getBids (IN bidItemID int) 
begin 
	select name,amount,time_of_bid from bid,user where bid.user_id = user.id and bid.bid_item_id = bidItemID order by amount desc;
end &&stopBid
show tables;
call getBids(1);
alter table bid modify amount int check(min > (call getCurrentBid(bid.bid_item_id));
delimiter $$

delimiter &&
create procedure startBid (IN bidId int,IN itemID int,IN base_price int) 
begin 
	IF not exists (select distinct(item_id) from bidItem where item_id = itemID)
    THEN begin
		Insert into bidItem (id,base_price,is_sold,item_id) values (1,base_price,0,itemId);
	end;
    end if;
end&&

delimiter &&
create procedure stopBid (IN biditemID int) 
begin 
	update biditem set is_sold = 1 where id = biditemID;
end&&

insert into category (id,name,description) values (1,"Weapons","Ancient weapons used by great kings");
insert into category (id,name,description) values (2,"Paintings","Ancient paintings of great kings");

insert into item(id,name,description,category_id) values(101,"Sword","Sword of great King",1);
insert into item(id,name,description,category_id) values(102,"Spear","Spear of great King",1);
insert into item(id,name,description,category_id) values(103,"Bow","Bow of great King",1);
insert into item(id,name,description,category_id) values(104,"Shield","Shield of great King",1);
insert into item(id,name,description,category_id) values(105,"Reaper","Reaper of great King",1);
insert into item(id,name,description,category_id) values(106,"Sketch","Sketxh of great King",2);
insert into item(id,name,description,category_id) values(107,"Leaf Painting","Leaf painting of great King",2);
insert into item(id,name,description,category_id) values(108,"Oil Painting","Oil Painting of great King",2);
insert into item(id,name,description,category_id) values(109,"Hash painting","Hash painting of great King",2);
insert into item(id,name,description,category_id) values(110,"Thumb painting","Thumb painting of great King",2);

-- User Registration
INSERT INTO user (id,phone_number, age, first_name, last_name, password, email) VALUES (1,8619151680, 18, 'Arya veer singh', 'chauhan', 'goku@1111', 'f20200094@pilani.bits-pilani.ac.in');
INSERT INTO user (id,phone_number, age, first_name, last_name, password, email) VALUES (2,9863291227, 20, 'Ruchika', 'Sarkar', 'goku@1111', 'f20200016@pilani.bits-pilani.ac.in');
INSERT INTO user (id,phone_number, age, first_name, last_name, password, email) VALUES (3,9828315713, 40, 'Samikhi', 'Silavat', 'goku@1111', 'f20200018@pilani.bits-pilani.ac.in');

select * from bidItem;
-- BidItem creation 
Insert into bidItem (id,base_price,is_sold,item_id) values (1,12000,0,101);

-- Bidding Starts 
START TRANSACTION;
INSERT INTO bid (id,amount, bid_item_id, user_id) VALUES (1,14000, 1,1);
select * from bid;
Update bid set status = "approved" where id = 1;
INSERT INTO bid (id, amount, bid_item_id, user_id) VALUES (2,15000, 1,2);
Update bid set status = "approved" where id = 2;
INSERT INTO bid (id, amount, bid_item_id, user_id) VALUES (3,17000, 1,3);
Update bid set status = "rejected" where id = 3;
INSERT INTO bid (id,amount, bid_item_id, user_id) VALUES (4,20000, 1,1);
Update bid set status = "approved" where id = 4;
call stopBid(1);
COMMIT;

-- drop table if exists bid;
-- drop table if exists biditem;
-- drop table if exists user;
-- drop table if exists item;
-- drop table if exists category;
-- drop database auctionms;

