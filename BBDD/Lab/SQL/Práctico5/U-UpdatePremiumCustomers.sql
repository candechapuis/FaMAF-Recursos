USE `sakila`;

UPDATE customer 
SET premium_customer = 'T'
WHERE customer_id IN (
	SELECT t.customer_id
	FROM 
		(SELECT p.customer_id, SUM(p.amount) AS money_spent
		FROM payment AS p
		GROUP BY p.customer_id 
		ORDER BY money_spent DESC
		LIMIT 10) AS t);