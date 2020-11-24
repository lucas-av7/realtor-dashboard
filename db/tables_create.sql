SET GLOBAL time_zone = '-3:00';

-- Users
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `is_admin` BOOLEAN,
  `is_approved` BOOLEAN,
  `role` INTEGER NOT NULL,
  `phone` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `password` VARCHAR(225) NOT NULL,
  `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `created_at` TIMESTAMP NOT NULL
);

-- Roles/Permissions
DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(30) NOT NULL,
  `activate` BOOLEAN,
  `all_products` BOOLEAN,
  `categories` BOOLEAN,
  `purposes` BOOLEAN,
  `users` BOOLEAN,
  `store` BOOLEAN
);
INSERT INTO `roles`(title, activate, all_products, categories, purposes, users, store) VALUES ('Cliente', False, False, False, False, False, False);
INSERT INTO `roles`(title, activate, all_products, categories, purposes, users, store) VALUES ('Corretor', False, False, False, False, False, False);
INSERT INTO `roles`(title, activate, all_products, categories, purposes, users, store) VALUES ('Corretor parceiro', True, False, False, False, False, False);

-- photos
DROP TABLE IF EXISTS `images`;
CREATE TABLE IF NOT EXISTS `images` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `main` BOOLEAN,
  `product_id` INTEGER,
  `url` VARCHAR(200) NOT NULL,
  `url_thumb` VARCHAR(200) NOT NULL,
  `url_medium` VARCHAR(200) NOT NULL,
  `delete_url` VARCHAR(200) NOT NULL
);

-- Categories
DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(30) NOT NULL
);
INSERT INTO `categories`(title) VALUES ('Sem categoria');

-- Purposes
DROP TABLE IF EXISTS `purposes`;
CREATE TABLE IF NOT EXISTS `purposes` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(30) NOT NULL
);
INSERT INTO `purposes`(title) VALUES ('Sem propósito');

-- Store Info
DROP TABLE IF EXISTS `store`;
CREATE TABLE IF NOT EXISTS `store` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50),
  `phone` VARCHAR(50),
  `email` VARCHAR(50),
  `street` VARCHAR(50),
  `district` VARCHAR(50),
  `house_number` VARCHAR(30),
  `city` VARCHAR(30),
  `state` VARCHAR(30),
  `auto_active_user` BOOLEAN
);
INSERT INTO store(auto_active_user) VALUES(TRUE)

-- Products
DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
  `is_active` BOOLEAN,
  `created_by` INTEGER NOT NULL,
  `title` VARCHAR(50) NOT NULL,
  `category` INTEGER NOT NULL,
  `purpose` INTEGER NOT NULL,
  `rooms` VARCHAR(50) NOT NULL,
  `bathrooms` VARCHAR(50) NOT NULL,
  `parking_spaces` VARCHAR(50) NOT NULL,
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