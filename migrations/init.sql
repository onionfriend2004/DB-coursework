CREATE DATABASE clinic_database;
USE clinic_database;

-- Таблица отделений
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(255),
    department_floor INT,
    head_doctor_surname VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Таблица кабинетов
CREATE TABLE offices (
    office_id INT AUTO_INCREMENT PRIMARY KEY,
    office_number INT,
    office_type VARCHAR(255),
    office_area INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Таблица врачей
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    passport_serial_number VARCHAR(255),
    doctor_name VARCHAR(255),
    doctor_address VARCHAR(255),
    birth_date DATE,
    specialization VARCHAR(255),
    employment_date DATE,
    dismission_date DATE,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Таблица пациентов
CREATE TABLE patients (
    card_number INT AUTO_INCREMENT PRIMARY KEY,
    passport_serial_number VARCHAR(255),
    patient_address VARCHAR(255),
    patient_name VARCHAR(255),
    birth_date DATE,
    card_creation_date DATE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Таблица расписаний
CREATE TABLE schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_date DATE,
    appointment_time_start TIME,
    appointment_time_end TIME,
    doctor_id INT,
    office_id INT,
    is_busy BOOLEAN,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (office_id) REFERENCES offices(office_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Таблица посещений
CREATE TABLE visits (
    visit_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT,
    main_complaints VARCHAR(255),
    prescriptions VARCHAR(255),
    diagnosis VARCHAR(255),
    appointment_date DATE,
    appointment_time_start TIME,
    appointment_time_end TIME,
    patient_id INT,
    has_come BOOLEAN,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (patient_id) REFERENCES patients(card_number)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Таблица пользователей
CREATE TABLE users (
    username VARCHAR(50) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    user_role VARCHAR(20) NOT NULL,
    PRIMARY KEY (username)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Таблица отчетов врачей по пациентам
CREATE TABLE doctor_patient_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_name VARCHAR(255),
    patient_count INT,
    report_month INT,
    report_year INT
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Таблица отчетов по диагнозам
CREATE TABLE diagnosis_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    diagnosis VARCHAR(255),
    patient_count INT,
    report_month INT,
    report_year INT
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Процедура создания отчета по пациентам для врача
DELIMITER //

CREATE PROCEDURE create_patient_report(
    IN report_year INT,
    IN report_month INT
)
BEGIN
    -- Вставка данных, если есть совпадения
    INSERT INTO doctor_patient_reports (doctor_name, patient_count, report_month, report_year)
    SELECT
        COALESCE(d.doctor_name, NULL) AS doctor_name,
        COUNT(v.visit_id) AS patient_count,
        report_month,
        report_year
    FROM visits v
    RIGHT JOIN doctors d ON v.doctor_id = d.doctor_id
       AND MONTH(v.appointment_date) = report_month
       AND YEAR(v.appointment_date) = report_year
       AND v.has_come = TRUE
    GROUP BY d.doctor_id;

    -- Вставка строки с нулями, если ничего не найдено
    IF ROW_COUNT() = 0 THEN
        INSERT INTO doctor_patient_reports (doctor_name, patient_count, report_month, report_year)
        VALUES (NULL, 0, report_month, report_year);
    END IF;

    -- Возврат результатов
    SELECT * FROM doctor_patient_reports WHERE report_month = report_month AND report_year = report_year;
END //

DELIMITER ;

-- Процедура создания отчета по диагнозам
DELIMITER //

CREATE PROCEDURE create_diagnosis_report(
    IN report_year INT,
    IN report_month INT
)
BEGIN
    -- Вставка данных, если есть совпадения
    INSERT INTO diagnosis_reports (diagnosis, patient_count, report_month, report_year)
    SELECT
        COALESCE(v.diagnosis, NULL) AS diagnosis,
        COUNT(v.visit_id) AS patient_count,
        report_month,
        report_year
    FROM visits v
    WHERE MONTH(v.appointment_date) = report_month
      AND YEAR(v.appointment_date) = report_year
      AND v.diagnosis IS NOT NULL
    GROUP BY v.diagnosis;

    -- Вставка строки с нулями, если ничего не найдено
    IF ROW_COUNT() = 0 THEN
        INSERT INTO diagnosis_reports (diagnosis, patient_count, report_month, report_year)
        VALUES (NULL, 0, report_month, report_year);
    END IF;

    -- Возврат результатов
    SELECT * FROM diagnosis_reports WHERE report_month = report_month AND report_year = report_year;
END //

DELIMITER ;