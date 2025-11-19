USE `world`;

SELECT DISTINCT `Name`, `Code`
FROM `country` AS `c`
LEFT JOIN `countrylanguage` AS `l` ON `l`.`CountryCode`= `c`.`Code`
WHERE (`l`.`Language` = 'French' OR `l`.`Language` = 'English') 
		AND `l`.IsOfficial = 'T';