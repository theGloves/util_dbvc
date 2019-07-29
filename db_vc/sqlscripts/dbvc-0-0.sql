
CREATE TABLE IF NOT EXISTS `db_version`(
    `version` varchar(64) NOT NULL ,
    PRIMARY KEY (`version`) USING BTREE
);
INSERT INTO db_version (version) values ("85ca7af0-ae78-11e9-afd6-525400f7cc8d");
