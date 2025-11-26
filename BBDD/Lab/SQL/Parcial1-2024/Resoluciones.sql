USE `airbnb_like_db`; 

-- 1. Listar las 7 propiedades con la mayor cantidad de reviews en el año 2024.

SELECT p.id, p.name, p.location, COUNT(*) AS amount_of_reviews
FROM properties AS p JOIN reviews AS r 
ON p.id = r.property_id AND YEAR(r.created_at) = 2024
GROUP BY p.id
ORDER BY amount_of_reviews DESC
LIMIT 7;

-- 2. Obtener los ingresos por reservas de cada propiedad.
-- Esta consulta debe calcular los ingresos totales generados por cada propiedad.
-- Ayuda: hay un campo `price_per_night` en la tabla de `properties` donde los
-- ingresos totales se computan sumando la cantidad de noches reservadas para cada
-- reserva multiplicado por el precio por noche.

-- Suponiendo que ingresos por reserva se refiere al total de los
-- ingresos que se estima tendrá la propiedad según las reservas
-- que tiene pendientes o confirmadas, sin importar si fueron o no
-- abonadas aún.

DROP FUNCTION IF EXISTS total_booking_price;

DELIMITER $$
CREATE FUNCTION total_booking_price(property_id INT, booking_id INT)
	RETURNS DECIMAL(10,2)
	READS SQL DATA
	BEGIN 
		DECLARE price_x_night DECIMAL(10,2);
		DECLARE total_price DECIMAL(10,2);

			SELECT p.price_per_night INTO price_x_night
			FROM properties AS p
			WHERE p.id = property_id;


			SELECT DATEDIFF(b.check_out, b.check_in) * price_x_night INTO total_price
			FROM bookings AS b
			WHERE b.id = booking_id;
		
	RETURN total_price;
	END$$
	
DELIMITER ; 
	
 
SELECT p.id, p.name, p.location, SUM(total_booking_price(p.id, b.id)) AS total_income_for_bookings
FROM properties AS p JOIN bookings AS b
ON p.id = b.property_id AND (b.status = 'pending' OR b.status = 'confirmed')
GROUP BY p.id
ORDER BY total_income_for_bookings;


-- 3. Listar los principales usuarios según los pagos totales.
-- Esta consulta calcula los pagos totales realizados por cada usuario y enumera los
-- principales 10 usuarios según la suma de sus pagos.

SELECT u.id, u.name, SUM(p.amount) AS total_payments
FROM users AS u JOIN payments AS p
ON u.id = p.user_id AND p.status = 'completed'
GROUP BY u.id 
ORDER BY total_payments DESC
LIMIT 10;

-- 4. Crear un trigger notify_host_after_booking que notifica al anfitrión sobre una nueva
-- reserva. Es decir, cuando se realiza una reserva, notifique al anfitrión de la propiedad
-- mediante un mensaje.

DROP TRIGGER IF EXISTS notify_host_after_booking;

DELIMITER $$

CREATE TRIGGER notify_host_after_booking
AFTER INSERT ON bookings
FOR EACH ROW
BEGIN 
	DECLARE receiver INT;
		SELECT p.owner_id INTO receiver
		FROM properties AS p
		WHERE p.id = NEW.property_id;

	INSERT INTO messages (sender_id, receiver_id, property_id, content)
	VALUES (NEW.user_id, receiver, NEW.property_id, 'You have a new booking.');
	
END$$
DELIMITER ;

INSERT INTO bookings (property_id, user_id, check_in, check_out, total_price, status)
VALUES (1603, 1737, '2026-01-04', '2026-01-20', 1300, 'pending');

SELECT *
FROM messages
WHERE content = 'You have a new booking.';


-- 5. Crear un procedimiento add_new_booking para agregar una nueva reserva.
-- Este procedimiento agrega una nueva reserva para un usuario, según el ID de la
-- propiedad, el ID del usuario y las fechas de entrada y salida. Verifica si la propiedad
-- está disponible durante las fechas especificadas antes de insertar la reserva.

DROP PROCEDURE IF EXISTS add_new_booking;

DELIMITER $$

CREATE PROCEDURE add_new_booking(IN input_user_id INT,
									IN input_property_id INT,
									IN input_check_in DATE,
									IN input_check_out DATE)
	BEGIN 
		DECLARE prop_is_occupied INT;
			SELECT COUNT(*) INTO prop_is_occupied
			FROM bookings AS b
			WHERE b.property_id = input_property_id 
			AND input_check_in BETWEEN b.check_in AND b.check_out;

		IF (prop_is_occupied < 1) THEN
			INSERT INTO bookings (property_id, 
			user_id, 
			check_in, 
			check_out, 
			total_price, 
			status)
			VALUES (input_property_id, 
			input_user_id, 
			input_check_in, 
			input_check_out,
			800,
			'pending');
			SELECT CONCAT('Booking inserted with ID = ', LAST_INSERT_ID()) AS result;
		ELSE
			SELECT 'Property is already booked in those dates.' AS result;
		END IF;
	END$$
	
DELIMITER ;

-- Occupied property during the dates(bc of the trigger test), 
-- nothing should change in db.
CALL add_new_booking(1737, 1603, '2026-01-15', '2026-01-17');

-- Free property, new booking should be added to db.
CALL add_new_booking(1738, 1604, '2026-04-15', '2026-04-17');

SELECT *
FROM bookings AS b
WHERE b.check_in = '2026-04-15';

-- 6. Crear el rol `admin` y asignarle permisos de creación sobre la tabla `properties` y
-- permiso de actualización sobre la columna `status` de la tabla
-- `property_availability` .


CREATE ROLE IF NOT EXISTS `admin`;

GRANT INSERT ON properties TO `admin`;

GRANT UPDATE (status) ON property_availability TO `admin`;


	
-- 7. Si ejecuto esta consulta:
-- START TRANSACTION;
-- UPDATE reviews
-- SET comment = 'bad'
-- WHERE rating = 1;
-- COMMIT;
-- Se va a asignar como comentario "bad" a todos los reviews con rating=1.
-- ¿Por qué esto no contradice la propiedad de Durabilidad de ACID en las transacciones,
-- ya que modifico los datos contenidos en la tabla reviews, cuando ya fueron cargados al
-- comienzo del parcial?

-- Porque la propiedad Durabilidad no implica Inmutabilidad, los cambios luego de un COMMIT
-- se hacen afectivos y durarán HASTA que haya alguna otra modificación válida sobre ellos. Esta
-- nueva modificación también DURARÁ en el tiempo luego de un COMMIT, hasta que haya
-- otra modificación válida.






















































































