USE `world`;

WITH 
max_percentage_of_official_languages (CountryCode, OffPercentage) AS (
	SELECT CountryCode, MAX(Percentage)
	FROM countrylanguage
	WHERE IsOfficial = 'T'
	GROUP BY CountryCode)


SELECT country.Name, countrylanguage.Language
FROM country JOIN countrylanguage ON country.Code = countrylanguage.CountryCode
AND countrylanguage.IsOfficial = 'F'
WHERE countrylanguage.Percentage > ALL (
	SELECT OffPercentage
	FROM max_percentage_of_official_languages
	WHERE countrylanguage.CountryCode = max_percentage_of_official_languages.CountryCode
	)

