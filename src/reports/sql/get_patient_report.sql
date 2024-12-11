SELECT
    doctor_name AS 'Имя врача',
    patient_count AS 'Количество пациентов',
    report_month AS 'Месяц отчета',
    report_year AS 'Год отчета'
FROM
    doctor_patient_reports
WHERE
    report_month = '$month' AND
    report_year = '$year';
