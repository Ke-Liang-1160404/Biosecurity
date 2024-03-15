create schema Biosecurity;

use Biosecurity;


CREATE TABLE IF NOT EXISTS `apiarists`
(
`apiarists_id` INT auto_increment PRIMARY KEY NOT NULL,
`first_name` varchar(25),
`last_name` varchar(25) not null,
`username` varchar(100) NOT NULL,
`password` varchar(255) NOT NULL,
`email` varchar(320) UNIQUE,
`address` varchar(320) not null,
`phone` varchar(15) not null,
`date_joined` date NOT NULL,
`status` tinyint default 1
);

CREATE TABLE IF NOT EXISTS `staff_admin`
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

CREATE TABLE IF NOT EXISTS `pest_disease`
(
`id` INT auto_increment PRIMARY KEY NOT NULL,
`item_type` ENUM('pest','disease') not null,
`presence` tinyint default 0,
`common_name` varchar(25) not null,
`scientific_name` varchar(50) not null,
`key_characteristics` varchar(320) not null,
`biology_description` varchar(1000) not null,
`symptoms` varchar(320) not null,
`primary_image` varchar(25) not null
);


CREATE TABLE IF NOT EXISTS `images` (
  `image_id` INT NOT NULL,
  `pest_id` INT NOT NULL,
  `image_url` VARCHAR(100) NULL,
  UNIQUE INDEX `image_id_UNIQUE` (`image_id` ASC) VISIBLE,
  INDEX `id_idx` (`pest_id` ASC) VISIBLE,
  CONSTRAINT `id`
    FOREIGN KEY (`pest_id`)
    REFERENCES `pest_disease` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- Sample data for Staff/Admin
INSERT INTO staff_admin (`first_name`, `last_name`, `username`, `password`, `email`, `address`, `work_phone_number`, `hire_date`, `position`, `department`, `status`)
VALUES
('Emily', 'Brown', 'emily_brown', '3f9a05750d8bf6d7ba9d3c2444c2ac30479afc44d814308460eb8816ad1ce03b', 'emily.brown@staff.com', '123 Bee St, Auckland', '111-222-3333', '2022-01-15', 'staff', 'Research', 1),
('David', 'Wilson', 'david_wilson', '8882834cabdb4f0dfae4b2892798c0bd69d3f090cc8d5d07ee3535d0d04ccb4b', 'david.wilson@staff.com', '456 Honey Rd, Wellington', '444-555-6666', '2021-12-20', 'staff', 'Research', 1),
('Sarah', 'Jones', 'sarah_jones', 'bb7e9554ebf937bfce131d79ec74dfc6eaa3138fdaa78756e53256654a8fabf1', 'sarah.jones@staff.com', '789 Pollen Ave, Christchurch', '777-888-9999', '2023-03-10', 'staff', 'Marketing', 1),
('John', 'Murray', 'john_murray', '674f27c0c25a522dfd497dd8e147ddbe006d11a57f0a543c0013b2329e26617e', 'john.murray@admin.com', '123 Victoria Rd, Wellington', '444-555-6666', '2021-12-20', 'admin', 'Manager', 1);



-- Sample data for Apiarists
INSERT INTO apiarists (`first_name`, `last_name`, `username`, `password`, `email`, `address`, `phone`, `date_joined`, `status`)
VALUES
('Michael', 'Smith', 'michael_smith', '3f9a05750d8bf6d7ba9d3c2444c2ac30479afc44d814308460eb8816ad1ce03b', 'michael.smith@example.com', '10 Honeycomb St, Auckland', '123-456-7890', '2023-05-10', 1),
('Emma', 'Johnson', 'emma_johnson', '8882834cabdb4f0dfae4b2892798c0bd69d3f090cc8d5d07ee3535d0d04ccb4b', 'emma.johnson@example.com', '20 Beehive Rd, Wellington', '987-654-3210', '2024-02-15', 1),
('William', 'Davis', 'william_davis', 'bb7e9554ebf937bfce131d79ec74dfc6eaa3138fdaa78756e53256654a8fabf1', 'william.davis@example.com', '30 Pollen Way, Christchurch', '555-555-5555', '2022-10-20', 0);


INSERT INTO pest_disease (item_type, presence, common_name, scientific_name, key_characteristics, biology_description, symptoms, primary_image)
VALUES
('pest', '1', 'Varroa mite', 'Varroa destructor', 'External parasite of adult bees and brood', 'Varroa mites reproduce in honeybee colonies', 'Deformed wings, reduced lifespan of bees',1),
('pest', '0', 'Small Hive Beetle', 'Aethina tumida', 'Small dark beetle', 'Larvae damage combs and honey', 'Slimy comb and honey',2),
('disease', '1', 'American Foulbrood', 'Paenibacillus larvae', 'Bacterial infection', 'Spores spread through contaminated equipment', 'Discolored larvae',3),
('disease', '1', 'Nosema', 'Nosema apis', 'Microsporidian parasite', 'Infects the gut of bees', 'Dysentery',4),
('pest', '0', 'European Foulbrood', 'Melissococcus plutonius', 'Bacterial infection', 'Affects bee larvae', 'Ropey texture in larvae',5),
('pest', '0', 'Tropilaelaps mite', 'Tropilaelaps spp.', 'Parasitic mites', 'Attacks brood cells and adults', 'Deformed wings, reduced lifespan of bees',6),
('pest', '0', 'Asian Hornet', 'Vespa velutina', 'Large hornet species', 'Preys on honeybees', 'Attack honeybee hives',7),
('disease', '1', 'Chalkbrood', 'Ascosphaera apis', 'Fungal infection', 'Affects bee larvae', 'White mummified larvae',8),
('pest', '0', 'Wax Moth', 'Galleria mellonella', 'Moth larvae', 'Destroys comb and honey', 'Webbing and cocoons in hive',9),
('disease', '1', 'Sacbrood Virus', 'Sacbrood virus', 'Viral infection', 'Affects bee larvae', 'Dead larvae with sac-like appearance', 10),
('disease', '1', 'Deformed Wing Virus', 'Deformed wing virus', 'Viral infection', 'Named after the main symptom of wing deformities in adult honey bees, can also affect all life stages and castes of bees', 'Deformed wings in adult bees; other symptoms not easily observed', 11),
('disease', '1', 'Manuka tree bee disease', 'Pseudomonas syringae pv. manuka', 'Bacterial infection', 'Affects bees pollinating Manuka trees', 'Reduced honey production', 12),
('pest', '1', 'Southern Bee Mite', 'Varroa jacobsoni', 'External parasite of adult bees and brood', 'Similar to Varroa destructor', 'Deformed wings, reduced lifespan of bees', 13),
('disease', '1', 'Nosema ceranae', 'Nosema ceranae', 'Microsporidian parasite', 'Infects the gut of bees', 'Dysentery', 14),
('pest', '1', 'European Bee Eater', 'Merops apiaster', 'Bird species', 'Feeds on bees', 'Direct predation on bees', 15),
('pest', '0', 'Africanized Honey Bee', 'Apis mellifera scutellata', 'Aggressive honey bee hybrid', 'Interbreeding of European and African honey bees', 'Aggressive behavior, mass stinging', 16),
('pest', '0', 'Varroa jacobsoni', 'Varroa jacobsoni', 'External parasite of adult bees and brood', 'Affects mainly Asian honeybee species', 'Deformed wings, reduced lifespan of bees', 17),
('disease', '0', 'Stonebrood', 'Aspergillus spp.', 'Fungal infection', 'Affects bee larvae', 'Hardened mummified larvae', 18),
('pest', '0', 'Hornet Moth', 'Sesia apiformis', 'Moth species', 'Resembles hornets', 'Mimicry of hornet appearance', 19),
('disease', '0', 'Black Queen Cell Virus', 'Black queen cell virus', 'Viral infection', 'Affects bee larvae', 'Darkened and perforated queen cells', 20);

INSERT INTO images (image_id, pest_id, image_url) VALUES
(1, 1, 'varroa-mite.jpeg'),
(2, 2, 'small-hive-bettle.jpeg'),
(3, 3, 'American-Foulbrood.jpeg'),
(4, 4, 'Nosema.jpeg'),
(5, 5, 'European-Foulbrood.jpeg'),
(6, 6, 'Tropilaelaps-mite.jpeg'),
(7, 7, 'Asian-Hornet.jpeg'),
(8, 8, 'chalkbrood.jpeg'),
(9, 9, 'Wax-Moth.jpeg'),
(10, 10, 'Sacbrood-Virus.jpeg'),
(11, 11, 'Deformed-Wing-Virus.jpeg'),
(12, 12, 'Manuka-tree-bee-disease.jpeg'),
(13, 13, 'Southern-Bee-Mite.jpeg'),
(14, 14, 'Nosema-ceranae.jpeg'),
(15, 15, 'European-Bee-Eater.jpeg'),
(16, 16, 'Africanized-Honey-Bee.jpeg'),
(17, 17, 'Varroa-jacobsoni.jpeg'),
(18, 18, 'Stonebrood.jpeg'),
(19, 19, 'Hornet-Moth.jpeg'),
(20, 20, 'Black-Queen-Cell-Virus.jpeg'),
(21, 1, 'varroa-mite-1.jpeg'),
(22, 2, 'small-hive-bettle-1.jpeg'),
(23, 3, 'American-Foulbrood-1.jpeg'),
(24, 4, 'Nosema-1.jpeg'),
(25, 5, 'European-Foulbrood-1.jpeg'),
(26, 6, 'Tropilaelaps-mite-1.jpeg'),
(27, 7, 'Asian-Hornet-1.jpeg'),
(28, 8, 'chalkbrood-1.jpeg'),
(29, 9, 'Wax-Moth-1.jpeg'),
(30, 10, 'Sacbrood-Virus-1.jpeg'),
(31, 11, 'Deformed-Wing-Virus-1.jpeg'),
(32, 12, 'Manuka-tree-bee-disease-1.jpeg'),
(33, 13, 'Southern-Bee-Mite-1.jpeg'),
(34, 14, 'Nosema-ceranae-1.jpeg'),
(35, 15, 'European-Bee-Eater-1.jpeg'),
(36, 16, 'Africanized-Honey-Bee-1.jpeg'),
(37, 17, 'Varroa-jacobsoni-1.jpeg'),
(38, 18, 'Stonebrood-1.jpeg'),
(39, 19, 'Hornet-Moth-1.jpeg'),
(40, 20, 'Black-Queen-Cell-Virus-1.jpeg'),
(41, 3, 'American-Foulbrood-2.jpeg');


