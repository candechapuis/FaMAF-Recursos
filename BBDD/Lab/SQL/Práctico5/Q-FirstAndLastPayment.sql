USE `sakila`;

SELECT MAX(p.payment_date) AS LastPaymentEver, 
	MIN(p.payment_date) AS FirstPaymentEver
FROM payment AS p;
