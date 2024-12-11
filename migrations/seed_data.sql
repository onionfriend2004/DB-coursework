USE clinic_database;

-- Вставка данных в таблицу пользователей
INSERT INTO users (username, user_password, user_role)
VALUES 
    ('registrator', '1', 'registrator'),
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

-- Вставка данных в таблицу schedules на 2024 год
INSERT INTO schedules (appointment_date, appointment_time_start, appointment_time_end, doctor_id, office_id, is_busy)
VALUES
    ('2024-01-01', '09:00:00', '10:00:00', 1, 1, TRUE),
    ('2024-01-01', '10:00:00', '11:00:00', 2, 3, TRUE),
    ('2024-01-01', '11:00:00', '12:00:00', 3, 5, TRUE),
    ('2024-01-02', '09:00:00', '10:00:00', 1, 2, TRUE),
    ('2024-01-02', '10:00:00', '11:00:00', 2, 4, TRUE),
    ('2024-01-02', '11:00:00', '12:00:00', 3, 6, TRUE);
