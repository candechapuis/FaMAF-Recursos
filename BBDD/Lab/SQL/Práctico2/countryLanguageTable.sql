USE `world`;

CREATE TABLE countryLanguage (
	CountryCode CHAR(3),
	Language VARCHAR(50),
	IsOfficial CHAR(1),
	Percentage NUMERIC(4,1)
);

ALTER TABLE countryLanguage 
ADD CONSTRAINT pk_countryLang 
PRIMARY KEY (CountryCode, Language);

ALTER TABLE countryLanguage 
ADD CONSTRAINT fk_countryCode
FOREIGN KEY (CountryCode) REFERENCES country(Code);