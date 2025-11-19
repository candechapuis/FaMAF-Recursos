-- base de datos a usar
USE olympics;

-- 1. Crear un campo nuevo `total_medals` en la tabla `person` que almacena la
-- cantidad de medallas ganadas por cada persona. Por defecto, con valor 0.

ALTER TABLE person 
ADD COLUMN total_medals INT DEFAULT 0;

-- 2. Actualizar la columna
-- `total_medals` de cada persona con el recuento real de
-- medallas que ganó. Por ejemplo, para Michael Fred Phelps II, luego de la
-- actualización debería tener como valor de `total_medals` igual a 28.

WITH medals_p_person AS (
	SELECT p.id AS id, COUNT(*) AS medals
	FROM competitor_event AS ce
	JOIN games_competitor AS gc
	ON ce.competitor_id = gc.id 
	JOIN person AS p
	ON gc.person_id = p.id
	WHERE ce.medal_id IN (1,2,3)
	GROUP BY p.id
)

UPDATE person
JOIN medals_p_person ON person.id = medals_p_person.id
SET person.total_medals = medals_p_person.medals;

-- total_medals debería ser 28
SELECT p.full_name, p.total_medals
FROM person AS p 
WHERE p.full_name = "Michael Fred Phelps, II";

-- 3. Devolver todos los medallistas olímpicos de Argentina, es decir, los que hayan
-- logrado alguna medalla de oro, plata, o bronce, enumerando la cantidad por tipo de
-- medalla. Por ejemplo, la query debería retornar casos como el siguiente:
-- (Juan Martín del Potro, Bronze, 1), (Juan Martín del Potro, Silver,1)

SELECT p.id, p.full_name, m.medal_name, COUNT(m.medal_name) AS "Amount"
FROM person AS p JOIN person_region AS pr
ON pr.person_id = p.id 
JOIN games_competitor AS gc
	ON p.id = gc.person_id
JOIN competitor_event AS ce
	ON gc.id = ce.competitor_id
JOIN medal AS m
	ON ce.medal_id = m.id
WHERE pr.region_id = 9 -- id 9 = ARG
	AND ce.medal_id IN (1,2,3)
GROUP BY m.medal_name, p.id, p.full_name;

-- 4. Listar el total de medallas ganadas por los deportistas argentinos en cada deporte.


SELECT s.sport_name, COUNT(*) AS "Medal Amount"
FROM person AS p JOIN person_region AS pr
ON pr.person_id = p.id 
JOIN games_competitor AS gc
	ON p.id = gc.person_id
JOIN competitor_event AS ce
	ON gc.id = ce.competitor_id
JOIN event AS e
	ON ce.event_id = e.id
JOIN sport AS s
	ON e.sport_id = s.id
WHERE 
	pr.region_id = 9 -- id 9 = ARG
	AND ce.medal_id IN (1,2,3)
GROUP BY s.sport_name;

-- 5. Listar el número total de medallas de oro, plata y bronce ganadas por cada país
-- (país representado en la tabla `noc_region`), agruparlas los resultados por pais.

SELECT nr.region_name, m.medal_name, COUNT(m.medal_name) AS "Amount"
FROM noc_region AS nr JOIN person_region AS pr
ON pr.region_id  = nr.id 
JOIN person AS p 
ON pr.person_id = p.id 
JOIN games_competitor AS gc
	ON p.id = gc.person_id
JOIN competitor_event AS ce
	ON gc.id = ce.competitor_id
JOIN medal AS m
	ON ce.medal_id = m.id
WHERE ce.medal_id IN (1,2,3)
GROUP BY m.medal_name, nr.region_name;

-- 6. Listar el país con más y menos medallas ganadas en la historia de las olimpiadas.

WITH medals_per_country AS (
	SELECT nr.region_name AS "Country", m.medal_name AS "Medal", COUNT(m.medal_name) AS "Amount"
	FROM noc_region AS nr JOIN person_region AS pr
	ON pr.region_id  = nr.id 
	JOIN person AS p 
	ON pr.person_id = p.id 
	JOIN games_competitor AS gc
		ON p.id = gc.person_id
	JOIN competitor_event AS ce
		ON gc.id = ce.competitor_id
	JOIN medal AS m
		ON ce.medal_id = m.id
	WHERE ce.medal_id IN (1,2,3)
	GROUP BY m.medal_name, nr.region_name
)

(
SELECT mp.Country, SUM(mp.Amount) AS "Total Amount Of Medals"
FROM medals_per_country AS mp
GROUP BY mp.Country
ORDER BY `Total Amount Of Medals` DESC
LIMIT 1
)
UNION
(
SELECT mp.Country, SUM(mp.Amount) AS "Total Amount Of Medals"
FROM medals_per_country AS mp
GROUP BY mp.Country
ORDER BY `Total Amount Of Medals` ASC
LIMIT 1
);

-- 7. Crear dos triggers:
-- a. Un trigger llamado `increase_number_of_medals` que incrementará en 1 el
-- valor del campo `total_medals` de la tabla `person`.
-- b. Un trigger llamado `decrease_number_of_medals` que decrementará en 1
-- el valor del campo `totals_medals` de la tabla `person`.


DROP TRIGGER IF EXISTS increase_number_of_medals;

DELIMITER $$

