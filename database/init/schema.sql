CREATE DATABASE IF NOT EXISTS devops_dashboard;

USE devops_dashboard;

CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    environment VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL
);

INSERT INTO applications (
    name,
    version,
    environment,
    status
) VALUES (
    'devops-dashboard',
    '1.0.0',
    'development',
    'ok'
);
