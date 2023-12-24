CREATE TRIGGER IF NOT EXISTS generate_student_username
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
    SET NEW.sUsername = CONCAT(LOWER(LEFT(NEW.sFirstName, 1)), LOWER(NEW.sLastName),NEW.cms);
END;