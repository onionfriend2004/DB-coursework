SELECT doctor_name, patient_count, report_month, report_year
FROM doctor_patient_reports
WHERE report_month = '$month' AND report_year = '$year';
