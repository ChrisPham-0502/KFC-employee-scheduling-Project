CREATE DATABASE Schedule_Project;
GO

USE Schedule_Project;

CREATE TABLE Branches (
  BranchID INT IDENTITY(1,1) PRIMARY KEY,
  BranchName VARCHAR(50)
);
GO

CREATE TABLE Employees (
  EmployeeID INT IDENTITY(1,1) PRIMARY KEY,
  BranchID INT,
  FullName VARCHAR(50),
  Email VARCHAR(200),
  Phone VARCHAR(12),
  Password VARCHAR(30),
  Role VARCHAR(30),
  Type CHAR(1) CHECK (Type IN ('F', 'P')),
  Status INT CHECK (Status = 1 OR Status = 0),
  FOREIGN KEY (BranchID) REFERENCES Branches (BranchID)
);
GO


CREATE TABLE Timetables (
  TimetableID INT IDENTITY(1,1) PRIMARY KEY,
  CreateDate DATE,
  ExpiredDate DATE
);
GO

CREATE TABLE TimetableDetails (
  DetailID INT IDENTITY(1,1) PRIMARY KEY,
  TimetableID INT,
  EmployeeID INT,
  Schedule VARCHAR(50),
  Status INT CHECK (Status = 1 OR Status = 0),
  FOREIGN KEY (TimetableID) REFERENCES Timetables (TimetableID),
  FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID)
);
GO

CREATE TABLE Results (
  ResultID INT IDENTITY(1,1) PRIMARY KEY,
  EmployeeID INT,
  Month INT,
  Year INT,
  Salary DECIMAL(10,2),
  FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID)
);
GO

CREATE TABLE SwapRequests (
  RequestID INT IDENTITY(1,1) PRIMARY KEY,
  RequesterID INT,
  RequesteeID INT,
  TimetableID INT,
  Schedule VARCHAR(50),
  Status INT CHECK (Status = 1 OR Status = 0),
  FOREIGN KEY (RequesterID) REFERENCES Employees (EmployeeID),
  FOREIGN KEY (RequesteeID) REFERENCES Employees (EmployeeID),
  FOREIGN KEY (TimetableID) REFERENCES Timetables (TimetableID)
);
GO
