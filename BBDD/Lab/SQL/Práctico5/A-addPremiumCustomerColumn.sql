USE `sakila`;

ALTER TABLE customer 
ADD premium_customer enum('T','F') NOT NULL DEFAULT 'F';