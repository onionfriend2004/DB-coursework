SELECT MONTH(card_creation_date) as 'Месяц', COUNT(*) as 'Количество'
FROM patients
WHERE YEAR(card_creation_date) = '$year'
GROUP BY month;