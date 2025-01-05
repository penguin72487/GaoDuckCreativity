-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2025 年 01 月 05 日 22:37
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
-- 資料表結構 `announcement`
--

CREATE TABLE `announcement` (
  `announcement_id` int NOT NULL,
  `information` text NOT NULL,
  `title` varchar(50) NOT NULL,
  `publisher_u_id` int NOT NULL,
  `publish_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- 傾印資料表的資料 `announcement`
--

INSERT INTO `announcement` (`announcement_id`, `information`, `title`, `publisher_u_id`, `publish_timestamp`, `last_update_timestamp`) VALUES
(1, '<br><h1>測試正文</h1><p>abc</p>', '測試修改標題', 18, '2025-01-04 09:45:39', '2025-01-04 10:21:15'),
(2, '<br>aaa2<br>', '標題', 18, '2025-01-04 09:48:14', '2025-01-04 09:48:14'),
(3, '<br>aaa2<br>', '標afa題', 18, '2025-01-04 09:48:50', '2025-01-04 09:48:50'),
(4, '<br>asedaa1232<br>', '標222題', 18, '2025-01-04 09:48:50', '2025-01-04 09:48:50'),
(5, '<br>aaa423422<br>', '標523題', 18, '2025-01-04 09:48:50', '2025-01-04 09:48:50'),
(6, '<br>aasvsef12123a2<br>', '標daw題', 18, '2025-01-04 09:48:50', '2025-01-04 09:48:50'),
(7, '<br>aaaffsrgsefa2<br>', '標rrwr題', 18, '2025-01-04 09:48:51', '2025-01-04 09:48:51'),
(8, '<br>aaa2<br>', '標題wdaacaef', 18, '2025-01-04 09:48:51', '2025-01-04 09:48:51'),
(9, '<br>aaa2awdawdc<br>', '標ava題', 18, '2025-01-04 09:48:51', '2025-01-04 09:48:51'),
(10, '<br>aaawdawda2<br>', '標ssg題', 18, '2025-01-04 09:48:51', '2025-01-04 09:48:51'),
(11, '<br>aaaffsrawevgsefa2<br>', 'ascaw', 18, '2025-01-04 09:48:51', '2025-01-04 09:48:51'),
(12, '<br>aaa2awdaw<br>', 'sdv', 18, '2025-01-04 09:48:51', '2025-01-04 09:48:51'),
(13, '<br>aaa2awdawdc<br>', 'awdawcvv', 18, '2025-01-04 09:48:52', '2025-01-04 09:48:52'),
(14, '<br>aaawdawda2<br>', 'zscss', 18, '2025-01-04 09:48:52', '2025-01-04 09:48:52'),
(15, '<br>aaaffsrgsefa2<br>', 'egs', 18, '2025-01-04 09:48:52', '2025-01-04 09:48:52'),
(16, '<br>aaa2<br>', '標題wessefsdaacaef', 18, '2025-01-04 09:48:52', '2025-01-04 09:48:52'),
(17, '<br>aaa2awdawdc<br>', 'fhrsr', 18, '2025-01-04 09:48:52', '2025-01-04 09:48:52'),
(18, '<br>aaawdawda2<br>', 'asf', 18, '2025-01-04 09:48:52', '2025-01-04 09:48:52'),
(19, '<br>agsegaa2<br>', '標wesfawd題', 18, '2025-01-04 09:48:53', '2025-01-04 09:48:53');

-- --------------------------------------------------------

--
-- 資料表結構 `file`
--

-- CREATE TABLE `file` (
--   `file_id` int NOT NULL COMMENT '流水號',
--   `file_path` varchar(100) NOT NULL,
--   `uploader_t_id` int DEFAULT NULL COMMENT '如=null，代表該檔案不是任何隊伍成員上傳的，而是管理員為公告上傳的，無需登入也能存取檔案；如非null，代表該檔案為其中一隊隊伍上傳，存取權限為該隊隊伍成員丶該隊指導老師及評審委員'
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --
-- 傾印資料表的資料 `file`
--

-- INSERT INTO `file` (`file_id`, `file_path`, `uploader_t_id`) VALUES
-- (3, 'aahwdalwaouwf.png', NULL),
-- (4, 'ann_att.png', NULL),
-- (5, 'apic_awubd.webp', NULL),
-- (6, 'apic_awubd.webp', 5),
-- (7, 'apic_awubd.webp', NULL),
-- (8, 'apic_awubd.webp', 5);

-- --------------------------------------------------------

--
-- 資料表結構 `project`
--

CREATE TABLE `project` (
  `p_id` int NOT NULL,
  `p_name` varchar(20) NOT NULL,
  `description` text NOT NULL,
  `poster_file_id` int NOT NULL COMMENT '流水號of檔案id',
  `video_link` varchar(100) NOT NULL,
  `github_link` varchar(100) NOT NULL,
  `t_id` int NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最後修改報名時間'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- 傾印資料表的資料 `project`
--

INSERT INTO `project` (`p_id`, `p_name`, `description`, `poster_file_id`, `video_link`, `github_link`, `t_id`, `time`) VALUES
(1, 'cesi', '非常SB的project', 3, 'https://youtube.com/yyy', 'https://github.com/yyy', 5, '2025-01-04 22:16:26');

-- --------------------------------------------------------

--
-- 資料表結構 `review`
--

CREATE TABLE `review` (
  `water_id` int NOT NULL COMMENT '流水號',
  `rater_u_id` int NOT NULL,
  `p_id` int NOT NULL COMMENT 'project',
  `s_creativity` tinyint NOT NULL COMMENT '創意性評分',
  `s_usability` tinyint NOT NULL COMMENT '實用性評分',
  `s_design` tinyint NOT NULL COMMENT '美觀度評分',
  `s_completeness` tinyint NOT NULL COMMENT '完整度評分'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- 傾印資料表的資料 `review`
--

INSERT INTO `review` (`water_id`, `rater_u_id`, `p_id`, `s_creativity`, `s_usability`, `s_design`, `s_completeness`) VALUES
(3, 41, 1, 4, 5, 7, 9),
(4, 40, 1, 9, 8, 7, 6);

-- --------------------------------------------------------

--
-- 資料表結構 `team`
--

CREATE TABLE `team` (
  `t_id` int NOT NULL,
  `t_name` varchar(20) NOT NULL,
  `leader_u_id` int NOT NULL,
  `teacher_u_id` int DEFAULT NULL,
  `join_team_pass` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- 傾印資料表的資料 `team`
--

INSERT INTO `team` (`t_id`, `t_name`, `leader_u_id`, `teacher_u_id`, `join_team_pass`) VALUES
(5, '屌爆了', 4, 10, 'AWVISAJWNS');

-- --------------------------------------------------------

--
-- 資料表結構 `team_student`
--

CREATE TABLE `team_student` (
  `water_id` int NOT NULL,
  `t_id` int NOT NULL,
  `teammate_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- 傾印資料表的資料 `team_student`
--

INSERT INTO `team_student` (`water_id`, `t_id`, `teammate_id`) VALUES
(2, 5, 24),
(3, 5, 25),
(4, 5, 26),
(5, 5, 28),
(6, 5, 29);

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
-- 資料表索引 `announcement`
--
ALTER TABLE `announcement`
  ADD PRIMARY KEY (`announcement_id`),
  ADD KEY `publisher_u_id` (`publisher_u_id`);

--
-- 資料表索引 `file`
--
ALTER TABLE `file`
  ADD PRIMARY KEY (`file_id`),
  ADD KEY `uploader` (`uploader_t_id`);

--
-- 資料表索引 `project`
--
ALTER TABLE `project`
  ADD PRIMARY KEY (`p_id`),
  ADD KEY `poster_file_id` (`poster_file_id`),
  ADD KEY `t_id` (`t_id`);

--
-- 資料表索引 `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`water_id`),
  ADD KEY `p_id` (`p_id`),
  ADD KEY `rater_u_id` (`rater_u_id`);

--
-- 資料表索引 `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`t_id`),
  ADD KEY `leader_u_id` (`leader_u_id`),
  ADD KEY `teacher_u_id` (`teacher_u_id`);

