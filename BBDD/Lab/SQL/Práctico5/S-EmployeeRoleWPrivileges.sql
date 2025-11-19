USE `sakila`;

CREATE ROLE IF NOT EXISTS employee;
GRANT INSERT, DELETE, UPDATE
ON rental 
TO employee;