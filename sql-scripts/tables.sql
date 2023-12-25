
CREATE DATABASE IF NOT EXISTS project;
use project;

CREATE TABLE IF NOT EXISTS Student (
cms INT NOT NULL,
sFirstName VARCHAR(50) NOT NULL,
sLastName VARCHAR(50) NOT NULL,
sAge INT NOT NULL,
sEmail VARCHAR(50) CHECK (sEmail LIKE '%@%') NOT NULL,
sPhoneNumber BIGINT NOT NULL,
city VARCHAR(50) NOT NULL,
street VARCHAR(10) NOT NULL,
house_no VARCHAR(10) NOT NULL,
full_address VARCHAR(150),
roomNumber INT NOT NULL,
sBatch INT NOT NULL,
sUsername VARCHAR(50),
sPassword VARCHAR(50) NOT NULL,
CONSTRAINT PkStudent PRIMARY KEY (cms)
);


CREATE TABLE IF NOT EXISTS Hostel(
hID INT PRIMARY KEY NOT NULL,
hName VARCHAR(50),
numberOfRooms INT,
numberOfStudents INT
);

CREATE TABLE IF NOT EXISTS Guardian(
gName VARCHAR(50),
gPhoneNumber BIGINT CHECK (LENGTH(gPhoneNumber) = 11) NOT NULL,
gEmail VARCHAR(50) CHECK (gEmail LIKE '%@%'),
cms INT NOT NULL,
constraint FkGuardian FOREIGN KEY(cms) REFERENCES Student(cms),
constraint PkGuardian PRIMARY KEY(cms, gName)
);

CREATE TABLE IF NOT EXISTS Department(
dID INT PRIMARY KEY NOT NULL,
dname VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Outpass(
    OID INT AUTO_INCREMENT,
    LeavingDate DATE NOT NULL,
    JoiningDate DATE NOT NULL,
    Purpose VARCHAR(100) NOT NULL,
    OStatus VARCHAR(50) DEFAULT 'Pending' NOT NULL,
    CONSTRAINT ostatus_constraint CHECK(OStatus IN ('Pending', 'Approved', 'Rejected')),
    CONSTRAINT outpasspk PRIMARY KEY(OID),
    CONSTRAINT date_validity CHECK(LeavingDate < JoiningDate)
);


CREATE TABLE IF NOT EXISTS Complaint(
	CID INT NOT NULL,
    CDescription VARCHAR(500) NOT NULL,
    CStatus VARCHAR(50) NOT NULL,
    CDate DATE NOT NULL,
    CONSTRAINT complaintpk PRIMARY KEY(CID),
    CONSTRAINT cstatus_constraint CHECK(CStatus IN ("Pending","Resolved"))
);
--  CONSTRAINT cdate_constraint CHECK(CDate <= CURRENT_DATE())

CREATE TABLE IF NOT EXISTS  Manager(
	MID INT NOT NULL,
    mFirstName CHAR(50) NOT NULL,
    mLastName CHAR(50) NOT NULL,
    mUsername VARCHAR(50),
    mPassword VARCHAR(50),
    CONSTRAINT managerpk PRIMARY KEY(MID)
);


CREATE TABLE IF NOT EXISTS AttendanceEvent(
	ADate DATE NOT NULL,
    Attendance BOOLEAN NOT NULL,
    cms INT NOT NULL,
    CONSTRAINT attendanceeventfk FOREIGN KEY(cms) REFERENCES Student(cms),
    CONSTRAINT attendanceeventpk PRIMARY KEY(ADate, cms)
);

