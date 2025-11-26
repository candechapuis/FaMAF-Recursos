USE `world`;

(SELECT `Name`
FROM `country` as `c`
LEFT JOIN `countrylanguage`AS `l` ON `l`.`CountryCode`= `c`.`Code`
WHERE `l`.`Language` = 'English')
EXCEPT
(SELECT `Name`
FROM `country` as `c`
LEFT JOIN `countrylanguage`AS `l` ON `l`.`CountryCode`= `c`.`Code`
WHERE `l`.`Language` = 'Spanish');
