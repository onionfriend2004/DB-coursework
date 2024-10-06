CREATE DATABASE clinic;
USE clinic;

CREATE TABLE patient(
    CardNumber INT NOT NULL AUTO_INCREMENT,
    PassportSerialNumber INT NOT NULL,
    Adress VARCHAR(45) NOT NULL,   
    Name VARCHAR(45) NOT NULL,
    Surname VARCHAR(45) NOT NULL,
    Fathername VARCHAR(45) NOT NULL,
    BirthDate DATE NOT NULL,
    CardCreationDate DATE NOT NULL,
    PRIMARY KEY (CardNumber)
);

