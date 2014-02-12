CREATE DATABASE IF NOT EXISTS `atdb`;

USE `atdb`;

DROP TABLE IF EXISTS `fszmonitor`;
CREATE TABLE `fszmonitor` (
    `machineip` VARCHAR(15) NOT NULL PRIMARY KEY,
    `machinename` VARCHAR(64) NOT NULL,
    `machinestate` SMALLINT NOT NULL DEFAULT 0,
    `processstate` SMALLINT NOT NULL DEFAULT 0,
    `playerstate` SMALLINT NOT NULL DEFAULT 0,
    `updatetime` DATETIME NOT NULL,
    `streamname` VARCHAR(512),
    `streamtype` VARCHAR(16),
    `frequency` VARCHAR(32),
    `bandwidth` VARCHAR(16),
    `tdt` SMALLINT DEFAULT 0,
    `comment` VARCHAR(512)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `streams`;
CREATE TABLE `streams` (
    `filename` VARCHAR(255) NOT NULL,
    `filesize` BIGINT UNSIGNED NOT NULL,
    `channelnumber` SMALLINT UNSIGNED,
    `serverlocation` VARCHAR(1024),
    `streamtype` VARCHAR(16),
    `country` VARCHAR(512),
    `md5` VARCHAR(512),
    `comment` VARCHAR(512),
    PRIMARY KEY ( filename, filesize )
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `channels`;
CREATE TABLE `channels` (
    `filename` VARCHAR(255) NOT NULL,
    `filesize` BIGINT UNSIGNED NOT NULL,
    `channelnumber` SMALLINT UNSIGNED,
    `channelname` VARCHAR(1024),
    `comment` VARCHAR(512),
    FOREIGN KEY (filename, filesize ) REFERENCES streams(filename, filesize) ON UPDATE CASCADE ON DELETE RESTRICT
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `epgtoolresult` (
    `filename` VARCHAR(255) NOT NULL,
    `filesize` BIGINT UNSIGNED NOT NULL,
    `serverlocation` VARCHAR(1024),
    `toolmd5` VARCHAR(255),
    `toolret` VARCHAR(64),
    `toollog` VARCHAR(64),
    PRIMARY KEY ( filename, filesize, toolmd5 )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tempstreams` (
    `filename` VARCHAR(255) NOT NULL,
    `filesize` BIGINT UNSIGNED NOT NULL,
    `serverlocation` VARCHAR(1024),
    `toolmd5` VARCHAR(255),
    `toolret` VARCHAR(64),
    `toollog` VARCHAR(64),
    PRIMARY KEY ( filename, filesize, toolmd5 )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;