-- PostgreSQL initialization script for Trino lab
-- This creates sample tables for federated queries

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    shipping_address TEXT,
    payment_method VARCHAR(50)
);

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_tier VARCHAR(20) DEFAULT 'bronze',
    total_orders INTEGER DEFAULT 0,
    total_spent DECIMAL(10,2) DEFAULT 0.00
);

-- Insert sample data
INSERT INTO customers (customer_id, name, email, phone, customer_tier, total_orders, total_spent) VALUES
('cust_001', 'Alice Johnson', 'alice.johnson@email.com', '+84-123-456-789', 'gold', 15, 2500000.00),
('cust_002', 'Bob Smith', 'bob.smith@email.com', '+84-987-654-321', 'silver', 8, 1200000.00),
('cust_003', 'Carol Davis', 'carol.davis@email.com', '+84-555-123-456', 'bronze', 3, 450000.00),
('cust_004', 'David Wilson', 'david.wilson@email.com', '+84-777-888-999', 'gold', 22, 3800000.00),
('cust_005', 'Eva Brown', 'eva.brown@email.com', '+84-111-222-333', 'silver', 12, 1800000.00)
ON CONFLICT (customer_id) DO NOTHING;

INSERT INTO orders (order_id, user_id, product_id, quantity, unit_price, total_amount, order_date, status, shipping_address, payment_method) VALUES
('order_001', 'cust_001', 'prod_001', 2, 15000000.00, 30000000.00, '2025-09-15 10:30:00', 'completed', '123 Main St, Ho Chi Minh City', 'credit_card'),
('order_002', 'cust_002', 'prod_002', 1, 22000000.00, 22000000.00, '2025-09-16 14:20:00', 'completed', '456 Oak Ave, Hanoi', 'paypal'),
('order_003', 'cust_001', 'prod_003', 3, 5000000.00, 15000000.00, '2025-09-17 09:15:00', 'shipped', '123 Main St, Ho Chi Minh City', 'credit_card'),
('order_004', 'cust_003', 'prod_001', 1, 15000000.00, 15000000.00, '2025-09-18 16:45:00', 'pending', '789 Pine St, Da Nang', 'bank_transfer'),
('order_005', 'cust_004', 'prod_002', 2, 22000000.00, 44000000.00, '2025-09-19 11:30:00', 'completed', '321 Elm St, Ho Chi Minh City', 'credit_card'),
('order_006', 'cust_005', 'prod_003', 1, 5000000.00, 5000000.00, '2025-09-20 13:20:00', 'completed', '654 Maple Ave, Hanoi', 'paypal'),
('order_007', 'cust_002', 'prod_001', 1, 15000000.00, 15000000.00, '2025-09-21 08:10:00', 'shipped', '456 Oak Ave, Hanoi', 'credit_card')
ON CONFLICT (order_id) DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_product_id ON orders(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

-- Create a view for order summary
CREATE OR REPLACE VIEW order_summary AS
SELECT 
    o.order_id,
    c.name as customer_name,
    c.email as customer_email,
    c.customer_tier,
    o.product_id,
    o.quantity,
    o.total_amount,
    o.order_date,
    o.status,
    o.payment_method
FROM orders o
JOIN customers c ON o.user_id = c.customer_id;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO user;
GRANT USAGE ON SCHEMA public TO user;
