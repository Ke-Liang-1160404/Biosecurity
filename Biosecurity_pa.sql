CREATE TABLE IF NOT EXISTS apiarists
(
`apiarists_id` INT auto_increment PRIMARY KEY NOT NULL,
`first_name` varchar(25),
`last_name` varchar(25) not null,
`email` varchar(320) UNIQUE,
`username` varchar(100) NOT NULL,
`password` varchar(255) NOT NULL,
`address` varchar(320) not null,
`phone` varchar(15) not null,
`date_joined` date NOT NULL,
`status` tinyint default 1
);

CREATE TABLE IF NOT EXISTS staff_admin
(
`staff_id` INT auto_increment PRIMARY KEY NOT NULL,
`first_name` varchar(25),
`last_name` varchar(25) not null,
`email` varchar(320) not null,
`username` varchar(100) NOT NULL,
`password` varchar(255) NOT NULL,
`address` varchar(320) not null,
`work_phone_number` varchar(15) not null,
`hire_date` date NOT NULL,
`position` varchar(25) not null,
`department` varchar(25) not null,
`status` tinyint default 1
);

CREATE TABLE IF NOT EXISTS pest_disease
(
`id` INT auto_increment PRIMARY KEY NOT NULL,
`item_type` ENUM('pest','disease') not null,
`presence` tinyint default 0,
`common_name` varchar(25) not null,
`scientific_name` varchar(25) not null,
`key_characteristics` varchar(320) not null,
`biology_description` varchar(1000) not null,
`symptoms` varchar(320) not null,
`primary_image` varchar(25) not null
);


-- Sample data for Staff/Admin
INSERT INTO staff_admin (`first_name`, `last_name`, `username`, `password`, `email`, `address`, `work_phone_number`, `hire_date`, `position`, `department`, `status`)
VALUES
('Emily', 'Brown', 'emily_brown', 'password123', 'emily.brown@example.com', '123 Bee St, Auckland', '111-222-3333', '2022-01-15', 'Manager', 'Operations', 1),
('David', 'Wilson', 'david_wilson', 'password456', 'david.wilson@example.com', '456 Honey Rd, Wellington', '444-555-6666', '2021-12-20', 'Supervisor', 'Research', 1),
('Sarah', 'Jones', 'sarah_jones', 'password789', 'sarah.jones@example.com', '789 Pollen Ave, Christchurch', '777-888-9999', '2023-03-10', 'Coordinator', 'Marketing', 0);


-- Sample data for Apiarists
INSERT INTO apiarists (`first_name`, `last_name`, `username`, `password`, `email`, `address`, `phone`, `date_joined`, `status`)
VALUES
('Michael', 'Smith', 'michael_smith', 'password123', 'michael.smith@example.com', '10 Honeycomb St, Auckland', '123-456-7890', '2023-05-10', 1),
('Emma', 'Johnson', 'emma_johnson', 'password456', 'emma.johnson@example.com', '20 Beehive Rd, Wellington', '987-654-3210', '2024-02-15', 1),
('William', 'Davis', 'william_davis', 'password789', 'william.davis@example.com', '30 Pollen Way, Christchurch', '555-555-5555', '2022-10-20', 0);


INSERT INTO pest_disease (item_type, presence, common_name, scientific_name, key_characteristics, biology_description, symptoms, primary_image)
VALUES
('pest', 1, 'Varroa mite', 'Varroa destructor', 'External parasite', 'Varroa mites reproduce in brood cells and feed on both adult and larval bees.', 'Deformed wings, crawling bees, weakened colonies', 'varroa_mite.jpg'),
('pest', 1, 'Small hive beetle', 'Aethina tumida', 'Small beetle, larvae feed on hive contents', 'Small hive beetles can cause fermentation of honey, making it unpalatable for bees.', 'Slimy honey, beetles in the hive', 'small_hive_beetle.jpg'),
('disease', 1, 'American foulbrood', 'Paenibacillus larvae', 'Bacterial infection', 'Spores spread by infected bees and equipment.', 'Sunken, greasy-looking brood cappings', 'american_foulbrood.jpg');
