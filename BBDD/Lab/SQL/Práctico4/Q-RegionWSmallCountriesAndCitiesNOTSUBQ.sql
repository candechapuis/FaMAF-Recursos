USE `world`;

SELECT DISTINCT country.Region
FROM country JOIN city ON country.Code = city.CountryCode 
AND city.Population < 100000
WHERE country.SurfaceArea < 1000 
ORDER BY country.Region;