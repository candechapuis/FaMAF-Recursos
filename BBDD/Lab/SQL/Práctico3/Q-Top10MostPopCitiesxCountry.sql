USE `world`;

SELECT co.`Name` as  `Country`, ci.`Name` as `City`, co.`Region`, co.`GovernmentForm`
FROM `city` AS `ci`
LEFT JOIN `country` as `co` ON `ci`.`CountryCode` = `co`.`Code`
ORDER BY `ci`.`Population` DESC
LIMIT 10;
