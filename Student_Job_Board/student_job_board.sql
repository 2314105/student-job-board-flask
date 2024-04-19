-- Create Database
CREATE DATABASE IF NOT EXISTS `student_job_board`;

-- Use the Database
USE `student_job_board`;

-- Create Tables
CREATE TABLE IF NOT EXISTS `employer` (
  `employer_id` INT AUTO_INCREMENT PRIMARY KEY,
  `company` VARCHAR(50) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `profile_picture` VARCHAR(255),
  `description` TEXT,
  `website` TEXT
);

CREATE TABLE IF NOT EXISTS `employer_job` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT NOT NULL,
  `requirements` TEXT NOT NULL,
  `job_type` VARCHAR(50) NOT NULL,
  `deadline_day` INT NOT NULL,
  `deadline_month` INT NOT NULL,
  `deadline_year` INT NOT NULL,
  `location` VARCHAR(255) NOT NULL,
  `salary` VARCHAR(100),
  `employer_id` INT,
  FOREIGN KEY (`employer_id`) REFERENCES `employer`(`employer_id`)
);

CREATE TABLE IF NOT EXISTS `employers_address` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `address_line_1` VARCHAR(255) NOT NULL,
  `address_line_2` VARCHAR(255),
  `postal_code_1` VARCHAR(20) NOT NULL,
  `postal_code_2` VARCHAR(20),
  `employer_id` INT,
  FOREIGN KEY (`employer_id`) REFERENCES `employer`(`employer_id`)
);

CREATE TABLE IF NOT EXISTS `employers_contact` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `phone_number_1` VARCHAR(20),
  `phone_number_2` VARCHAR(20),
  `email_1` VARCHAR(120),
  `email_2` VARCHAR(120),
  `employer_id` INT,
  FOREIGN KEY (`employer_id`) REFERENCES `employer`(`employer_id`)
);

CREATE TABLE IF NOT EXISTS `job_skills` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `skill_name` VARCHAR(100) NOT NULL,
  `employer_job_id` INT,
  FOREIGN KEY (`employer_job_id`) REFERENCES `jobs`(`id`)
);

CREATE TABLE IF NOT EXISTS `student` (
  `student_id` INT AUTO_INCREMENT PRIMARY KEY,
  `forename` VARCHAR(50) NOT NULL,
  `surname` VARCHAR(50) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `date_of_birth` DATE NOT NULL,
  `gender` ENUM('Male','Female','Other') NOT NULL,
  `nationality` VARCHAR(50),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `profile_picture` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS `student_address` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `address_line_1` VARCHAR(255) NOT NULL,
  `address_line_2` VARCHAR(255),
  `postal_code_1` VARCHAR(20) NOT NULL,
  `postal_code_2` VARCHAR(20),
  `student_id` INT,
  FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`)
);

CREATE TABLE IF NOT EXISTS `student_contact` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `phone_number_1` VARCHAR(20),
  `phone_number_2` VARCHAR(20),
  `email_1` VARCHAR(120),
  `email_2` VARCHAR(120),
  `student_id` INT,
  FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`)
);

CREATE TABLE IF NOT EXISTS `student_education` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `institution` VARCHAR(255),
  `field_of_study` VARCHAR(255),
  `degree` VARCHAR(50),
  `years_attended` INT,
  `student_id` INT,
  FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`)
);

CREATE TABLE IF NOT EXISTS `student_key_skills` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `skill_name` VARCHAR(100),
  `student_id` INT,
  FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`)
);

CREATE TABLE IF NOT EXISTS `student_work_experience` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `company` VARCHAR(255),
  `position` VARCHAR(255),
  `duration_year` INT,
  `duration_month` INT,
  `responsibility` TEXT,
  `student_id` INT,
  FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`)
);

