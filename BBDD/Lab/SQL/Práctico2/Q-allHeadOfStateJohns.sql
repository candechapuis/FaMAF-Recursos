USE `world`;

SELECT `Name`, `HeadOfState`
FROM `country`
WHERE `HeadOfState` LIKE '%John%';