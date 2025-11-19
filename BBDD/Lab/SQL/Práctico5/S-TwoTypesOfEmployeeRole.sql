USE `sakila`;

CREATE ROLE IF NOT EXISTS admin_employee;
CREATE ROLE IF NOT EXISTS simple_employee;

GRANT employee TO simple_employee;
GRANT administrator TO admin_employee;