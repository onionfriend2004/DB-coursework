SELECT
    doctor_name AS 'Имя врача',
    birth_date AS 'Дата рождения',
    specialization AS 'Специальность'
FROM
    doctors
WHERE
    specialization = '$specialization';
