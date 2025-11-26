USE `world`;


SELECT c.Name, cl.Language
FROM country AS c JOIN countrylanguage AS cl
ON c.Code = cl.CountryCode AND cl.IsOfficial = 'F'
WHERE cl.Percentage > (
	SELECT AVG(cl.Percentage)
	FROM countrylanguage AS cl
	WHERE c.Code = cl.CountryCode
	AND cl.IsOfficial = 'T');