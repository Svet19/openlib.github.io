-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 09, 2016 at 09:40 AM
-- Server version: 5.5.30
-- PHP Version: 5.4.4-14

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `gmlc-modelinfo`
--

-- --------------------------------------------------------

--
-- Table structure for table `ModelInfo`
--

CREATE TABLE IF NOT EXISTS `ModelInfo` (
  `modelID` char(16) COLLATE utf8_bin NOT NULL,
  `modelName` char(64) COLLATE utf8_bin NOT NULL,
  `authorName` char(32) COLLATE utf8_bin NOT NULL,
  `authorOrg` char(16) COLLATE utf8_bin NOT NULL,
  `date` date NOT NULL,
  `version` char(16) COLLATE utf8_bin NOT NULL,
  `accessibility` varchar(256) COLLATE utf8_bin NOT NULL,
  `proprietary` varchar(256) COLLATE utf8_bin NOT NULL,
  `symbol` char(64) COLLATE utf8_bin NOT NULL,
  `accreditation` char(32) COLLATE utf8_bin NOT NULL,
  `type` varchar(1024) COLLATE utf8_bin NOT NULL,
  `background` varchar(1024) COLLATE utf8_bin NOT NULL,
  `specifications` varchar(512) COLLATE utf8_bin NOT NULL,
  `dependencies` varchar(512) COLLATE utf8_bin NOT NULL,
  `interfacing` varchar(1024) COLLATE utf8_bin NOT NULL,
  `diagram` char(64) COLLATE utf8_bin NOT NULL,
  `hilCapabilities` varchar(256) COLLATE utf8_bin NOT NULL,
  `hilDiagram` char(64) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`modelID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `ModelInfo`
--

INSERT INTO `ModelInfo` (`modelID`, `modelName`, `authorName`, `authorOrg`, `date`, `version`, `accessibility`, `proprietary`, `symbol`, `accreditation`, `type`, `background`, `specifications`, `dependencies`, `interfacing`, `diagram`, `hilCapabilities`, `hilDiagram`) VALUES
('10000001', 'IEEE 13 node distribution test feeder [ieee13node]', 'R. Hovsapian', 'INL', '2016-05-31', '1.00', '<ul><li>Open source</li><li>Simulation environ. - RSCAD&reg 4.1 and above</li><li>Cross platform transportability - none</li></ul>', 'Public info enough for model modifications. No proprietary information required.', '', 'TRL 3', '<ul><li>System</li><li>Electrical</li><li>Scalability unknown, EMTP type, parameter tuning reqd.</li><li>System level model diagram in SysML?: No</li></ul>', 'This circuit model is very small and used to test common features of distribution analysis software, operating at 4.16 kV. It is characterized by being short, relatively highly loaded, a single voltage regulator at the substation, overhead and underground lines, shunt capacitors, an in-line transformer, and unbalanced loading. Model is built using RSCAD&reg and is suitable for steady-state an dynamic simulations.<br>List of References:<br><ul><li>[ref 1] Data reference for validation - IEEE Documentation( <a href="https://ewh.ieee.org/soc/pes/dsacom/testfeeders/">https://ewh.ieee.org/soc/pes/dsacom/testfeeders/</a>)</li><li>[ref 2] IEEE conference paper for RSCAD&reg model (<a href="http://dx.doi.org/10.1109/NAPS.2014.6965445">http://dx.doi.org/10.1109/NAPS.2014.6965445</a>)</li><li>[ex1] Files for example implementation in RSCAD&reg can be found here (link)</li></ul>', '<ul><li>Assumptions: Node 650 is slack bus; Base load is 3577kW and is attained after 10s of simulation start time</li> <li>Limitations: No frequency dependent loads</li></ul>', '<ul><li>Cross-platform interop: No</li><li>Device level replaceable: No</li><li>Other model docs: [codename for line config. data]</li></ul>', '<ul><li>Platform: RSCAD$reg</li><li>Inputs: Load demand values for spot and distributed loads</li><li>Outputs: RunTime screen values for node voltages and distribution transformer taps positions after 30s</li></ul>', '', 'Not present in current model. I/O signal scaling required.', ''),
('10000002', 'HVAC Equipment', 'A.C. Duckwork', 'ORNL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000003', 'Residential Appliances', 'R. Maytag', 'NREL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000004', 'Commercial Non-HVAC', 'F. Lorescent', 'LBNL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000005', 'PV', 'Sonny Powers', 'NREL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000006', 'Inverter', 'Cy N. Waverly', 'NREL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000007', 'Battery', 'Ann Odegaard', 'SNL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000008', 'Inverter', 'Connnie Verder', 'SNL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000009', 'Electric Vehicle', '', 'ANL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000010', 'Supercapacitor', 'C. Banks', 'INL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000011', 'Flywheel', 'Ken Ettick', 'INL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000012', 'Fuel Cell', '', 'INL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000013', 'Electrolyzer', '', 'INL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', ''),
('10000014', 'Thermal Storage', 'M. Toasty', 'PNNL', '2016-09-09', '0', '', '', '', '', '', '', '', '', '', '', '', '');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
