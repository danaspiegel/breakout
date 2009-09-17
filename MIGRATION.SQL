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
