USE `sakila`;

SELECT MONTH(p.payment_date) AS `Month`, AVG(p.amount) AS AvgPayment
FROM payment AS p
GROUP BY `Month`; 