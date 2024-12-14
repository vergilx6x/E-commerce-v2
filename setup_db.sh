-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS web_db;
CREATE USER IF NOT EXISTS 'web_admin'@'localhost' IDENTIFIED BY 'Testpassword6.';
GRANT ALL PRIVILEGES ON `web_db`.* TO 'web_admin'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'web_admin'@'localhost';
FLUSH PRIVILEGES;