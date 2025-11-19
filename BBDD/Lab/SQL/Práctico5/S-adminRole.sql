USE `sakila`;

REVOKE DELETE 
ON rental
FROM employee;

CREATE ROLE IF NOT EXISTS administrator;

GRANT ALL PRIVILEGES 
ON sakila.*
TO administrator;