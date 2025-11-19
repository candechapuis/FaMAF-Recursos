USE `world`;

SELECT `cou`.`Name` as `Country`, `cou`.`Continent` as `Continent`, 
		`lan`.`Language` as Language
FROM `countrylanguage`as `lan`
LEFT JOIN `country` as `cou` ON `lan`.CountryCode = `cou`.Code
WHERE `lan`.IsOfficial = 'T';