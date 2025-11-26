USE `world`;

SELECT DISTINCT country.Region
FROM country
WHERE country.SurfaceArea < 1000 AND EXISTS (
	SELECT city.Population
	FROM city
	WHERE country.Code = city.CountryCode 
	AND city.Population < 100000)
ORDER BY country.Region;