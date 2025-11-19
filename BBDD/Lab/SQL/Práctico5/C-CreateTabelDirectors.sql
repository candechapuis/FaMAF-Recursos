USE `sakila`;

CREATE TABLE directors (
	director_id SMALLINT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(45) NOT NULL,
	last_name VARCHAR(45) NOT NULL,
	number_of_films SMALLINT NOT NULL DEFAULT '0',
	PRIMARY KEY (director_id)
);