create schema biosecurity;

use biosecurity;

CREATE TABLE IF NOT EXISTS apiarists
(
apiarists_id INT auto_increment PRIMARY KEY NOT NULL,
first_name varchar(25),
last_name varchar(25) not null,
email varchar(320) UNIQUE,
address varchar(320) not null,
phone varchar(20) not null,
date_joined date NOT NULL,
status tinyint default 1
);

CREATE TABLE IF NOT EXISTS staff_admin
(
staff_id INT auto_increment PRIMARY KEY NOT NULL,
first_name varchar(25),
last_name varchar(25) not null,
email varchar(320) not null,
address varchar(320) not null,
work_phone_number varchar(20) not null,
hire_date date NOT NULL,
position varchar(25) not null,
department varchar(25) not null,
status tinyint default 1
);

CREATE TABLE IF NOT EXISTS pest_disease
(
id INT auto_increment PRIMARY KEY NOT NULL,
item_type ENUM('pest','disease') not null,
presence tinyint default 0,
common_name varchar(25) not null,
scientific_name varchar(25) not null,
key_characteristics varchar(320) not null,
biology_description varchar(1000) not null,
symptoms varchar(320) not null,
primary_image varchar(25) not null
);

-- Sample data for Apiarists
INSERT INTO apiarists (first_name, last_name, address, email, phone, date_joined, status)
VALUES
('John', 'Doe', '123 Beehive St, Auckland', 'john.doe@example.com', '123-456-7890', '2022-05-10', 1),
('Jane', 'Smith', '456 Honey Rd, Wellington', 'jane.smith@example.com', '987-654-3210', '2023-02-15', 1),
('Michael', 'Johnson', '789 Pollen Ave, Christchurch', 'michael.johnson@example.com', '555-555-5555', '2021-10-20', 0);

-- Sample data for Staff/Admin
INSERT INTO staff_admin (first_name, last_name, email, address, work_phone_number, hire_date, position, department, status)
VALUES
('Emily', 'Brown', 'emily.brown@example.com', 'Address 1', '111-222-3333', '2020-07-01', 'Manager', 'Operations', 1),
('David', 'Wilson', 'david.wilson@example.com', 'Address 2', '444-555-6666', '2019-09-15', 'Supervisor', 'Research', 1),
('Sarah', 'Jones', 'sarah.jones@example.com', 'Address 3', '777-888-9999', '2021-01-10', 'Coordinator', 'Marketing', 0);

INSERT INTO pest_disease (item_type, presence, common_name, scientific_name, key_characteristics, biology_description, symptoms, primary_image)
VALUES
('pest', 1, 'Varroa mite', 'Varroa destructor', 'External parasite', 'Varroa mites reproduce in brood cells and feed on both adult and larval bees.', 'Deformed wings, crawling bees, weakened colonies', 'varroa_mite.jpg'),
('pest', 1, 'Small hive beetle', 'Aethina tumida', 'Small beetle, larvae feed on hive contents', 'Small hive beetles can cause fermentation of honey, making it unpalatable for bees.', 'Slimy honey, beetles in the hive', 'small_hive_beetle.jpg'),
('disease', 1, 'American foulbrood', 'Paenibacillus larvae', 'Bacterial infection', 'Spores spread by infected bees and equipment.', 'Sunken, greasy-looking brood cappings', 'american_foulbrood.jpg');
