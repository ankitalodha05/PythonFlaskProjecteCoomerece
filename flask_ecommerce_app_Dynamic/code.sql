CREATE DATABASE my_product;
USE my_product;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(255)
);


INSERT INTO products (name, description, price, image_url)
VALUES (
    'Example Product',
    'This is a sample description for the example product.',
    49.99,
    'https://img.autocarindia.com/Features/Hycross%20feature.jpg?w=700&c=1'
);