--
-- 資料表索引 `team_student`
--
ALTER TABLE `team_student`
  ADD PRIMARY KEY (`water_id`);

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
-- 使用資料表自動遞增(AUTO_INCREMENT) `announcement`
--
ALTER TABLE `announcement`
  MODIFY `announcement_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `file`
--
ALTER TABLE `file`
  MODIFY `file_id` int NOT NULL AUTO_INCREMENT COMMENT '流水號', AUTO_INCREMENT=9;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `project`
--
ALTER TABLE `project`
  MODIFY `p_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `review`
--
ALTER TABLE `review`
  MODIFY `water_id` int NOT NULL AUTO_INCREMENT COMMENT '流水號', AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `team`
--
ALTER TABLE `team`
  MODIFY `t_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `team_student`
--
ALTER TABLE `team_student`
  MODIFY `water_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `user`
--
ALTER TABLE `user`
  MODIFY `u_id` int NOT NULL AUTO_INCREMENT COMMENT '流水號', AUTO_INCREMENT=53;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `announcement`
--
ALTER TABLE `announcement`
  ADD CONSTRAINT `announcement_ibfk_1` FOREIGN KEY (`publisher_u_id`) REFERENCES `user` (`u_id`);

--
-- 資料表的限制式 `file`
--
ALTER TABLE `file`
  ADD CONSTRAINT `file_ibfk_1` FOREIGN KEY (`uploader_t_id`) REFERENCES `team` (`t_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- 資料表的限制式 `project`
--
ALTER TABLE `project`
  ADD CONSTRAINT `project_ibfk_1` FOREIGN KEY (`t_id`) REFERENCES `team` (`t_id`),
  ADD CONSTRAINT `project_ibfk_2` FOREIGN KEY (`poster_file_id`) REFERENCES `file` (`file_id`);

--
-- 資料表的限制式 `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `project` (`p_id`),
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`rater_u_id`) REFERENCES `user` (`u_id`);

--
-- 資料表的限制式 `team`
--
ALTER TABLE `team`
  ADD CONSTRAINT `team_ibfk_1` FOREIGN KEY (`teacher_u_id`) REFERENCES `user` (`u_id`),
  ADD CONSTRAINT `team_ibfk_2` FOREIGN KEY (`leader_u_id`) REFERENCES `user` (`u_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
