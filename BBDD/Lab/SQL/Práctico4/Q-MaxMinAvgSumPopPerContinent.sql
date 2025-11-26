USE `world`;

SELECT country.Continent, MAX(country.Population) AS MaxPop,
MIN(country.Population) AS MinPop, AVG(country.Population) AS AvgPop,
SUM(country.Population) AS TotalPop
FROM country 
GROUP BY country.Continent;
