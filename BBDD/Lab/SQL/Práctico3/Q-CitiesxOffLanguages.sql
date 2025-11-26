USE `world`;

SELECT `c`.`Name`, `l`.`Language`,`l`.`Percentage`
FROM `city` AS `c`
LEFT JOIN `countrylanguage` AS `l` ON `c`.`CountryCode` = `l`.`CountryCode`
WHERE `l`.`IsOfficial` = 'T'
ORDER BY `c`.`Population`;