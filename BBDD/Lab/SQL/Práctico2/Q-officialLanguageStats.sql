USE `world`;

SELECT `CountryCode`,`Language`, `Percentage`
FROM `countrylanguage`
WHERE IsOfficial = 'T';
