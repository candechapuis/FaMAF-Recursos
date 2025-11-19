USE `world`;

( SELECT `Name` AS 'Top 10 Most/Less Populated Countries'
FROM `country`
ORDER BY `Population` DESC
LIMIT 10)
UNION
( SELECT `Name`
FROM `country`
WHERE `Population` >= 100
ORDER BY `Population` 
LIMIT 10);
