USE `world`;

CREATE TABLE country(
	Code CHAR(3),
	Name VARCHAR(50),
	Continent VARCHAR(12),
	Region VARCHAR(50),
	SurfaceArea INT,
	IndepYear INT,
	Population INT,
	LifeExpectancy DECIMAL(3,1),
	GNP INT,
	GNPOld INT,
	LocalName VARCHAR(50),
	GovernmentForm VARCHAR(50),
	HeadOfState VARCHAR(50),
	Capital INT,
	Code2 CHAR(2),
	CONSTRAINT pk_country PRIMARY KEY (Code)
);

	
	
