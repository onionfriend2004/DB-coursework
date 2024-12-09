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

DELIMITER //

-- Процедура создания отчета по пациентам для врача
CREATE PROCEDURE create_patient_report(IN report_year INT, IN report_month INT)
BEGIN
    INSERT INTO doctor_patient_reports (doctor_name, patient_count, report_month, report_year)
    SELECT d.doctor_name, COUNT(v.visit_id), report_month, report_year
    FROM visits v
    JOIN doctors d ON v.doctor_id = d.doctor_id
    WHERE MONTH(v.appointment_date) = report_month AND YEAR(v.appointment_date) = report_year
    GROUP BY d.doctor_name;

    SELECT 0 AS error_code;
END //

-- Процедура создания отчета по диагнозам
CREATE PROCEDURE create_diagnosis_report(IN report_year INT, IN report_month INT)
BEGIN
    INSERT INTO diagnosis_reports (diagnosis, patient_count, report_month, report_year)
    SELECT v.diagnosis, COUNT(v.visit_id), report_month, report_year
    FROM visits v
    WHERE MONTH(v.appointment_date) = report_month AND YEAR(v.appointment_date) = report_year
    GROUP BY v.diagnosis;

    SELECT * FROM diagnosis_reports WHERE report_month = report_month AND report_year = report_year;
END //

DELIMITER ;


-- Вставка данных в таблицу пользователей
INSERT INTO users (username, user_password, user_role)
VALUES ('registrator', '1', 'registrator'),
       ('doctor', '1', 'doctor'),
       ('manager', '1', 'manager');

-- Вставка данных в таблицу departments
INSERT INTO departments (department_id, department_name, department_floor, head_doctor_surname)
VALUES
(1, 'Кардиология', 3, 'Иванов'),
(2, 'Неврология', 2, 'Петров'),
(3, 'Педиатрия', 1, 'Сидоров');

-- Вставка данных в таблицу offices
INSERT INTO offices (office_id, office_number, office_type, office_area, department_id)
VALUES
(1, 101, 'Кабинет осмотра', 20, 1),
(2, 102, 'Кабинет консультаций', 15, 1),
(3, 201, 'Кабинет осмотра', 25, 2),
(4, 202, 'Кабинет консультаций', 20, 2),
(5, 301, 'Кабинет осмотра', 18, 3),
(6, 302, 'Кабинет консультаций', 15, 3);

-- Вставка данных в таблицу doctors
INSERT INTO doctors (doctor_id, passport_serial_number, doctor_name, doctor_address, birth_date, specialization, employment_date, dismission_date, department_id)
VALUES
(1, 'АБ123456', 'Иванов Иван Иванович', 'ул. Ленина, 123', '1980-05-15', 'Кардиолог', '2010-06-01', NULL, 1),
(2, 'ВГ654321', 'Петров Петр Петрович', 'ул. Пушкина, 456', '1975-08-20', 'Невролог', '2005-09-15', NULL, 2),
(3, 'ДЕ987654', 'Сидоров Сидор Сидорович', 'ул. Лермонтова, 789', '1985-11-30', 'Педиатр', '2015-01-10', NULL, 3);

-- Вставка данных в таблицу patients
INSERT INTO patients (card_number, passport_serial_number, patient_address, patient_name, birth_date, card_creation_date)
VALUES
(1, 'ЕЖ123456', 'ул. Советская, 101', 'Иван Иванов', '1990-03-25', '2020-01-01'),
(2, 'ЗЫ654321', 'ул. Мира, 202', 'Анна Петрова', '1988-07-10', '2019-05-15'),
(3, 'ИК987654', 'ул. Лесная, 303', 'Дмитрий Сидоров', '1970-12-05', '2018-09-20');

-- Вставка данных в таблицу schedules
INSERT INTO schedules (schedule_id, appointment_date, appointment_time_start, appointment_time_end, doctor_id, office_id)
VALUES
(1, '2023-10-01', '09:00:00', '10:00:00', 1, 1),
(2, '2023-10-01', '10:00:00', '11:00:00', 2, 3),
(3, '2023-10-01', '11:00:00', '12:00:00', 3, 5),
(4, '2023-10-02', '09:00:00', '10:00:00', 1, 2),
(5, '2023-10-02', '10:00:00', '11:00:00', 2, 4),
(6, '2023-10-02', '11:00:00', '12:00:00', 3, 6);

-- Вставка данных в таблицу visits
INSERT INTO visits (visit_id, doctor_id, main_complaints, prescriptions, diagnosis, appointment_date, appointment_time_start, appointment_time_end, patient_id, has_come)
VALUES
(1, 1, 'Боль в груди', 'Прописать обследование', 'Ишемическая болезнь сердца', '2023-10-01', '09:00:00', '10:00:00', 1, TRUE),
(2, 2, 'Головная боль', 'Прописать обезболивающее', 'Мигрень', '2023-10-01', '10:00:00', '11:00:00', 2, TRUE),
(3, 3, 'Кашель', 'Прописать антибиотики', 'Бронхит', '2023-10-01', '11:00:00', '12:00:00', 3, TRUE),
(4, 1, 'Одышка', 'Прописать ингалятор', 'Астма', '2023-10-02', '09:00:00', '10:00:00', 1, TRUE),
(5, 2, 'Слабость', 'Прописать витамины', 'Анемия', '2023-10-02', '10:00:00', '11:00:00', 2, TRUE),
(6, 3, 'Температура', 'Прописать жаропонижающее', 'Грипп', '2023-10-02', '11:00:00', '12:00:00', 3, TRUE);