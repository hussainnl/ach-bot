/*****************************************************************************
 RDBMS:          MySQL
 Create Date:    01/23/2026
 Author:         Hussain Fathy
 Description:    Create all the tables for telegram bot that is manangr a self growth 
                 group 
 *************************************************************************************/

-- drop database ach_bot_db if it exists
DROP DATABASE IF EXISTS ach_bot_db;

-- create database ach_bot_db
-- character set utf8
CREATE DATABASE IF NOT EXISTS ach_bot_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ach_bot_db;

-- Table group_info
DROP TABLE IF EXISTS group_info;
CREATE TABLE group_info (
  group_id BIGINT NOT NULL,
  group_name VARCHAR(128) NOT NULL,
  study_topic_id SMALLINT
  DEFAULT NULL,
  weekly_topic_id SMALLINT
  DEFAULT NULL,
  notification_topic_id SMALLINT
  DEFAULT NULL,
  rules_topic_id SMALLINT
  DEFAULT NULL,
  PRIMARY KEY (group_id),
  UNIQUE  unq_group_name (group_name) 
);

-- Table user_info
DROP TABLE IF EXISTS user_info;
CREATE TABLE IF NOT EXISTS user_info (
  user_id BIGINT NOT NULL ,
  group_id BIGINT NOT NULL,
  user_name VARCHAR(128) NOT NULL,
  score INT
  DEFAULT 0,
  missed TINYINT(5)
  DEFAULT 0 ,
  is_subscribed  TINYINT(1)
  DEFAULT 0,
  mode TINYINT(1)
  DEFAULT 0,
  PRIMARY KEY (user_id),
  UNIQUE INDEX  unq_username (user_name) ,
  INDEX  idx_sorce (score),
  INDEX  idx_missed (missed),
  CONSTRAINT fk_group_id
    FOREIGN KEY (group_id)
    REFERENCES group_info (group_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);



-- Table message
DROP TABLE IF EXISTS message;
CREATE TABLE IF NOT EXISTS message (
  msg_id TINYINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  msg_name VARCHAR(32),
  content VARCHAR(320)
  );
-- Table achievement
DROP TABLE IF EXISTS achievement;
CREATE TABLE IF NOT EXISTS achievement (
  ach_id TINYINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  ach_name VARCHAR(32),
  ach_point TINYINT
  );
