-- base de datos que uso

USE airbnb_like_db;

-- 1. Listar las 7 propiedades con la mayor cantidad de reviews en el año 2024.

SELECT p.name, p.location, COUNT(r.id) AS `Amount Of Reviews`
FROM reviews AS r JOIN properties AS p
ON r.property_id = p.id AND YEAR(r.created_at) = 2024
GROUP BY p.id
ORDER BY `Amount Of Reviews` DESC
LIMIT 7;

-- 2. Obtener los ingresos por reservas de cada propiedad.
-- Esta consulta debe calcular los ingresos totales generados por cada propiedad.
-- Ayuda: hay un campo `price_per_night` en la tabla de `properties` donde los
-- ingresos totales se computan sumando la cantidad de noches reservadas para cada
-- reserva multiplicado por el precio por noche.

-- usando total_price en bookings

SELECT p.Name, p.location, SUM(b.total_price) AS `Total Income Generated`
FROM bookings AS b JOIN properties AS p
ON b.property_id  = p.id
GROUP BY p.id;

-- usando price_per_night en properties

SELECT p.Name, p.location, SUM(DATEDIFF(b.check_out, b.check_in) * p.price_per_night) AS `Total Income Generated`
FROM bookings AS b JOIN properties AS p
ON b.property_id  = p.id
GROUP BY p.id;

-- 3. Listar los principales usuarios según los pagos totales.
-- Esta consulta calcula los pagos totales realizados por cada usuario y enumera los
-- principales 10 usuarios según la suma de sus pagos.


SELECT u.name, SUM(p.amount) AS `Total Payments`
FROM payments AS p JOIN users AS u
ON p.user_id = u.id AND p.status = "completed"
GROUP BY p.user_id 
ORDER BY `Total Payments` DESC
LIMIT 10;

-- 4. Crear un trigger notify_host_after_booking que notifica al anfitrión sobre una nueva
-- reserva. Es decir, cuando se realiza una reserva, notifique al anfitrión de la propiedad
-- mediante un mensaje.

DROP TRIGGER IF EXISTS notify_host_after_booking;

DELIMITER $$

CREATE TRIGGER notify_host_after_booking AFTER INSERT ON bookings
FOR EACH ROW
BEGIN
	INSERT INTO messages(sender_id, receiver_id, property_id, content, sent_at)
	SELECT b.user_id, p.owner_id, b.property_id, "Tienes una nueva reserva.", CURRENT_TIMESTAMP()
	FROM bookings AS b JOIN properties AS p 
	ON b.property_id = p.id AND b.id = NEW.id;
END$$

DELIMITER ;

INSERT INTO bookings(property_id, user_id, check_in, check_out, total_price, status, created_at)
VALUES (1603, 1737, '2024-10-26', '2024-11-02', 400.30, 'pending', CURRENT_TIMESTAMP());

SELECT *
FROM messages AS m
WHERE m.content = "Tienes una nueva reserva.";

-- 5. Crear un procedimiento add_new_booking para agregar una nueva reserva.
-- Este procedimiento agrega una nueva reserva para un usuario, según el ID de la
-- propiedad, el ID del usuario y las fechas de entrada y salida. Verifica si la propiedad
-- está disponible durante las fechas especificadas antes de insertar la reserva.

DROP PROCEDURE IF EXISTS add_new_booking;

DELIMITER $$

CREATE PROCEDURE add_new_booking(IN prop_id INT, IN u_id INT, IN c_in_d DATE, IN c_out_d DATE, OUT b_id INT)
BEGIN
	DECLARE price DECIMAL(10,2);
	SELECT COUNT(*) INTO b_id
	FROM bookings AS b
	WHERE b.property_id = prop_id AND b.check_in BETWEEN c_in_d AND c_out_d
	LIMIT 1;
	IF (b_id < 1) THEN
		SELECT (p.price_per_night * DATEDIFF(c_out_d, c_in_d)) INTO price
		FROM properties AS p
		WHERE p.id = prop_id;
		INSERT INTO bookings (property_id, user_id, check_in, check_out, total_price, status, created_at)
		VALUES (prop_id, u_id, c_in_d, c_out_d, price, "pending", CURRENT_TIMESTAMP());
		SET b_id = LAST_INSERT_ID();		
	ELSE
		SET b_id = 0;
	END IF;
END$$

DELIMITER ; 

SET @b_id = NULL;
-- fechas no ocupadas
CALL add_new_booking(1606, 1744, '2025-01-04', '2025-01-20', @b_id);
-- esto debería ser otra cosa que 0
SELECT @b_id;
-- fechas ocupadas (trigger)
CALL add_new_booking(1603, 1737, '2024-10-30', '2024-11-20', @b_id);
-- esto debería ser 0
SELECT @b_id;

-- 6. Crear el rol `admin` y asignarle permisos de creación sobre la tabla `properties` y
-- permiso de actualización sobre la columna `status` de la tabla `property_availability` .

CREATE ROLE IF NOT EXISTS admin;

GRANT INSERT ON properties
TO admin;

GRANT UPDATE (status) ON property_availability
TO admin;



























