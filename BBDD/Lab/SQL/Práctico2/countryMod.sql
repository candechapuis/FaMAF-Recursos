USE `world`;

ALTER TABLE `country`
ADD CONSTRAINT `country_ibfk_1`
FOREIGN KEY (`Continent`) REFERENCES `Continent`(`Name`);