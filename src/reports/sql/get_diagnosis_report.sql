SELECT diagnosis, patient_count, report_month, report_year
FROM diagnosis_reports
WHERE report_month = '$month' AND report_year = '$year';
