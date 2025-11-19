USE `world`;

SELECT country.Name, city.Name, city.Population
FROM country JOIN city
ON country.Code = city.CountryCode
WHERE city.Population >= ALL (
		SELECT city.Population
		FROM city
		WHERE country.Code = city.CountryCode);