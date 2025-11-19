USE `world`;

SELECT `Name`, `Population`
FROM `country`
WHERE `Population` BETWEEN 35000000 AND 45000000
ORDER BY `Population` DESC;