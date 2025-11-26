USE `world`;

SELECT city.Name, country.Continent
FROM city
JOIN country ON country.Continent != 'Asia' AND city.CountryCode = country.Code
WHERE city.Population >= ANY (
			SELECT country.Population
			FROM country
			WHERE country.Continent = 'Asia'
);