CREATE TRIGGER increase_number_of_medals
AFTER INSERT ON competitor_event
FOR EACH ROW
BEGIN
	
	DECLARE id_to_increase INT;
	
	SELECT gc.person_id INTO id_to_increase
	FROM competitor_event AS ce 
	JOIN games_competitor AS gc
		ON ce.competitor_id = gc.id
	WHERE ce.competitor_id = NEW.competitor_id
	LIMIT 1;
	
	IF (NEW.medal_id IN (1,2,3)) THEN
	
		UPDATE person
		SET total_medals = total_medals + 1
		WHERE person.id = id_to_increase;
		
	END IF;
		
END$$

DELIMITER ; 

DROP TRIGGER IF EXISTS decrease_number_of_medals;

DELIMITER $$

CREATE TRIGGER decrease_number_of_medals
AFTER DELETE ON competitor_event 
FOR EACH ROW 
BEGIN 
	
	DECLARE id_to_decrease INT;

	SELECT gc.person_id INTO id_to_decrease
	FROM competitor_event AS ce 
	JOIN games_competitor AS gc
		ON ce.competitor_id = gc.id
	WHERE ce.competitor_id = OLD.competitor_id
	LIMIT 1;
	
	IF (OLD.medal_id IN (1,2,3)) THEN
	
		UPDATE person
		SET total_medals = total_medals - 1
		WHERE person.id = id_to_decrease;
		
	END IF;
END$$


DELIMITER ;


WITH test_trigger AS (
	SELECT p.id, p.total_medals, gc.games_id, ce.event_id
	FROM person AS p JOIN games_competitor AS gc
		ON p.id = gc.person_id
	JOIN competitor_event AS ce
		ON ce.competitor_id = gc.id
	WHERE ce.competitor_id = 4
)

-- para ver el valor inicial de total_medals
SELECT * FROM test_trigger;

INSERT INTO competitor_event VALUES (11, 4, 3);

-- debería devolver total_medals = valor inicial + 1
SELECT  * FROM test_trigger;

DELETE FROM competitor_event
WHERE event_id = 11 AND competitor_id = 4;

-- total_medals debería volver a ser valor incial
SELECT  * FROM test_trigger;

-- 8. Crear un procedimiento `add_new_medalists` que tomará un `event_id`, y tres ids
-- de atletas `g_id`, `s_id`, y `b_id` donde se deberá insertar tres registros en la tabla
-- `competitor_event` asignando a `g_id` la medalla de oro, a `s_id` la medalla de
-- plata, y a `b_id` la medalla de bronce.
-----------------------------------------------------------
-- Si g_id, s_id y b_id son competitor_id(id de games_competitor), OK
-- Sino, debería agregar el game_id como input, sino no hay forma de obtener
-- un solo competitor_id solo con el person_id, ya que cada person_id
-- puede tener varios competitor_id, uno para cada juego en el que participó.
-- Agrego un input game_id para identificar el competitor al que debo agregale la medalla.

DROP PROCEDURE IF EXISTS add_new_medalists;

DELIMITER $$

CREATE PROCEDURE add_new_medalists(IN input_event_id INT,
									IN input_game_id INT,
									IN g_id INT,
									IN s_id INT,
									IN b_id INT)
BEGIN
	DECLARE g_competitor INT;
	DECLARE s_competitor INT;
	DECLARE b_competitor INT;
	
	SELECT gc.id INTO g_competitor
	FROM games_competitor AS gc 
	WHERE gc.person_id = g_id
		AND gc.games_id = input_game_id;
	
	SELECT gc.id INTO s_competitor
	FROM games_competitor AS gc 
	WHERE gc.person_id = s_id
		AND gc.games_id = input_game_id;
	
	SELECT gc.id INTO b_competitor
	FROM games_competitor AS gc 
	WHERE gc.person_id = b_id
		AND gc.games_id = input_game_id;
	
	INSERT INTO competitor_event (event_id, competitor_id, medal_id) 
		VALUES (input_event_id, g_competitor, 1);
	INSERT INTO competitor_event (event_id, competitor_id, medal_id)
		VALUES (input_event_id, s_competitor, 2);
	INSERT INTO competitor_event (event_id, competitor_id, medal_id)
		VALUES (input_event_id, b_competitor, 3);
	
	-- imprimo las filas insertadas
	
	SELECT p_id, gc.games_id, ce.competitor_id, ce.event_id, ce.medal_id
	FROM (
		SELECT p.id AS p_id
		FROM person AS p
		WHERE p.id IN (g_id, s_id, b_id)
		) AS athletes
	JOIN games_competitor AS gc
		ON p_id = gc.person_id
	JOIN competitor_event AS ce
		ON gc.id = ce.competitor_id
	WHERE gc.games_id = input_game_id
		AND ce.event_id = input_event_id;
	
	
END$$

DELIMITER ;

CALL add_new_medalists(15, 6, 5, 6, 7);

-- 9. Crear el rol `organizer` y asignarle permisos de eliminación sobre la tabla `games`
-- y permiso de actualización sobre la columna `games_name` de la tabla `games` .

CREATE ROLE IF NOT EXISTS `organizer`;

GRANT DELETE ON `games`
TO `organizer`;

GRANT UPDATE (`games_name`) ON `games` 
TO `organizer`;
































































































