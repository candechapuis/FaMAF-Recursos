USE `world`;
	
SELECT country.Name,
	(SELECT MAX(Population)
	FROM city
	WHERE country.Code = city.CountryCode
	) AS `Population of Most Populated city`
FROM country;