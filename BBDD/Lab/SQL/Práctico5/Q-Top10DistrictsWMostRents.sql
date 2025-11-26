USE `sakila`;

SELECT a.district, RentsPerShop.AmountOfRents 
FROM address AS a JOIN (
	SELECT store.address_id AS store_address, RentsPerStaff.AmountOfRents 
	FROM store JOIN 
		(SELECT staff.staff_id AS staff_id, COUNT(*) AS AmountOfRents 
		FROM staff JOIN rental ON rental.staff_id = staff.staff_id 
		GROUP BY staff.staff_id) AS RentsPerStaff
	ON RentsPerStaff.staff_id = store.manager_staff_id) AS RentsPerShop
ON RentsPerShop.store_address = a.address_id;


