USE  `northwind`;

--  1.​ Listar los 5 clientes que más ingresos han generado a lo largo del tiempo.

-- versión corregida

SELECT c.`CustomerID`, (SUM(tp.`TotalPrice`)) AS `TotalIncome`
FROM `Customers` AS c JOIN 
	(SELECT o.`CustomerID`, SUM(od.`UnitPrice` * od.`Quantity` - (od.`UnitPrice` * od.`Quantity` * od.`Discount`)) AS `TotalPrice`
	FROM `Orders` AS o JOIN `Order Details` AS od
	ON o.`OrderID` = od.`OrderID`
	GROUP BY o.`OrderID`
	ORDER BY o.`CustomerID`, o.`OrderID`) AS `tp`
ON c.`CustomerID` = tp.`CustomerID`
GROUP BY c.`CustomerID`
ORDER BY `TotalIncome` DESC;

-- versión original

DROP FUNCTION IF EXISTS total_price_per_order;

DELIMITER $$

CREATE FUNCTION total_price_per_order(orderID INT)
	RETURNS DECIMAL (10,4)
	READS SQL DATA
	BEGIN
		DECLARE total_price_per_order DECIMAL(10,4);
		
			SELECT 
				SUM(o.`UnitPrice` * o.`Quantity` - (o.`UnitPrice` * o.`Quantity` * o.`Discount`))
				INTO total_price_per_order
			FROM `Order Details`AS o
			WHERE o.`OrderID` = orderID;
	
		RETURN total_price_per_order;

	END$$
	
DELIMITER ;

SELECT c.`CustomerID`, c.`ContactName`, SUM(total_price_per_order(o.`OrderID`)) AS totalIncomeGenerated
FROM `Customers` AS c JOIN Orders AS o 
ON c.CustomerID = o.CustomerID
GROUP BY c.`CustomerID`
ORDER BY totalIncomeGenerated DESC
LIMIT 5;

-- 2.​ Listar cada producto con sus ventas totales, agrupados por categoría.

--versión original

DROP FUNCTION IF EXISTS total_price_per_product;

DELIMITER $$

CREATE FUNCTION total_price_per_product(productID INT)
	RETURNS DECIMAL (10,4)
	READS SQL DATA
	BEGIN
		DECLARE total_price_per_product DECIMAL(10,4);
		
			SELECT 
				SUM(o.`UnitPrice` * o.`Quantity` - (o.`UnitPrice` * o.`Quantity` * o.`Discount`))
				INTO total_price_per_product
			FROM `Order Details`AS o
			WHERE o.`ProductID` = productID;
	
		RETURN total_price_per_product;

	END$$
	
DELIMITER ;

SELECT p.`ProductID`, p.`ProductName`, p.`CategoryID`, SUM(total_price_per_product(o.`ProductID`)) AS totalSales
FROM `Products` AS p JOIN `Order Details` AS o
ON p.ProductID = o.ProductID
GROUP BY p.`ProductID`
ORDER BY p.`CategoryID`;

--versión corregida

SELECT p.`ProductName`, c.`CategoryName`, SUM(od.`UnitPrice` * od.`Quantity` * (1-od.`Discount`)) AS `TotalSales`
FROM `Products` AS p JOIN `Categories` AS c
ON p.`CategoryID` = c.`CategoryID`
JOIN `Order Details` AS od
ON p.`ProductID` = od.`ProductID`
GROUP BY p.`ProductID`
ORDER BY c.`CategoryName`;


-- 3.​ Calcular el total de ventas para cada categoría.

-- versión original

SELECT c.`CategoryName`, SalesPerCategory.totalSales 
FROM `Categories` AS c JOIN (
	SELECT p.`CategoryID` AS `CategoryID`, SUM(total_price_per_product(o.`ProductID`)) AS totalSales
	FROM `Products` AS p JOIN `Order Details` AS o
	ON p.ProductID = o.ProductID
	GROUP BY p.`CategoryID`
	ORDER BY p.`CategoryID`) AS SalesPerCategory
