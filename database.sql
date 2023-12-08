-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 08, 2023 at 08:18 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `eis_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `acc_id` int(11) NOT NULL,
  `username` varchar(32) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL DEFAULT 0,
  `last_login` datetime(6) DEFAULT NULL,
  `acc_is_active` tinyint(1) NOT NULL,
  `acc_created_at` datetime(6) NOT NULL DEFAULT current_timestamp(6),
  `acc_updated_at` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `acc_type_id` int(11) DEFAULT NULL,
  `emp_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `account_type`
--

CREATE TABLE `account_type` (
  `acc_type_id` int(11) NOT NULL,
  `acc_type_name` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `account_type`
--

INSERT INTO `account_type` (`acc_type_id`, `acc_type_name`) VALUES
(1, 'Super Administrator'),
(2, 'Administrator'),
(3, 'Employee');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `cus_id` int(11) NOT NULL,
  `cus_fname` varchar(1024) NOT NULL,
  `cus_mname` varchar(1024) DEFAULT NULL,
  `cus_lname` varchar(1024) NOT NULL,
  `cus_phone` varchar(12) NOT NULL,
  `cus_created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `cus_updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `emp_id` int(11) NOT NULL,
  `emp_fname` varchar(1024) NOT NULL,
  `emp_mname` varchar(1024) DEFAULT NULL,
  `emp_lname` varchar(1024) NOT NULL,
  `emp_birthdate` date DEFAULT NULL,
  `emp_phone` varchar(12) DEFAULT NULL,
  `emp_email` varchar(1024) DEFAULT NULL,
  `emp_address` varchar(1024) DEFAULT NULL,
  `emp_created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `emp_updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `in_id` int(11) NOT NULL,
  `in_qty` int(11) DEFAULT NULL,
  `in_status` varchar(13) DEFAULT NULL,
  `in_created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `in_updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `prod_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `invoice`
--

CREATE TABLE `invoice` (
  `inv_id` int(11) NOT NULL,
  `inv_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `inv_amount` double DEFAULT NULL,
  `cus_id` int(11) DEFAULT NULL,
  `emp_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `order_list`
--

CREATE TABLE `order_list` (
  `ord_id` int(11) NOT NULL,
  `ord_price` double DEFAULT NULL,
  `ord_qty` int(11) DEFAULT NULL,
  `inv_id` int(11) NOT NULL,
  `prod_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `prod_id` int(11) NOT NULL,
  `prod_name` varchar(1024) NOT NULL,
  `prod_desc` varchar(1024) DEFAULT NULL,
  `prod_price` double DEFAULT NULL,
  `prod_status` varchar(32) NOT NULL,
  `prod_created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `prod_updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `prod_type_id` int(11) NOT NULL,
  `prod_br_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `product_brand`
--

CREATE TABLE `product_brand` (
  `prod_br_id` int(11) NOT NULL,
  `prod_br_name` varchar(1024) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product_brand`
--

INSERT INTO `product_brand` (`prod_br_id`, `prod_br_name`) VALUES
(1, 'Epson');

-- --------------------------------------------------------

--
-- Table structure for table `product_type`
--

CREATE TABLE `product_type` (
  `prod_type_id` int(11) NOT NULL,
  `prod_type_name` varchar(1024) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product_type`
--

INSERT INTO `product_type` (`prod_type_id`, `prod_type_name`) VALUES
(1, 'Projector');

-- --------------------------------------------------------

--
-- Table structure for table `supplier`
--

CREATE TABLE `supplier` (
  `sup_id` int(11) NOT NULL,
  `sup_name` varchar(1024) NOT NULL,
  `sup_phone` varchar(12) NOT NULL,
  `sup_email` varchar(1024) NOT NULL,
  `sup_created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `sup_updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `sup_status` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `supplier_item`
--

CREATE TABLE `supplier_item` (
  `sup_itm_id` int(11) NOT NULL,
  `sup_itm_qty` int(11) DEFAULT NULL,
  `sup_itm_dr` varchar(1024) NOT NULL,
  `sup_itm_status` varchar(9) DEFAULT NULL,
  `sup_itm_created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `sup_itm_updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `prod_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`acc_id`),
  ADD UNIQUE KEY `acc_username` (`username`) USING BTREE,
  ADD UNIQUE KEY `account_emp_id_b8b807d9_uniq` (`emp_id`),
  ADD KEY `account_acc_type_id_e07fe73a_fk` (`acc_type_id`);

--
-- Indexes for table `account_type`
--
ALTER TABLE `account_type`
  ADD PRIMARY KEY (`acc_type_id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`cus_id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`emp_id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`in_id`),
  ADD UNIQUE KEY `inventory_prod_id_7e0b888a_uniq` (`prod_id`);

--
-- Indexes for table `invoice`
--
ALTER TABLE `invoice`
  ADD PRIMARY KEY (`inv_id`),
  ADD KEY `invoice_cus_id_b682f190_fk_customer_cus_id` (`cus_id`),
  ADD KEY `invoice_emp_id_f1bc3265_fk_employee_emp_id` (`emp_id`);

--
-- Indexes for table `order_list`
--
ALTER TABLE `order_list`
  ADD PRIMARY KEY (`ord_id`),
  ADD KEY `order_list_inv_id_5583eef3_fk_invoice_inv_id` (`inv_id`),
  ADD KEY `order_list_prod_id_4c198035_fk_product_prod_id` (`prod_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`prod_id`),
  ADD KEY `product_prod_br_id_c48274be_fk` (`prod_br_id`),
  ADD KEY `product_prod_type_id_a7d022e2_fk` (`prod_type_id`);

--
-- Indexes for table `product_brand`
--
ALTER TABLE `product_brand`
  ADD PRIMARY KEY (`prod_br_id`);

--
-- Indexes for table `product_type`
--
ALTER TABLE `product_type`
  ADD PRIMARY KEY (`prod_type_id`);

--
-- Indexes for table `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`sup_id`);

--
-- Indexes for table `supplier_item`
--
ALTER TABLE `supplier_item`
  ADD PRIMARY KEY (`sup_itm_id`),
  ADD KEY `supplier_item_prod_id_b2c6d16d_fk_product_prod_id` (`prod_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `acc_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_type`
--
ALTER TABLE `account_type`
  MODIFY `acc_type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `cus_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `emp_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `in_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `invoice`
--
ALTER TABLE `invoice`
  MODIFY `inv_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `order_list`
--
ALTER TABLE `order_list`
  MODIFY `ord_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `prod_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product_brand`
--
ALTER TABLE `product_brand`
  MODIFY `prod_br_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `product_type`
--
ALTER TABLE `product_type`
  MODIFY `prod_type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `supplier`
--
ALTER TABLE `supplier`
  MODIFY `sup_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `supplier_item`
--
ALTER TABLE `supplier_item`
  MODIFY `sup_itm_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account`
--
ALTER TABLE `account`
  ADD CONSTRAINT `account_acc_type_id_e07fe73a_fk` FOREIGN KEY (`acc_type_id`) REFERENCES `account_type` (`acc_type_id`);

--
-- Constraints for table `inventory`
--
ALTER TABLE `inventory`
  ADD CONSTRAINT `inventory_prod_id_7e0b888a_fk_product_prod_id` FOREIGN KEY (`prod_id`) REFERENCES `product` (`prod_id`);

--
-- Constraints for table `invoice`
--
ALTER TABLE `invoice`
  ADD CONSTRAINT `invoice_cus_id_b682f190_fk_customer_cus_id` FOREIGN KEY (`cus_id`) REFERENCES `customer` (`cus_id`),
  ADD CONSTRAINT `invoice_emp_id_f1bc3265_fk_employee_emp_id` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`);

--
-- Constraints for table `order_list`
--
ALTER TABLE `order_list`
  ADD CONSTRAINT `order_list_inv_id_5583eef3_fk_invoice_inv_id` FOREIGN KEY (`inv_id`) REFERENCES `invoice` (`inv_id`),
  ADD CONSTRAINT `order_list_prod_id_4c198035_fk_product_prod_id` FOREIGN KEY (`prod_id`) REFERENCES `product` (`prod_id`);

--
-- Constraints for table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `product_prod_br_id_c48274be_fk` FOREIGN KEY (`prod_br_id`) REFERENCES `product_brand` (`prod_br_id`),
  ADD CONSTRAINT `product_prod_type_id_a7d022e2_fk` FOREIGN KEY (`prod_type_id`) REFERENCES `product_type` (`prod_type_id`);

--
-- Constraints for table `supplier_item`
--
ALTER TABLE `supplier_item`
  ADD CONSTRAINT `supplier_item_prod_id_b2c6d16d_fk_product_prod_id` FOREIGN KEY (`prod_id`) REFERENCES `product` (`prod_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
