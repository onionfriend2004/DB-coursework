SELECT v.main_complaints, v.prescriptions, v.visit_date, p.card_number
FROM visits v
JOIN patients p ON v.patient_id = p.card_number
WHERE v.diagnosis LIKE '%$keyword%';
