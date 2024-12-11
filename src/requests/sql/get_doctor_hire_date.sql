SELECT
    doctor_name AS 'Имя врача',
    birth_date AS 'Дата рождения',
    specialization AS 'Специальность',
    employment_date AS 'Дата приема на_работу'
FROM
    doctors
WHERE
    YEAR(employment_date) = '$year' AND
    MONTH(employment_date) = '$month';
