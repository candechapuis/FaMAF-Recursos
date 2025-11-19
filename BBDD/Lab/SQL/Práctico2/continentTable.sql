USE `world`;

CREATE TABLE `Continent` (
	`Name` enum('Asia','Europe','North America','Africa','Oceania','Antarctica','South America') NOT NULL DEFAULT 'Asia',
	`Surface` decimal(10,2) NOT NULL DEFAULT '0.00',
	`PercentTotalMass` decimal(4,1) NOT NULL DEFAULT '0.0',
	`MostPopulousCity` INT NOT NULL DEFAULT '0',
	PRIMARY KEY (`Name`),
	CONSTRAINT `continent_ibfk_1` FOREIGN KEY (`MostPopulousCity`) REFERENCES city(ID)
);