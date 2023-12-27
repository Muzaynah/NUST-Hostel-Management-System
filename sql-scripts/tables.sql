
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
sRoomNumber INT NOT NULL,
sBatch INT NOT NULL,
sUsername VARCHAR(50),
sPassword VARCHAR(50) NOT NULL,
sProgram VARCHAR(50),
HID INT,
dID INT,
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
cms INT,
CONSTRAINT guardianpk PRIMARY KEY(cms,gName)
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
    cms INT,
    CONSTRAINT ostatus_constraint CHECK(OStatus IN ('Pending', 'Approved', 'Rejected')),
    CONSTRAINT outpasspk PRIMARY KEY(OID),
    CONSTRAINT date_validity CHECK(LeavingDate < JoiningDate)
);


CREATE TABLE IF NOT EXISTS Complaint(
	CID INT AUTO_INCREMENT NOT NULL ,
    CDescription VARCHAR(500) NOT NULL,
    CStatus VARCHAR(50) DEFAULT 'Pending' NOT NULL,
    CDate DATE NOT NULL,
    cms INT,
    CONSTRAINT complaintpk PRIMARY KEY(CID),
    CONSTRAINT cstatus_constraint CHECK(CStatus IN ("Pending","Resolved"))
);

CREATE TABLE IF NOT EXISTS Manager(
	MID INT NOT NULL,
    mFirstName CHAR(50) NOT NULL,
    mLastName CHAR(50) NOT NULL,
    mUsername VARCHAR(50),
    mPassword VARCHAR(50),
    HID INT,
    CONSTRAINT managerpk PRIMARY KEY(MID)
);


CREATE TABLE IF NOT EXISTS AttendanceEvent(
	ADate DATE NOT NULL,
    Attendance BOOLEAN NOT NULL,
    cms INT NOT NULL,
    CONSTRAINT attendanceeventpk PRIMARY KEY(ADate, cms)
);

CREATE TABLE IF NOT EXISTS Notifications(
    NID INT AUTO_INCREMENT,
    NText VARCHAR(1000),
    NDate DATE NOT NULL,
    HID INT,
    CONSTRAINT notificationspk PRIMARY KEY(NID)
);

ALTER TABLE Manager
ADD CONSTRAINT Manager_Hostel_Fk
FOREIGN KEY(HID) REFERENCES Hostel(HID);

ALTER TABLE Student 
ADD CONSTRAINT Student_Hostel_Fk
FOREIGN KEY(HID) REFERENCES Hostel(HID);

ALTER TABLE Guardian
ADD CONSTRAINT Guardian_Student_Fk
FOREIGN KEY(cms) REFERENCES Student(cms);

ALTER TABLE Student 
ADD CONSTRAINT Student_Department_Fk
FOREIGN KEY(dID) REFERENCES Department(dID);

ALTER TABLE AttendanceEvent
ADD CONSTRAINT Attendance_Student_Fk
FOREIGN KEY(cms) REFERENCES Student(cms);

ALTER TABLE Complaint 
ADD CONSTRAINT Complain_Student_Fk
FOREIGN KEY(cms) REFERENCES Student(cms);

ALTER TABLE Outpass
ADD CONSTRAINT Outpass_Student_Fk
FOREIGN KEY(cms) REFERENCES Student(cms);

ALTER TABLE Notifications
ADD CONSTRAINT Notifications_Hostel_Fk
FOREIGN KEY(HID) REFERENCES Hostel(HID);

