USE `world`;

SELECT `co`.`Name` as `Country`, `ci`.`Name` as `Capital`
FROM `country` as `co`
LEFT JOIN `city`as `ci` ON `co`.Capital = `ci`.ID
ORDER BY `co`.`SurfaceArea` DESC
LIMIT 20;
