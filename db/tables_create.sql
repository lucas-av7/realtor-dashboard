-- Users
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY,
  `is_admin` BOOLEAN,
  `is_partner` BOOLEAN,
  `is_approved` BOOLEAN,
  `email` VARCHAR(100) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `register_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- products
DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `id` INTEGER PRIMARY KEY,
  `category_id` VARCHAR(100) NOT NULL,
  `created_by` INTEGER,
  `description` TEXT NOT NULL,
  `img` INTEGER NOT NULL,
  `register_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `title` VARCHAR(100) NOT NULL
);

-- photos
DROP TABLE IF EXISTS `photos`;
CREATE TABLE IF NOT EXISTS `photos` (
  `id` INTEGER PRIMARY KEY,
  `product_id` INTEGER,
  `register_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `url` VARCHAR(200) NOT NULL
);

-- Categories
DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id` INTEGER PRIMARY KEY,
  `register_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `title` VARCHAR(100) NOT NULL
);