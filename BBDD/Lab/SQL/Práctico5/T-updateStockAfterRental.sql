USE `sakila`;

-- Cree un trigger `update_stock` que, cada vez que se agregue un nuevo registro 
-- a la tabla rental, haga un update en la tabla `inventory` restando una copia 
-- al stock de la película rentada (Hint: revisar que el rental 
-- no tiene información directa sobre la tienda, sino sobre el cliente, 
-- que está asociado a una tienda en particular).
DELIMITER $$
CREATE TRIGGER update_stock 
AFTER INSERT ON rental 
FOR EACH ROW
BEGIN 
	UPDATE inventory 
	SET inventory.stock = inventory.stock - 1
	WHERE inventory_id = NEW.inventory_id
	AND inventory.stock > 0;
END$$
DELIMITER ;

	
