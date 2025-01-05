-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2025 年 01 月 05 日 22:36
-- 伺服器版本： 8.0.35
-- PHP 版本： 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `gaoduckcreativity`
--

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `u_id` int NOT NULL COMMENT '流水號',
  `ID_num` varchar(10) NOT NULL COMMENT '身份證字號',
  `name` varchar(30) NOT NULL COMMENT '中文名',
  `phone` int NOT NULL COMMENT '電話號碼',
  `email` varchar(70) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'email',
  `password` varchar(50) NOT NULL COMMENT '加密後密碼',
  `address` varchar(60) NOT NULL COMMENT '住址',
  `admin_type` int DEFAULT NULL,
  `rater_title` varchar(50) DEFAULT NULL,
  `role` int NOT NULL COMMENT '1=學生，2=老師，3=評委，999=admin',
  `stu_id` varchar(8) DEFAULT NULL COMMENT '學號'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- 傾印資料表的資料 `user`
--

INSERT INTO `user` (`u_id`, `ID_num`, `name`, `phone`, `email`, `password`, `address`, `admin_type`, `rater_title`, `role`, `stu_id`) VALUES
(4, 'A147909161', '學生1', 922334455, 'student@example.com', 'securepassword', '新北市板橋區', NULL, NULL, 0, '0'),
(7, 'A102954995', '評分者1', 912345678, 'rater@example.com', 'securepassword', '日本日本日本', NULL, '筑波大學電腦科學系副教授', 3, '0'),
(10, 'C117528249', '教師1', 933445566, 'teacher@example.com', 'securepassword', '高雄市苓雅區', NULL, NULL, 0, '0'),
(18, 'C114437590', '超級admin', 987654321, 'admin@example.com', 'saltedpassword7777', '國立高雄大學創新學院', 999, NULL, 0, '0'),
(21, 'A347909163', '學生3', 944556677, 'student3@example.com', 'securepassword3', '台中市西屯區', NULL, NULL, 0, '0'),
(22, 'A447909164', '學生4', 955667788, 'student4@example.com', 'securepassword4', '台南市東區', NULL, NULL, 0, '0'),
(23, 'A547909165', '學生5', 966778899, 'student5@example.com', 'securepassword5', '高雄市左營區', NULL, NULL, 0, '0'),
(24, 'A647909166', '學生6', 977889900, 'student6@example.com', 'securepassword6', '桃園市中壢區', NULL, NULL, 0, '0'),
(25, 'A747909167', '學生7', 988990011, 'student7@example.com', 'securepassword7', '新竹市北區', NULL, NULL, 0, '0'),
(26, 'A847909168', '學生8', 999001122, 'student8@example.com', 'securepassword8', '基隆市仁愛區', NULL, NULL, 0, '0'),
(27, 'A947909169', '學生9', 911223344, 'student9@example.com', 'securepassword9', '苗栗縣竹南鎮', NULL, NULL, 0, '0'),
(28, 'A157909170', '學生10', 922334456, 'student10@example.com', 'securepassword10', '彰化縣彰化市', NULL, NULL, 0, '0'),
(29, 'A167909171', '學生11', 933445567, 'student11@example.com', 'securepassword11', '雲林縣斗六市', NULL, NULL, 0, '0'),
(30, 'A177909172', '學生12', 944556678, 'student12@example.com', 'securepassword12', '嘉義市西區', NULL, NULL, 0, '0'),
(31, 'A187909173', '學生13', 955667789, 'student13@example.com', 'securepassword13', '屏東縣屏東市', NULL, NULL, 0, '0'),
(32, 'A197909174', '學生14', 966778890, 'student14@example.com', 'securepassword14', '花蓮縣花蓮市', NULL, NULL, 0, '0'),
(33, 'A207909175', '學生15', 977889901, 'student15@example.com', 'securepassword15', '宜蘭縣羅東鎮', NULL, NULL, 0, '0'),
(34, 'A217909176', '學生16', 988990012, 'student16@example.com', 'securepassword16', '台東縣台東市', NULL, NULL, 0, '0'),
(35, 'A227909177', '學生17', 999001123, 'student17@example.com', 'securepassword17', '南投縣埔里鎮', NULL, NULL, 0, '0'),
(36, 'A237909178', '學生18', 911223345, 'student18@example.com', 'securepassword18', '澎湖縣馬公市', NULL, NULL, 0, '0'),
(37, 'A247909179', '學生19', 922334457, 'student19@example.com', 'securepassword19', '金門縣金城鎮', NULL, NULL, 0, '0'),
(38, 'A257909180', '學生20', 933445568, 'student20@example.com', 'securepassword20', '連江縣南竿鄉', NULL, NULL, 0, '0'),
(39, 'Z117528222', '教師2', 922222222, 'two@222.com', 'securepassword', '高雄市三民區', NULL, NULL, 0, '0'),
(40, 'O102954775', '評分者2', 966444555, 'rater2@example.edu.tw', 'securepassword', '福建省金門縣', NULL, '金門大學電機工程學系教授', 3, '0'),
(41, 'K521566325', '評分者3', 966777555, 'rater3@example.ac.kr', 'securepassword', 'korea', NULL, '韓國科學技術院信息和通訊工程系講座教授', 3, '0'),
(42, 'Q144909361', '學生2', 922344450, 'studen222t@example.com', 'securepassword', '新北市板橋區', NULL, NULL, 1, 'A1154444'),
(50, 'Q144909351', '評委X', 922344420, 'rt222t@example.com', 'securepassword', '新北市板橋區', NULL, '臺師大', 3, NULL),
(52, 'Q144902351', '評委B', 922343330, 'rt2BBBBBBBB@example.com', 'securepassword', '新北市板橋區', NULL, '臺師大', 3, NULL);

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`u_id`),
  ADD UNIQUE KEY `ID_num` (`ID_num`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `user`
--
ALTER TABLE `user`
  MODIFY `u_id` int NOT NULL AUTO_INCREMENT COMMENT '流水號', AUTO_INCREMENT=53;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
