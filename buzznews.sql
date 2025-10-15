-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 14, 2025 at 08:28 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `buzznews`
--

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `author_id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `district_id` int(11) DEFAULT NULL,
  `second_district_id` int(11) DEFAULT NULL,
  `status` enum('pending','approved','rejected','draft') DEFAULT 'pending',
  `rejection_reason` text DEFAULT NULL,
  `is_local_voice` tinyint(1) DEFAULT 0,
  `submit_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id`, `title`, `content`, `image_url`, `author_id`, `category_id`, `district_id`, `second_district_id`, `status`, `rejection_reason`, `is_local_voice`, `submit_time`) VALUES
(5, 'demo', 'demo', NULL, 5, 2, 15, NULL, 'rejected', 'irrelevant content', 1, '2025-10-11 07:39:18'),
(7, 'Reflection: how villages of Gujarat taught me the value of Community', '<p data-start=\"4124\" data-end=\"4440\">Last winter, I spent two weeks volunteering in remote villages of North Gujarat, helping set up reading corners for children.&nbsp;</p><p data-start=\"4124\" data-end=\"4440\">What struck me most wasn’t the lack of infrastructure — it was the overwhelming sense of community. Families supported each other selflessly,&nbsp;</p><p data-start=\"4124\" data-end=\"4440\">sharing resources and time without hesitation.</p>\r\n<p data-start=\"4442\" data-end=\"4743\">In urban spaces, we often get caught in the cycle of individual goals and competition. But here, I witnessed how collective progress can uplift everyone.&nbsp;</p><p data-start=\"4442\" data-end=\"4743\">These villages reminded me that development isn’t just about concrete structures — it’s about nurturing the human bond that holds society together.</p>', 'village.jpeg', 9, 8, NULL, NULL, 'approved', NULL, 1, '2025-10-12 17:17:42'),
(8, 'Gir National Park reports record Lion Population in 2025', 'T<span style=\"font-size: 1rem;\">he 2025 lion census in Gir National Park has revealed a record population of 760 Asiatic lions,&nbsp;</span><div><span style=\"font-size: 1rem;\">reflecting successful conservation measures. Wildlife experts credit improved habitat corridors, community participation,&nbsp;</span></div><div><span style=\"font-size: 1rem;\">and stricter anti-poaching surveillance for the remarkable growth.</span></div><div><br><p data-start=\"3695\" data-end=\"3974\">The forest department is also planning to develop buffer eco-tourism zones to reduce human-animal conflict while providing&nbsp;</p><p data-start=\"3695\" data-end=\"3974\">livelihood opportunities for nearby villages.&nbsp;</p><p data-start=\"3695\" data-end=\"3974\">International conservation groups have lauded Gujarat’s long-term commitment to protecting its iconic species.</p></div>', 'lion.jpg', 1, 7, 14, NULL, 'draft', NULL, 0, '2025-10-12 18:12:36'),
(9, 'The Future of Education Lies Beyond Classrooms', '<p data-start=\"4881\" data-end=\"5196\">As someone who grew up in a small town in Gujarat and later moved to a metropolitan city for higher education,&nbsp;</p><p data-start=\"4881\" data-end=\"5196\">I’ve seen the stark contrast between rote learning and experiential education. Classrooms often limit students to textbooks,&nbsp;</p><p data-start=\"4881\" data-end=\"5196\">but true learning happens when they apply knowledge to real-world challenges.</p><p data-start=\"4881\" data-end=\"5196\"><br></p>\r\n<p data-start=\"5198\" data-end=\"5448\">With the rise of digital tools, local innovation hubs, and community-driven projects, Gujarat has the potential to&nbsp;</p><p data-start=\"5198\" data-end=\"5448\">redefine education. We must move towards encouraging curiosity, critical thinking, and collaboration rather than mere exam preparation.</p>', NULL, 1, 249, NULL, NULL, 'approved', NULL, 0, '2025-10-12 18:22:15'),
(10, 'GIFT City Attracts Global Startups with Special Regulatory Sandbox', '<p data-start=\"6932\" data-end=\"7212\">Gujarat International Finance Tec-City (GIFT City) has introduced a regulatory sandbox to attract fintech&nbsp;</p><p data-start=\"6932\" data-end=\"7212\">and blockchain startups from around the world.&nbsp;</p><p data-start=\"6932\" data-end=\"7212\">The sandbox allows startups to test products under relaxed regulations&nbsp;<span style=\"font-size: 1rem;\">before full-scale launch, reducing compliance burdens.</span></p><p data-start=\"6932\" data-end=\"7212\"><span style=\"font-size: 1rem;\"><br></span></p>\r\n<p data-start=\"7214\" data-end=\"7441\">Over 40 international companies have already shown interest. Experts believe this initiative could make Gujarat a leading innovation hub,&nbsp;</p><p data-start=\"7214\" data-end=\"7441\">generating high-skill jobs and boosting India’s position in the global fintech landscape.</p>', 'gift.jpeg', 6, 4, 13, NULL, 'approved', NULL, 0, '2025-10-12 18:35:30'),
(11, 'Mehsana-Patan Highway Sees Major Upgrade to Improve Connectivity', '<p data-start=\"2110\" data-end=\"2401\">The state government has approved a major expansion of the <b>Mehsana-Patan highway</b> to reduce&nbsp;</p><p data-start=\"2110\" data-end=\"2401\">congestion and improve connectivity between the two districts.&nbsp;</p><p data-start=\"2110\" data-end=\"2401\">The project includes widening the existing lanes, constructing flyovers at key intersections, and adding dedicated pedestrian pathways.</p><p data-start=\"2110\" data-end=\"2401\"><br></p><p data-start=\"2110\" data-end=\"2401\"><br></p>\r\n<p data-start=\"2403\" data-end=\"2696\">Local traders and commuters have welcomed the development, expecting it to cut travel time significantly and facilitate smoother transport of goods.&nbsp;</p><p data-start=\"2403\" data-end=\"2696\">Authorities stated that construction would be completed in phases over the next 18 months, with efforts to minimize disruption to daily traffic.</p>', 'highway.jpg', 11, 55, 25, 20, 'pending', NULL, 1, '2025-10-12 19:17:12'),
(12, 'Gujarat Govt Announces New Solar Power Scheme for Rural Households', 'The Gujarat government has announced a new solar power scheme aimed at rural households to boost sustainable&nbsp;<span style=\"font-size: 1rem;\">energy adoption and&nbsp;</span><div><span style=\"font-size: 1rem;\">reduce dependency on traditional power grids. The initiative will subsidize 40% of the installation cost for rooftop solar panels,&nbsp;</span></div><div><span style=\"font-size: 1rem;\">with an additional 20% support from the central government.</span><br></div><div><span style=\"font-size: 1rem;\"><br></span></div><div><span style=\"font-size: 1rem;\">O</span><span style=\"font-size: 1rem;\">fficials stated that the scheme is expected to benefit over 1.5 lakh rural families in its first phase. In addition to lowering electricity costs, the program aims to create local employment opportunities through installation and maintenance contracts. Training centers will be set up in district headquarters to ensure skilled labor availability.</span></div>', 'solar.jpeg', 10, 4, NULL, NULL, 'draft', NULL, 0, '2025-10-12 19:21:08'),
(13, 'The Art of Slow Living in a Fast-Paced World', '<p data-start=\"258\" data-end=\"606\">In today’s hyper-connected world, it feels like everything moves faster than we can keep up. Emails, notifications, and endless to-do lists leave little room to breathe. The concept of slow living—a lifestyle focused on mindfulness, intentionality, and savoring everyday moments—is gaining traction globally as people seek balance and well-being.</p>\r\n<p data-start=\"608\" data-end=\"977\">Adopting slow living doesn’t require a drastic life change. It can start with simple habits: taking longer walks without your phone, cooking meals from scratch, journaling your thoughts, or dedicating uninterrupted time to hobbies. These small acts help reduce stress, improve focus, and bring a sense of fulfillment that constant productivity often fails to provide.</p>\r\n<p data-start=\"979\" data-end=\"1313\">Interestingly, slow living also encourages deeper connections. By prioritizing meaningful conversations over fleeting interactions and experiences over possessions, we cultivate relationships and memories that truly enrich our lives. In a world obsessed with speed, learning to slow down might just be the ultimate act of self-care.</p>', 'lifestyle.jpg', 10, 6, NULL, NULL, 'pending', NULL, 0, '2025-10-12 19:23:54'),
(14, 'Minimalism Is Not Just About Empty Rooms', '<p data-start=\"1189\" data-end=\"1468\">The internet has made us connected like never before — but it’s also blurred the line between <em data-start=\"1283\" data-end=\"1290\">being</em> and <em data-start=\"1295\" data-end=\"1309\">broadcasting</em>.&nbsp;</p><p data-start=\"1189\" data-end=\"1468\">Every trip, every meal, every thought is shared, liked, and archived. Somewhere along the way, our private lives became performances for invisible audiences.</p><p data-start=\"1189\" data-end=\"1468\"><br></p>\r\n<p data-start=\"1470\" data-end=\"1745\">The question is not whether the internet is good or bad — it’s whether we’re still able to experience moments without the urge to record them.&nbsp;</p><p data-start=\"1470\" data-end=\"1745\">The pressure to “exist publicly” can slowly erode personal joy, making us curators of perception instead of participants in reality.</p>', 'house.jpeg', 12, 6, NULL, NULL, 'pending', NULL, 1, '2025-10-14 06:06:15');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `description`) VALUES
(1, 'Politics', 'Political news and analysis'),
(2, 'Sports', 'Sports updates and events'),
(3, 'Business', 'Business and finance news'),
(4, 'Technology', 'Tech and innovation news'),
(5, 'Entertainment', 'Movies, TV, and celebrity news'),
(6, 'Lifestyle', 'Fashion, travel, food, culture'),
(7, 'Environment', 'News on climate, wildlife and environmental issues'),
(8, 'Perspective', 'Personal view points, blogs and Analysis'),
(55, 'Urban Development ', 'News covering policy changes, major infrastructure projects, and emerging challenges'),
(249, 'Education', 'Articles related to literacy and educational initiatives in Gujarat.'),
(250, 'Agriculture', 'Topics covering farming, government schemes and rural farming communities.'),
(251, 'Economy', 'Articles focusing on state and local economic developments, business, and financial news.'),
(252, 'Trade', 'News related to local markets, commerce, exports, imports, and trade policies.');

-- --------------------------------------------------------

--
-- Table structure for table `districts`
--

CREATE TABLE `districts` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `districts`
--

INSERT INTO `districts` (`id`, `name`) VALUES
(1, 'Ahmedabad'),
(2, 'Amreli'),
(3, 'Anand'),
(4, 'Aravalli'),
(5, 'Banaskantha'),
(6, 'Bharuch'),
(7, 'Bhavnagar'),
(8, 'Botad'),
(9, 'Chhota Udaipur'),
(10, 'Dahod'),
(11, 'Dang'),
(12, 'Devbhumi Dwarka'),
(13, 'Gandhinagar'),
(14, 'Gir Somnath'),
(15, 'Jamnagar'),
(16, 'Junagadh'),
(17, 'Kheda'),
(18, 'Kutch'),
(19, 'Mahisagar'),
(20, 'Mehsana'),
(21, 'Morbi'),
(22, 'Narmada'),
(23, 'Navsari'),
(24, 'Panchmahal'),
(25, 'Patan'),
(26, 'Porbandar'),
(27, 'Rajkot'),
(28, 'Sabarkantha'),
(29, 'Surat'),
(30, 'Surendranagar'),
(31, 'Tapi'),
(32, 'Vadodara'),
(33, 'Valsad');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `article_id` int(11) DEFAULT NULL,
  `notif_type` varchar(50) DEFAULT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `article_id`, `notif_type`, `message`, `created_at`) VALUES
(1, 9, 7, 'approved', '✅ Your article \'Reflection: how villages of Gujarat taught me the value of Community\' has been approved.', '2025-10-12 17:39:59'),
(2, 5, 5, 'rejected', 'Your article \'demo\' was rejected. Reason: irrelevant content', '2025-10-12 17:55:36'),
(3, 6, 10, 'approved', '✅ Your article \'GIFT City Attracts Global Startups with Special Regulatory Sandbox\' has been approved.', '2025-10-12 18:38:58');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`) VALUES
(1, 'admin'),
(3, 'journalist'),
(2, 'moderator'),
(4, 'reader');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  `bio` text DEFAULT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `district_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role_id`, `bio`, `profile_image`, `district_id`, `created_at`, `updated_at`) VALUES
(1, 'admin', 'admin_123', 1, 'None', 'solar.jpeg', 15, '2025-10-11 03:11:40', '2025-10-14 06:15:25'),
(5, 'vaidehi', 'demo', 4, 'None', 'img2.jpeg', 15, '2025-10-11 03:34:17', '2025-10-14 05:58:49'),
(6, 'Journalist1', 'demo123', 3, 'Writing since 2005..', '20250309_181219_-_Copy.jpg', 9, '2025-10-11 03:35:23', '2025-10-12 18:44:49'),
(7, 'Moderator', 'demo123', 2, 'None', 'lifestyle.jpg', 19, '2025-10-11 03:35:43', '2025-10-14 06:12:05'),
(8, 'Anshu', 'demo123', 4, NULL, NULL, 1, '2025-10-11 04:57:23', '2025-10-11 04:57:23'),
(9, 'John Doe', 'johnD13', 4, NULL, NULL, 27, '2025-10-12 12:26:33', '2025-10-12 12:26:33'),
(10, 'David', 'david123', 3, NULL, NULL, 14, '2025-10-12 18:46:57', '2025-10-12 18:46:57'),
(11, 'Liya', 'demo', 3, NULL, NULL, 25, '2025-10-12 18:53:17', '2025-10-12 18:53:17'),
(12, 'nandani02', 'nandani', 4, NULL, NULL, 21, '2025-10-14 06:03:10', '2025-10-14 06:03:10');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `author_id` (`author_id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `district_id` (`district_id`),
  ADD KEY `second_district_id` (`second_district_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `districts`
--
ALTER TABLE `districts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `article_id` (`article_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `role_id` (`role_id`),
  ADD KEY `district_id` (`district_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=302;

--
-- AUTO_INCREMENT for table `districts`
--
ALTER TABLE `districts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1196;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `articles`
--
ALTER TABLE `articles`
  ADD CONSTRAINT `articles_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `articles_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `articles_ibfk_3` FOREIGN KEY (`district_id`) REFERENCES `districts` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `articles_ibfk_4` FOREIGN KEY (`second_district_id`) REFERENCES `districts` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `users_ibfk_2` FOREIGN KEY (`district_id`) REFERENCES `districts` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
