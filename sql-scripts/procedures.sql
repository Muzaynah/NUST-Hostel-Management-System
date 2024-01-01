
CREATE PROCEDURE get_attendance_data(IN id INT)
BEGIN  
    SELECT ADate,Attendance FROM attendanceevent WHERE cms = id;
END;
--
CREATE PROCEDURE get_attendance_data_through_date(IN id INT,IN date DATE)
BEGIN  
    SELECT ADate,Attendance FROM attendanceevent WHERE ADate = date and cms=id;
END;
--
CREATE PROCEDURE get_attendance_data_through_attendance(IN id INT,IN a CHAR(20) )
BEGIN  
    SELECT ADate,Attendance FROM attendanceevent WHERE attendance=a and cms=id;
END;
--
CREATE PROCEDURE get_attendance_data_through_both_attendance_date(IN id INT,IN a CHAR(20),IN date DATE )
BEGIN  
    SELECT ADate,Attendance FROM attendanceevent WHERE attendance=a and cms = id and ADate=date;
END;
--
CREATE PROCEDURE get_all_student_data(
    IN id INT,
    OUT firstName VARCHAR(50),
    OUT lastName VARCHAR(50),
    OUT age INT,
    OUT email VARCHAR(50),
    OUT phoneNumber BIGINT,
    OUT city VARCHAR(50),
    OUT street VARCHAR(50),
    OUT house_no VARCHAR(10),
    OUT full_address VARCHAR(150),
    OUT roomNumber INT,
    OUT batch INT,
    out username VARCHAR(50),
    out password VARCHAR(50),
    out program VARCHAR(50),
    out hostel_id INT,
    out department_id INT,
    out hostel_name VARCHAR(50),
    OUT department_name VARCHAR(50)
)
BEGIN 
    SELECT sFirstName, sLastName, sAge, sEmail,sPhoneNumber,city,street,house_no,full_address,sRoomNumber,sBatch,sUsername,sPassword,sProgram,Student.HID,Student.dID,hname,dname
    INTO firstName, lastName, age, email,phoneNumber,city,street,house_no,full_address,roomNumber,batch,username,password,program,hostel_id,department_id,hostel_name,department_name
    FROM Student,Hostel,Department
    WHERE Student.cms = id and Student.HID = Hostel.HID and Student.dID = Department.dID;
END;
--
CREATE PROCEDURE get_all_student_data_through_hostel2(
    IN current_hostel_id INT
)
BEGIN 
    SELECT Student.cms,sFirstName,sLastName,sAge,sEmail,sPhoneNumber,City,Street,house_no,sRoomNumber,sBatch,Student.dID,Department.dname,sProgram,Student.HID,Hostel.hname
    FROM Student,Hostel,Department
    WHERE Student.HID = current_hostel_id and Student.dID = Department.dID and Student.HID=Hostel.HID;
END;
--
CREATE PROCEDURE get_outpass_data_through_cms(
    IN current_student_id INT
)
BEGIN
    SELECT OID, Purpose, LeavingDate, JoiningDate,Ostatus
    FROM Outpass
    WHERE cms = current_student_id;
END;
--