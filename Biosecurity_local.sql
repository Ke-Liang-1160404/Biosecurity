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
`scientific_name` varchar(25) not null,
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
('pest', '1', 'Varroa mite', 'Varroa destructor', 'External parasite of adult bees and brood', 'Varroa mites reproduce in honeybee colonies', 'Deformed wings, reduced lifespan of bees',2),
('pest', '1', 'Small Hive Beetle', 'Aethina tumida', 'Small dark beetle', 'Larvae damage combs and honey', 'Slimy comb and honey',2),
('disease', '1', 'American Foulbrood', 'Paenibacillus larvae', 'Bacterial infection', 'Spores spread through contaminated equipment', 'Discolored larvae',2),
('disease', '1', 'Nosema', 'Nosema apis', 'Microsporidian parasite', 'Infects the gut of bees', 'Dysentery',2),
('pest', '1', 'European Foulbrood', 'Melissococcus plutonius', 'Bacterial infection', 'Affects bee larvae', 'Ropey texture in larvae',2),
('pest', '0', 'Tropilaelaps mite', 'Tropilaelaps spp.', 'Parasitic mites', 'Attacks brood cells and adults', 'Deformed wings, reduced lifespan of bees',2),
('pest', '0', 'Asian Hornet', 'Vespa velutina', 'Large hornet species', 'Preys on honeybees', 'Attack honeybee hives',2),
('disease', '0', 'Chalkbrood', 'Ascosphaera apis', 'Fungal infection', 'Affects bee larvae', 'White mummified larvae',2),
('pest', '0', 'Wax Moth', 'Galleria mellonella', 'Moth larvae', 'Destroys comb and honey', 'Webbing and cocoons in hive',2),
('disease', '0', 'Sacbrood Virus', 'Sacbrood virus', 'Viral infection', 'Affects bee larvae', 'Dead larvae with sac-like appearance', 2); 

INSERT INTO images (image_id, pest_id, image_url) VALUES
(1, 1, 'images/varroa-mite.jpg'),
(2, 1, 'images/varroa-mite-1.jpg'),
(3, 8, 'images/chalkbrood.jpg'),
(4, 8, 'images/chalkbrood-1.jpg');