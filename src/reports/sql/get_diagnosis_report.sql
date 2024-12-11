SELECT
    diagnosis AS Диагноз,
    patient_count AS 'Количество пациентов',
    report_month AS 'Месяц отчета',
    report_year AS 'Год отчета'
FROM
    diagnosis_reports
WHERE
    report_month = '$month' AND
    report_year = '$year';
