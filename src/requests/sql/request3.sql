SELECT
    v.main_complaints AS 'Основные жалобы',
    v.prescriptions AS 'Назначения',
    v.visit_date AS 'Дата визита',
    p.card_number AS 'Номер карты'
FROM
    visits v
JOIN
    patients p ON v.patient_id = p.card_number
WHERE
    v.diagnosis LIKE '%$keyword%';
