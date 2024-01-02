--
CREATE VIEW StudentGuardiansAttendanceView AS
SELECT
    s.cms,
    s.sFirstName,
    s.sLastName,
    s.sAge,
    s.sEmail,
    s.sPhoneNumber,
    s.city AS StudentCity,
    s.street AS StudentStreet,
    s.house_no AS StudentHouseNo,
    s.full_address AS StudentFullAddress,
    s.sRoomNumber,
    s.sBatch AS StudentBatch,
    s.sUsername AS StudentUsername,
    s.sProgram AS StudentProgram,
    s.HID AS StudentHostelID,
    s.dID AS StudentDepartmentID,
    a.ADate,
    a.Attendance,
    g1.gName AS Guardian1Name,
    g1.gPhoneNumber AS Guardian1PhoneNumber,
    g1.gEmail AS Guardian1Email,
    g2.gName AS Guardian2Name,
    g2.gPhoneNumber AS Guardian2PhoneNumber,
    g2.gEmail AS Guardian2Email,
    g3.gName AS Guardian3Name,
    g3.gPhoneNumber AS Guardian3PhoneNumber,
    g3.gEmail AS Guardian3Email
FROM
    Student s
JOIN
    AttendanceEvent a ON s.cms = a.cms
LEFT JOIN
    Guardian g1 ON s.cms = g1.cms
LEFT JOIN
    Guardian g2 ON s.cms = g2.cms
LEFT JOIN
    Guardian g3 ON s.cms = g3.cms;
--