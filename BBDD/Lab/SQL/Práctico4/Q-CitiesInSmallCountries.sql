USE `world`;

SELECT `ci`.`Name` AS `City`, `co`.`Name` AS `Country`
FROM `city` as `ci`
LEFT JOIN `country` AS `co` ON `ci`.`CountryCode` = `co`.`Code`
WHERE `co`.`Population` < 1000;