ON c.`CategoryID`= SalesPerCategory.CategoryID;

--versión corregida

SELECT c.`CategoryName`, SUM(od.`UnitPrice` * od.`Quantity` * (1-od.`Discount`)) AS `TotalSales`
FROM `Products` AS p JOIN `Categories` AS c
ON p.`CategoryID` = c.`CategoryID`
JOIN `Order Details` AS od
ON p.`ProductID` = od.`ProductID`
GROUP BY c.`CategoryName`
ORDER BY c.`CategoryName`;

-- 4.​ Crear una vista que liste los empleados con más ventas por cada año, mostrando
-- empleado, año y total de ventas. Ordenar el resultado por año ascendente.

--versión original
-- No anda, devuelve las ventas totales de cada empleado.

DROP VIEW IF EXISTS SalesPerEmployees;

CREATE VIEW SalesPerEmployees AS
SELECT COUNT(o.`OrderDate`) AS TotalSalesPerEmployee, e.EmployeeID
FROM `Employees`AS e JOIN `Orders` AS o
ON e.EmployeeID = o.EmployeeID
GROUP BY e.EmployeeID;

SELECT * FROM SalesPerEmployees;

--versión corregida

DROP VIEW IF EXISTS BestSalerPerYear;

CREATE VIEW BestSalerPerYear AS

WITH SalesPerEmployee AS (
	SELECT e.`EmployeeID`,  YEAR(o.`OrderDate`) AS `Y`, SUM(od.`UnitPrice` * od.`Quantity` * (1-od.`Discount`)) AS `TotalPrice`
	FROM `Employees` AS e JOIN `Orders` AS o 
	ON e.`EmployeeID` = o.`EmployeeID`
	JOIN `Order Details`AS od
	ON o.`OrderID` = od.`OrderID`
	GROUP BY e.`EmployeeID`, `Y`)
	
SELECT m.`Yearr`, e.`FirstName`, e.`LastName`, m.`Sales`
FROM `SalesPerEmployee` AS s JOIN (
	SELECT s.`Y` AS `Yearr`, MAX(s.`TotalPrice`) AS `Sales`
	FROM `SalesPerEmployee` AS s
	GROUP BY s.`Y`) AS m
ON s.`TotalPrice` = m.`Sales`
JOIN `Employees` AS e 
ON e.`EmployeeID` = s.`EmployeeID`
ORDER BY m.`Yearr`;

SELECT * FROM BestSalerPerYear;


-- 5. Crear un trigger que se ejecute después de insertar un nuevo registro en la tabla
-- Order Details. Este trigger debe actualizar la tabla Products para disminuir la
-- cantidad en stock (UnitsInStock) del producto correspondiente, restando la
-- cantidad (Quantity) que se acaba de insertar en el detalle del pedido.

DROP TRIGGER IF EXISTS process_order;

DELIMITER $$

CREATE TRIGGER process_order
AFTER INSERT ON `Order Details`
FOR EACH ROW
BEGIN 
	UPDATE `Products`
	SET UnitsInStock = UnitsInStock - NEW.Quantity
	WHERE `Products`.ProductID = NEW.ProductID;
END$$

DELIMITER ; 

INSERT INTO `Order Details` VALUES (10248, 1, 18, 5, 0);

-- UnitsInStock before INSERT: 39, UnitsInStock expected after INSERT: 34
SELECT * FROM `Products` AS p WHERE p.ProductID = 1;

-- 6 .Crear un rol llamado admin y otorgarle los siguientes permisos:
●​ -- crear registros en la tabla Customers.
●​ -- actualizar solamente la columna Phone de Customers.


CREATE ROLE IF NOT EXISTS `admin`;

GRANT INSERT ON `Customers` TO `admin`;

GRANT UPDATE (Phone) ON `Customers` TO `admin`;











