USE `world`;

SELECT `Name`, `Population`
FROM `city`
WHERE `Population` > (
		SELECT AVG( `Population`)
		FROM `city`)
ORDER BY `Population`;
