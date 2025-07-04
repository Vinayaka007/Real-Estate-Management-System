-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 04, 2025 at 04:31 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `realestate`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(20) NOT NULL,
  `phoneno` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `name`, `address`, `phoneno`) VALUES
(1, 'vinayak', 'jp nahgar', '1234567'),
(2, 'sidharth', 'rr nagar', '1234567'),
(3, 'zubair', 'mejestic', '1234567'),
(4, 'raju', 'whitefield', '1234567'),
(5, 'jeeva', 'kerala', '1234567');

-- --------------------------------------------------------

--
-- Table structure for table `buyer`
--

CREATE TABLE `buyer` (
  `id` int(11) NOT NULL,
  `srfid` varchar(20) NOT NULL,
  `pcode` varchar(20) NOT NULL,
  `plocation` varchar(100) NOT NULL,
  `ptype` varchar(50) NOT NULL,
  `pbedroom` int(11) NOT NULL,
  `bname` varchar(50) NOT NULL,
  `bphno` varchar(12) NOT NULL,
  `baddress` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `buyer`
--

INSERT INTO `buyer` (`id`, `srfid`, `pcode`, `plocation`, `ptype`, `pbedroom`, `bname`, `bphno`, `baddress`) VALUES
(121, '2234', 'f1234', 'bhatkal', 'lease', 6, 'kartik', '963258458', 'honnavar'),
(256, '234', 'd1234', 'mangalore', 'buy', 1, 'ravi', '932584544', 'udupi'),
(1234, '224', 'a1234', 'kerala', 'buy', 6, 'manju', '9632584544', 'gokarna'),
(2356, '2234', 'g1234', 'mangalore', 'buy', 6, 'kartik', '9632584544', 'honnavar'),
(3708, '447', 'g1234', 'honnavar', 'Rent', 5, 'ajay', '1211212112', 'marath halli');

-- --------------------------------------------------------

--
-- Table structure for table `propertydata`
--

CREATE TABLE `propertydata` (
  `id` int(11) NOT NULL,
  `pcode` varchar(100) NOT NULL,
  `plocation` varchar(100) NOT NULL,
  `bedroom` int(11) NOT NULL,
  `ptype` varchar(100) NOT NULL,
  `dimension` varchar(100) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `propertydata`
--

INSERT INTO `propertydata` (`id`, `pcode`, `plocation`, `bedroom`, `ptype`, `dimension`, `price`) VALUES
(121, 'f1234', 'asdaf', 2, 'sdfsda', '5454s4d', 1),
(2122, 'a1234', 'banagalore', 12, 'Sell', '1*1feet', 3),
(2197, 'd1234', 'bhatkal', 6, 'Sell', '60*65feet', 65000),
(2497, 'g1234', 'dfgdgfh', 3, 'Lease', '3*-2feet', 21212222);

--
-- Triggers `propertydata`
--
DELIMITER $$
CREATE TRIGGER `history` AFTER INSERT ON `propertydata` FOR EACH ROW BEGIN
    INSERT INTO property_history (property_id, pcode, plocation, ptype, bedroom, dimension, price, timestamp)
    VALUES (NEW.id, NEW.pcode, NEW.plocation, NEW.ptype, NEW.bedroom, NEW.dimension, NEW.price, CURRENT_TIMESTAMP);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `propertyuser`
--

CREATE TABLE `propertyuser` (
  `id` int(11) NOT NULL,
  `pcode` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `propertyuser`
--

INSERT INTO `propertyuser` (`id`, `pcode`, `password`, `email`) VALUES
(814, 'a1234', '1234', 'a@gmail.com'),
(927, 's1234', '1234', 's@gmail.com'),
(1700, 'f1234', '1234', 'f@gmail.com'),
(1931, 'd1234', '1234', 'd@gmail.com'),
(1957, 'g1234', '1234', 'g@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `property_history`
--

CREATE TABLE `property_history` (
  `id` int(11) NOT NULL,
  `property_id` int(11) NOT NULL,
  `pcode` varchar(100) NOT NULL,
  `plocation` varchar(100) NOT NULL,
  `ptype` varchar(100) NOT NULL,
  `bedroom` int(11) NOT NULL,
  `dimension` varchar(100) NOT NULL,
  `price` int(11) NOT NULL,
  `timestamp` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `property_history`
--

INSERT INTO `property_history` (`id`, `property_id`, `pcode`, `plocation`, `ptype`, `bedroom`, `dimension`, `price`, `timestamp`) VALUES
(646464649, 2943, 's1234', 'vinahaha', 'Lease', 5, '3*2feet', 1, '2024-02-29 14:02:19');

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `srfid` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `dob` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `srfid`, `email`, `dob`) VALUES
(18, 'o1', 'gg@gmail.com', '30/05/2000'),
(33, '449', 'e@gmail.com', '2000-05-30'),
(103, '447', 'q@gmail.com', '2000-05-30'),
(112, '121', 't@gmail.com', '2000-05-30'),
(290, '448', 'w@gmail.com', '2000-05-30'),
(726, '444', 'r@gmail.com', '2000-05-30'),
(112112, 'jbbbb', 'dh@gmail.com', '212121');

-- --------------------------------------------------------

--
-- Stand-in structure for view `views`
-- (See below for the actual view)
--
CREATE TABLE `views` (
`id` int(11)
,`pcode` varchar(100)
,`plocation` varchar(100)
);

-- --------------------------------------------------------

--
-- Structure for view `views`
--
DROP TABLE IF EXISTS `views`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `views`  AS SELECT `propertydata`.`id` AS `id`, `propertydata`.`pcode` AS `pcode`, `propertydata`.`plocation` AS `plocation` FROM `propertydata` WHERE `propertydata`.`price` > 3 ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `buyer`
--
ALTER TABLE `buyer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `propertydata`
--
ALTER TABLE `propertydata`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`,`pcode`);

--
-- Indexes for table `propertyuser`
--
ALTER TABLE `propertyuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `pcode` (`pcode`);

--
-- Indexes for table `property_history`
--
ALTER TABLE `property_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`srfid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `property_history`
--
ALTER TABLE `property_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=646464650;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
