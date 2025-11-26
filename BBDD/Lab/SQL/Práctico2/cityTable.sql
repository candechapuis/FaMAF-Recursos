USE `world`;

CREATE TABLE `city` (
	ID INT PRIMARY KEY,
	Name VARCHAR(50),
	CountryCode CHAR(3),
	District VARCHAR(50),
	Population INT,
	FOREIGN KEY (CountryCode) REFERENCES country(Code)
);