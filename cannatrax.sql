-- phpMyAdmin SQL Dump
-- version 4.0.10deb1ubuntu0.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 21, 2019 at 08:19 PM
-- Server version: 5.5.62-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `cannatrax`
--

-- --------------------------------------------------------

--
-- Table structure for table `cycle`
--

CREATE TABLE IF NOT EXISTS `cycle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `start` date NOT NULL,
  `end` date NOT NULL,
  `location` varchar(255) NOT NULL,
  `light_hours` int(2) NOT NULL,
  `total_yield` int(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- Table structure for table `environment`
--

CREATE TABLE IF NOT EXISTS `environment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `location` enum('indoor','outdoor') NOT NULL,
  `light_hours` int(3) NOT NULL,
  `temperature` int(3) NOT NULL,
  `humidity` int(11) NOT NULL,
  `light_source` varchar(255) NOT NULL,
  `lumens` int(5) NOT NULL,
  `wattage` varchar(255) NOT NULL,
  `grow_area` varchar(64) NOT NULL,
  `containment` varchar(255) NOT NULL,
  `max_plants` int(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `log`
--

CREATE TABLE IF NOT EXISTS `log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plant_ID` int(11) NOT NULL,
  `nutrient_ID` int(11) DEFAULT NULL,
  `environment_ID` int(11) DEFAULT NULL,
  `repellent_ID` int(11) DEFAULT NULL,
  `stage` varchar(64) DEFAULT NULL,
  `water` tinyint(1) DEFAULT NULL,
  `trim` varchar(32) DEFAULT NULL,
  `height` decimal(3,1) DEFAULT NULL,
  `span` decimal(3,1) DEFAULT NULL,
  `lux` int(5) NOT NULL,
  `soil_pH` decimal(2,1) NOT NULL DEFAULT '7.0',
  `transplant` tinyint(1) DEFAULT NULL,
  `photo` blob,
  `notes` text CHARACTER SET utf8,
  `logdate` date DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=183 ;

-- --------------------------------------------------------

--
-- Table structure for table `nutrient`
--

CREATE TABLE IF NOT EXISTS `nutrient` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `organic` varchar(8) NOT NULL,
  `nitrogen` int(2) NOT NULL,
  `phosphorus` int(2) NOT NULL,
  `potassium` int(2) NOT NULL,
  `trace` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- Table structure for table `options`
--

CREATE TABLE IF NOT EXISTS `options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `option_key` varchar(255) CHARACTER SET utf8 NOT NULL,
  `option_value` text CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

-- --------------------------------------------------------

--
-- Table structure for table `plant`
--

CREATE TABLE IF NOT EXISTS `plant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 NOT NULL,
  `gender` varchar(32) NOT NULL,
  `strain_ID` varchar(255) NOT NULL,
  `cycle_ID` varchar(255) NOT NULL,
  `source` varchar(64) NOT NULL,
  `yield` int(3) NOT NULL,
  `current_stage` varchar(255) DEFAULT NULL,
  `current_environment` int(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=22 ;

-- --------------------------------------------------------

--
-- Table structure for table `repellent`
--

CREATE TABLE IF NOT EXISTS `repellent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` enum('organic','chemical','other') NOT NULL,
  `target` varchar(255) NOT NULL,
  `price` varchar(64) NOT NULL,
  `purchase_location` varchar(255) NOT NULL,
  `notes` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- Table structure for table `report`
--

CREATE TABLE IF NOT EXISTS `report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `data` mediumtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `strain`
--

CREATE TABLE IF NOT EXISTS `strain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `notes` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
