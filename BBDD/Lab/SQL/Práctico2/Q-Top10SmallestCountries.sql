USE `world`;

SELECT `Name`, `Region`, `SurfaceArea`, `GovernmentForm`
FROM `country`
ORDER BY `SurfaceArea` ASC
LIMIT 10;
