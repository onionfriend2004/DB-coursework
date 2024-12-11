SELECT 1
FROM visits
WHERE doctor_id = '$doctor'
    AND appointment_date = '$appointment_date'
    AND appointment_time_start = '$appointment_time_start'
    AND appointment_time_end = '$appointment_time_end'
