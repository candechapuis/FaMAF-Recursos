USE `airbnb_like_db`;

-- 1. Obtener los usuarios que han gastado más en reservas
SELECT u.id, u.name, SUM(p.amount) AS money_spent
FROM users AS u JOIN payments AS p
WHERE u.id = p.user_id
GROUP BY p.user_id
ORDER BY money_spent DESC
LIMIT 5;

-- 2. Obtener las 10 propiedades con el mayor ingreso total por reservas

SELECT p.id, p.name, p.location, total_income
FROM properties AS p JOIN (
	SELECT b.property_id, SUM(pay.amount) AS total_income
	FROM payments AS pay JOIN bookings AS b
	ON pay.booking_id = b.id AND pay.status = 'completed'
	GROUP BY b.property_id) AS propertyb_x_payment
ON propertyb_x_payment.property_id  = p.id
ORDER BY total_income DESC
LIMIT 10;


-- 3. Crear un trigger para registrar automáticamente reseñas negativas 
-- en la tabla de mensajes. Es decir, el owner recibe un mensaje al obtener 
-- un review menor o igual a 2

DROP TRIGGER IF EXISTS handle_bad_review;

DELIMITER $$

CREATE TRIGGER handle_bad_review
AFTER INSERT ON reviews
FOR EACH ROW
BEGIN
	DECLARE r_owner_id INT;
	IF (NEW.rating <= 2) THEN
	
		SELECT p.owner_id INTO r_owner_id
		FROM properties AS p
		WHERE p.id = NEW.property_id;

		INSERT INTO messages (sender_id, receiver_id, property_id, content)
		VALUES  (NEW.user_id, 
				r_owner_id,
				NEW.property_id,
				'Recibiste una mala review.');
	END IF;
END$$
DELIMITER ;

-- 4. Crear un procedimiento llamado process_payment que:
-- Reciba los siguientes parámetros:
-- - input_booking_id (INT): El ID de la reserva.
-- - input_user_id (INT): El ID del usuario que realiza el pago.
-- - input_amount (NUMERIC): El monto del pago.
-- - input_payment_method (VARCHAR): El método de pago utilizado (por ejemplo,
-- "credit_card", "paypal").

-- Requisitos: verificar si la reserva asociada existe y está en estado 
-- confirmed. Insertar un nuevo registro en la tabla payments. 
-- Actualizar el estado de la reserva a paid.


DROP PROCEDURE IF EXISTS process_payment; 

DELIMITER $$

CREATE PROCEDURE process_payment (IN input_booking_id INT,
									IN input_user_id INT,
									IN input_amount NUMERIC(10,2),
									IN input_payment_method VARCHAR(20))
	BEGIN 
		DECLARE b_id INT;

		SELECT b.id INTO b_id 
		FROM bookings AS b
		WHERE b.id = input_booking_id AND b.status = 'confirmed';
		
		IF (b_id IS NOT NULL) THEN
			INSERT INTO payments (booking_id, 
									user_id, 
									amount, 
									payment_method, 
									status)
			VALUES (input_booking_id, 
					input_user_id, 
					input_amount, 
					input_payment_method, 
					'completed');
		
			UPDATE bookings SET status = 'paid'
			WHERE bookings.id = input_booking_id;
		
		END IF;
			
	END$$
	
	DELIMITER ;
	
	-- not confirmed booking, nothing should happen
	CALL process_payment(1306, 1754,172, 'credit_card');
	-- not existent booking, nothing should happen
	CALL process_payment(1, 1754,172, 'credit_card');
	-- existent and confirmed booking, new row in payments should be added
	CALL process_payment(1302, 1747, 4834, 'credit_card');
	
	











































	
