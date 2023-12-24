CREATE TRIGGER IF NOT EXISTS before_update_address
BEFORE UPDATE ON student
FOR EACH ROW
BEGIN
    SET NEW.full_address = CONCAT('City. ', NEW.city, ' Street ', NEW.street, ', House No. ', NEW.house_no);
END;