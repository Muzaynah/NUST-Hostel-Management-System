grant execute on procedure get_attendance_data to 'student'@'localhost';

grant execute on procedure get_attendance_data_through_date to 'student'@'localhost';

grant execute on procedure get_attendance_data_through_attendance to 'student'@'localhost';

grant execute on procedure get_all_student_data to 'student'@'localhost';

grant insert on complaint to 'student'@'localhost';

grant insert on outpass to 'student'@'localhost';

grant execute on procedure get_outpass_data_through_cms to 'student'@'localhost';

grant execute on procedure get_complaint_data_through_cms to 'student'@'localhost';





grant execute on procedure get_all_student_data_through_hostel2 to 'manager'@'localhost';

grant select on manager to 'manager'@'localhost';

grant insert on attendanceevent to 'manager'@'localhost';

grant insert on student to 'manager'@'localhost';

grant insert on guardian to 'manager'@'localhost';

grant select on department to 'manager'@'localhost';

GRANT SELECT ON complaint TO 'manager'@'localhost';

GRANT UPDATE ON complaint TO 'manager'@'localhost';

GRANT SELECT ON outpass TO 'manager'@'localhost';

GRANT UPDATE ON outpass TO 'manager'@'localhost';

grant select on hostel to 'manager'@'localhost';

GRANT SELECT ON guardian TO 'manager'@'localhost';