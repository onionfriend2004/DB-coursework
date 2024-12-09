    SELECT
        s.appointment_time_start AS start,
        s.appointment_time_end AS end,
        d.doctor_name,
        d.doctor_id
    FROM
        schedules s
    JOIN
        doctors d ON s.doctor_id = d.doctor_id
    WHERE
        d.specialization = '$specialization' AND
        s.appointment_date = '$date';