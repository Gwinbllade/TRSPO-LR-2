-- Вставка користувачів
INSERT INTO users (username, email,hashed_password, role)
VALUES
    ('john_doe', 'john@example.com', '123', 'BUYER'),
    ('jane_smith', 'jane@example.com', '123','BUYER'),
    ('admin', 'admin@example.com', '123','ADMIN');

-- Вставка категорій
INSERT INTO categories (name)
VALUES
    ('Electronics'),
    ('Clothing'),
    ('Books');

-- Вставка продуктів
INSERT INTO products (name, cost, category_id)
VALUES
    ('Laptop', 999.99, 1),
    ('Smartphone', 499.99, 1),
    ('T-Shirt', 19.99, 2),
    ('Jeans', 59.99, 2),
    ('Novel', 12.99, 3),
    ('Textbook', 39.99, 3);

-- Вставка замовлень
INSERT INTO orders (user_id, date, status, product_id)
VALUES
    (1, '2023-05-01', 'PROCESSING', 2),
    (2, '2023-05-02', 'SHIPPED',3),
    (3, '2023-05-03', 'DELIVERED',1);

