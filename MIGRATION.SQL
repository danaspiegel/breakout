SET FOREIGN_KEY_CHECKS =0;

RENAME TABLE `breakout_breakoutcategory` TO `breakout_breakoutsessionformat`;

ALTER TABLE `account_userprofile` ADD `age` smallint(5) unsigned default NULL;
ALTER TABLE `account_userprofile` ADD `gender` varchar(1) default NULL;
ALTER TABLE `account_userprofile` ADD `occupation` varchar(100) default NULL;

ALTER TABLE `breakout_breakoutsession` DROP FOREIGN KEY `category_id_refs_id_1be6b960`;
ALTER TABLE `breakout_breakoutsession` DROP KEY `breakout_breakoutsession_category_id`;
ALTER TABLE `breakout_breakoutsession` CHANGE COLUMN `category_id` `session_format_id` INT(11) NOT NULL DEFAULT 0;
ALTER TABLE `breakout_breakoutsession` ADD KEY `breakout_breakoutsession_session_format_id` (`session_format_id`);
ALTER TABLE `breakout_breakoutsession` ADD CONSTRAINT `session_format_id_refs_id_1be6b960` FOREIGN KEY (`session_format_id`) REFERENCES `breakout_breakoutsessionformat` (`id`);



-- ALTER TABLE `breakout_breakoutsession` ADD `rain_venue_id` int(11) default NULL;
-- ALTER TABLE `breakout_breakoutsession` ADD KEY `breakout_venue_rain_venue_id` (`rain_venue_id`);
-- ALTER TABLE `breakout_breakoutsession` ADD CONSTRAINT `rain_venue_id_refs_id_22c01e7b` FOREIGN KEY (`rain_venue_id`) REFERENCES `breakout_venue` (`id`);

SET FOREIGN_KEY_CHECKS = 1;


-- for timezone support
ALTER TABLE `breakout_breakoutsession` ADD COLUMN `timezone` VARCHAR(100) NOT NULL DEFAULT 'US/Eastern';


-- twitterpocalyse
ALTER TABLE `breakout`.`lifestream_twitterstatus` CHANGE COLUMN `twitter_id` `twitter_id` BIGINT(10) UNSIGNED NOT NULL DEFAULT 0  COMMENT ''  AFTER `lifestreamentry_ptr_id`;

ALTER TABLE `breakout`.`lifestream_twitteruser` CHANGE COLUMN `twitter_id` `twitter_id` BIGINT(10) UNSIGNED NULL DEFAULT 0  COMMENT ''  AFTER `updated_on`;

ALTER TABLE `breakout`.`lifestream_twitteruser` CHANGE COLUMN `screen_name` `screen_name` VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT ''  COMMENT ''  AFTER `twitter_id`;

ALTER TABLE `breakout`.`lifestream_twitteruser` CHANGE COLUMN `url` `url` VARCHAR(400) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL  COMMENT ''  AFTER `screen_name`;

ALTER TABLE `breakout`.`lifestream_twitteruser` CHANGE COLUMN `profile_image_url` `profile_image_url` VARCHAR(400) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL  COMMENT ''  AFTER `url`;

ALTER TABLE `breakout`.`lifestream_twitteruser` CHANGE COLUMN `location` `location` VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL  COMMENT ''  AFTER `profile_image_url`;

ALTER TABLE `breakout`.`lifestream_twitteruser` CHANGE COLUMN `description` `description` LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL  COMMENT ''  AFTER `location`;


