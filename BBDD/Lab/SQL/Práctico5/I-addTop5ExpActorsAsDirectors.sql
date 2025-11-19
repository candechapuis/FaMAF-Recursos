USE `sakila`;
	
INSERT INTO directors (director_id, first_name, last_name, number_of_films)
SELECT f.actor_id, a.first_name, a.last_name, count(*) AS number_films
	FROM film_actor AS f JOIN actor AS a ON f.actor_id = a.actor_id 
	GROUP BY f.actor_id
	ORDER BY number_films DESC
	LIMIT 5;
	
