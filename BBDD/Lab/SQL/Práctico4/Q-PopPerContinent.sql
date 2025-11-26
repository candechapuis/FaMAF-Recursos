USE `world`;

SELECT c.Name, TotalPopulation
FROM Continent AS c JOIN 
	(SELECT country.Continent, SUM(country.Population) AS TotalPopulation
	FROM country
	GROUP BY country.Continent) AS PopPerContinent 
ON PopPerContinent.Continent = c.Name
ORDER BY TotalPopulation DESC;
	