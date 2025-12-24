CREATE DATABASE IF NOT EXISTS buzznews;
USE buzznews;

-- Roles
CREATE TABLE IF NOT EXISTS roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);
INSERT IGNORE INTO roles (id, name) VALUES
(1, 'admin'),
(2, 'moderator'),
(3, 'journalist'),
(4, 'reader');

-- Districts
CREATE TABLE IF NOT EXISTS districts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);
INSERT IGNORE INTO districts (name) VALUES
('Ahmedabad'), ('Amreli'), ('Anand'), ('Aravalli'), ('Banaskantha'),
('Bharuch'), ('Bhavnagar'), ('Botad'), ('Chhota Udaipur'), ('Dahod'),
('Dang'), ('Devbhumi Dwarka'), ('Gandhinagar'), ('Gir Somnath'),
('Jamnagar'), ('Junagadh'), ('Kheda'), ('Kutch'), ('Mahisagar'),
('Mehsana'), ('Morbi'), ('Narmada'), ('Navsari'), ('Panchmahal'),
('Patan'), ('Porbandar'), ('Rajkot'), ('Sabarkantha'), ('Surat'),
('Surendranagar'), ('Tapi'), ('Vadodara'), ('Valsad');

-- Users
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role_id INT NULL,
    bio TEXT,
    profile_image VARCHAR(255),
    district_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL,
    FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE SET NULL
);
-- Insert admin user
INSERT IGNORE INTO users (username, password, role_id, district_id)
VALUES ('admin', 'admin_123', 1, 15);

-- Categories 
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);
INSERT IGNORE INTO categories (name, description) VALUES
('Politics', 'Political news and analysis'),
('Sports', 'Sports updates and events'),
('Business', 'Business and finance news'),
('Technology', 'Tech and innovation news'),
('Entertainment', 'Movies, TV, and celebrity news'),
('Lifestyle', 'Fashion, travel, food, culture'),
('Environment','News on climate, wildlife and environmental issues'),
('Perspective','Personal view points, blogs and Analysis'),
('Education', 'Articles related to literacy and educational initiatives in Gujarat.'),
('Agriculture', 'Topics covering farming, government schemes, and rural farming communities.'),
('Economy', 'Articles focusing on state and local economic developments, business, and financial news.'),
('Trade', 'News related to local markets, commerce, exports, imports, and trade policies.');

-- Articles
CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    author_id INT NOT NULL,
    category_id INT,
    district_id INT NULL,
    second_district_id INT NULL,
    status ENUM('draft','pending','approved','rejected') DEFAULT 'pending',
    rejection_reason VARCHAR(255) DEFAULT NULL,
    is_local_voice BOOLEAN DEFAULT FALSE,
    submit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE SET NULL
);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    article_id INT NULL,
    notif_type VARCHAR(50),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);