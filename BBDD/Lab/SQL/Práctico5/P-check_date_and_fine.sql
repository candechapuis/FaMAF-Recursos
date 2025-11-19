USE `sakila`;

DROP PROCEDURE IF EXISTS check_date_and_fine;

DELIMITER $$
CREATE PROCEDURE check_date_and_fine()
	BEGIN
		INSERT INTO fines (rental_id, amount)
			SELECT r.rental_id, 
				   ((DATEDIFF(r.return_date, r.rental_date) - 3) * 1.5)
			FROM rental AS r
			WHERE DATEDIFF(r.return_date, r.rental_date) > 3;
	END$$
DELIMITER ;

CALL check_date_and_fine();
SELECT * FROM fines;

	
		