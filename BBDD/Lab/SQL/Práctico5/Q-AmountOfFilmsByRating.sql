USE `sakila`;

SELECT f.rating, COUNT(*) AS AmountOfFilms
FROM film AS f
GROUP BY f.rating
ORDER BY AmountOfFilms;