DROP DATABASE IF EXISTS scitrack;

CREATE DATABASE scitrack;

USE scitrack;

CREATE TABLE Member(
	memID INT PRIMARY KEY AUTO_INCREMENT,
    memName VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    memType VARCHAR(50) NOT NULL,
    memStart DATE NOT NULL,
    memEnd DATE,
    phone VARCHAR(20),
    CONSTRAINT chk_memType CHECK(memType IN (
    'postdoc',
	'research assistant',
	'research associate',
	'research technician',
	'masters student',
	'phd student',
	'research scientist',
    'Volunteer',
	'PI'
	))
);

CREATE TABLE PrmaryInvestigator(
	empID INT PRIMARY KEY,
    piID INT NOT NULL,
    FOREIGN KEY(empID) REFERENCES Member(memID),
    FOREIGN KEY(piID) REFERENCES Member(memID)
);

CREATE TABLE Supervisor(
	subID INT PRIMARY KEY,
    superID INT NOT NULL,
    supStart DATE NOT NULL,
    supEnd DATE,
	FOREIGN KEY(subID) REFERENCES Member(memID),
    FOREIGN KEY(superID) REFERENCES Member(memID)
);

CREATE TABLE Project(
	projID INT PRIMARY KEY AUTO_INCREMENT,
    projName VARCHAR(50) NOT NULL,
    projDesc VARCHAR(250) NOT NULL,
    pLead INT NOT NULL,
    pLeadStart DATE NOT NULL,
    PLeadEnd DATE,
    FOREIGN KEY(pLead) REFERENCES Member(memID)
);

CREATE TABLE Research(
	resID INT PRIMARY KEY AUTO_INCREMENT,
    resBody TEXT NOT NULL,
    citation VARCHAR(100)
);

CREATE TABLE Informs(
	resID INT NOT NULL,
    projID INT NOT NULL,
    PRIMARY KEY(resID,projID),
    FOREIGN KEY(resID) REFERENCES Research(resID),
    FOREIGN KEY(projID) REFERENCES Project(projID)
);

CREATE TABLE Procedures(
	procID INT PRIMARY KEY AUTO_INCREMENT,
    procName VARCHAR(50) NOT NULL,
    procBody TEXT NOT NULL
);

CREATE TABLE Experiment(
	expID INT PRIMARY KEY AUTO_INCREMENT,
    eLead INT NOT NULL,
    projID INT NOT NULL,
    expName VARCHAR(50) NOT NULL,
    pLeadStart DATE NOT NULL,
    pLeadEnd DATE,
	FOREIGN KEY(eLead) REFERENCES Member(memID),
    FOREIGN KEY (projID) REFERENCES Project(projID)
);

CREATE TABLE Spectra(
	spID INT PRIMARY KEY AUTO_INCREMENT,
    sName VARCHAR(500) NOT NULL,
    formula VARCHAR(250),
    numPeaks int NOT NULL,
    contributor VARCHAR(50) NOT NULL,
    casNo VARCHAR(10)
);

CREATE TABLE Sample(
	samID INT PRIMARY KEY AUTO_INCREMENT,
    expID INT NOT NULL,
    procID INT NOT NULL,
    samName VARCHAR(50),
    normFact INT,
    FOREIGN KEY(procID) REFERENCES Procedures(procID),
    FOREIGN KEY(expID) REFERENCES Experiment(expID)
);

CREATE TABLE Note(
	noteID INT PRIMARY KEY AUTO_INCREMENT,
    noteTS DATETIME DEFAULT CURRENT_TIMESTAMP,
    notBody TEXT
);

CREATE TABLE ProjNote(
	noteID INT PRIMARY KEY,
    projID INT NOT NULL,
    FOREIGN KEY(noteID) REFERENCES Note(noteID),
    FOREIGN KEY(projID) REFERENCES Project(projID)
);

CREATE TABLE ExpNote(
	noteID INT PRIMARY KEY,
    expID INT NOT NULL,
    FOREIGN KEY(noteID) REFERENCES Note(noteID),
    FOREIGN KEY(expID) REFERENCES Experiment(expID)
);

CREATE TABLE samSpectra(
	samID INT NOT NULL,
    spID INT NOT NULL,
    PRIMARY KEY(samID,spID),
    FOREIGN KEY(samID) REFERENCES Sample(samID),
    FOREIGN KEY(spID) REFERENCES Spectra(spID)
);

CREATE TABLE expSpectra(
	expID INT NOT NULL,
    spID INT NOT NULL,
    PRIMARY KEY(expID,spID),
    FOREIGN KEY(expID) REFERENCES Experiment(expID),
    FOREIGN KEY(spID) REFERENCES Spectra(spID)
);

CREATE TABLE Intensities(
	spID INT NOT NULL,
    mz INT NOT NULL,
    intensity INT NOT NULL,
    PRIMARY KEY(spID,mz,intensity),
    FOREIGN KEY(spID) REFERENCES Spectra(spID)
);