-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 05, 2024 at 06:47 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `crop`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `fert_data`
--

CREATE TABLE `fert_data` (
  `id` int(11) NOT NULL,
  `crop` varchar(30) NOT NULL,
  `fert` varchar(200) NOT NULL,
  `pest` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fert_data`
--

INSERT INTO `fert_data` (`id`, `crop`, `fert`, `pest`) VALUES
(1, 'rice', 'Cottonseed Meal, Banana Skin Ash, Poultry Litter (Dried)', 'Insecticides, Fungicides, Herbicides'),
(2, 'maize', 'Fish, Blood & Bone meal, Activated Sewage Sludge', 'Egao (Emamectin Benzoate 5 SG) - 250 gm, Taiyo Plus (Thiamethoxam 30% FS)- 500 ml'),
(3, 'chickpea', 'Katyayani Chickpea Crop Super Combo Pack', 'Emamectin benzoate 05.00% SG, Chickpea, Pod borer');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` int(11) NOT NULL,
  `reg_date` varchar(20) NOT NULL,
  `question` varchar(100) NOT NULL,
  `username` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `reg_date`, `question`, `username`) VALUES
(1, '2024-05-05', 'I have used what frticide for rice crop', 'san');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `mobile`, `email`, `uname`, `pass`) VALUES
(1, 'Ram', 9638527415, 'ram@gmail.com', 'ram', '1234'),
(2, 'santhosh', 7854236658, 'san@gmail.com', 'san', '1234'),
(3, 'Raj', 8956232154, 'raj@gmail.com', 'raj01', '1234'),
(4, 'Raj', 6985221555, 'raj@gmail.com', 'raj', '1234'),
(5, 'Suresh', 9874562255, 'suresh@gmail.com', 'suresh', '123456');

-- --------------------------------------------------------

--
-- Table structure for table `suggestion`
--

CREATE TABLE `suggestion` (
  `id` int(11) NOT NULL,
  `qid` int(11) NOT NULL,
  `reg_date` varchar(20) NOT NULL,
  `sugges` varchar(100) NOT NULL,
  `username` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `suggestion`
--

