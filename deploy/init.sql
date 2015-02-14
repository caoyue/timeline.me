

CREATE DATABASE IF NOT EXISTS `timeline`;
USE `timeline`;


CREATE TABLE IF NOT EXISTS `configs` (
    `name` varchar(50) NOT NULL,
    `value` text,
    `create_time` datetime NOT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `posts` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `source` varchar(50) NOT NULL,
    `category` varchar(50) NOT NULL,
    `origin_id` varchar(100) DEFAULT NULL,
    `url` varchar(100) NOT NULL,
    `title` varchar(500) NOT NULL ,
    `content` text NOT NULL,
    `create_time` datetime NOT NULL,
    `origin_data` text,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;