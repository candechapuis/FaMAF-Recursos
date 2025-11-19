USE `sakila`;

CREATE TABLE fines ( 
	rental_id INT NOT NULL,
	amount DECIMAL(5,2) NOT NULL DEFAULT 0,
	PRIMARY KEY (rental_id, amount),
	CONSTRAINT fk_fine_rental FOREIGN KEY (rental_id) REFERENCES rental(rental_id)
);