-- Users
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `is_admin` BOOLEAN,
  `is_partner` BOOLEAN,
  `is_approved` BOOLEAN,
  `email` VARCHAR(50) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `password` VARCHAR(30) NOT NULL,
  `register_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- photos
DROP TABLE IF EXISTS `photos`;
CREATE TABLE IF NOT EXISTS `photos` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `main` BOOLEAN,
  `product_id` INTEGER,
  `url` VARCHAR(200) NOT NULL
);

-- Categories
DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(30) NOT NULL
);

-- Store Info
DROP TABLE IF EXISTS `store`;
CREATE TABLE IF NOT EXISTS `store` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) NOT NULL,
  `phone` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `street` VARCHAR(50) NOT NULL,
  `district` VARCHAR(50) NOT NULL,
  `house_number` VARCHAR(30) NOT NULL,
  `city` VARCHAR(30) NOT NULL,
  `state` VARCHAR(30) NOT NULL
);

-- Products
DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `is_active` BOOLEAN,
  `created_by` INTEGER NOT NULL,
  `title` VARCHAR(50) NOT NULL,
  `category` INTEGER NOT NULL,
  `rooms` VARCHAR(50) NOT NULL,
  `bathrooms` VARCHAR(50) NOT NULL,
  `area` VARCHAR(50) NOT NULL,
  `price` VARCHAR(50) NOT NULL,
  `cond_fare` VARCHAR(50) NOT NULL,
  `iptu_fare` VARCHAR(50) NOT NULL,
  `modality` VARCHAR(50) NOT NULL,
  `street` VARCHAR(50) NOT NULL,
  `district` VARCHAR(50) NOT NULL,
  `city` VARCHAR(30) NOT NULL,
  `state` VARCHAR(30) NOT NULL,
  `description` TEXT NOT NULL
);