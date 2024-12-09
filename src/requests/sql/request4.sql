SELECT doctor_name, birth_date, specialization, employment_date
FROM doctors
WHERE YEAR(employment_date) = '$year'
AND MONTH(employment_date) = '$month';
