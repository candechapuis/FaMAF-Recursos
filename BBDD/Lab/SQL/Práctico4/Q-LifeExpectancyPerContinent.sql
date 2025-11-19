USE `world`;

SELECT c.Name, `AvgLifeExpectancy`
FROM Continent AS c JOIN 
	(SELECT country.Continent, AVG(country.LifeExpectancy) AS `AvgLifeExpectancy`
	FROM country
	GROUP BY country.Continent) AS AvgLifeExpPerContinent 
ON AvgLifeExpPerContinent.Continent = c.Name
WHERE AvgLifeExpPerContinent.AvgLifeExpectancy BETWEEN 40 AND 70;