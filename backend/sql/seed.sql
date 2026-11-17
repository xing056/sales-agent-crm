/*
 Navicat Premium Dump SQL

 Source Server         : 本机
 Source Server Type    : MySQL
 Source Server Version : 80044 (8.0.44)
 Source Host           : localhost:3306
 Source Schema         : dj_rbac

 Target Server Type    : MySQL
 Target Server Version : 80044 (8.0.44)
 File Encoding         : 65001

 Date: 06/01/2026 09:14:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `parent_id` int UNSIGNED NULL DEFAULT NULL COMMENT '上级分类id',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '分类名称',
  `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '分类图片',
  `status` tinyint UNSIGNED NULL DEFAULT NULL COMMENT '分类状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '商品分类' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO `category` VALUES (1, NULL, '水光', NULL, 1);
INSERT INTO `category` VALUES (2, 1, '科技水光', NULL, 1);
INSERT INTO `category` VALUES (3, 1, '医学水光', NULL, 1);
INSERT INTO `category` VALUES (4, NULL, '面部护理', NULL, 1);
INSERT INTO `category` VALUES (5, 4, '洁面产品', NULL, 1);
INSERT INTO `category` VALUES (6, 4, '爽肤/调理', NULL, 1);
INSERT INTO `category` VALUES (7, 4, '精华类', NULL, 1);
INSERT INTO `category` VALUES (8, 4, '面霜/乳液', NULL, 1);
INSERT INTO `category` VALUES (9, 4, '眼周护理', NULL, 1);
INSERT INTO `category` VALUES (10, 4, '特殊护理', NULL, 1);
INSERT INTO `category` VALUES (11, 4, '防晒产品', NULL, 1);
INSERT INTO `category` VALUES (12, NULL, '彩妆', NULL, 1);
INSERT INTO `category` VALUES (13, 12, '底妆', NULL, 1);
INSERT INTO `category` VALUES (14, 12, '眼妆', NULL, 1);
INSERT INTO `category` VALUES (15, 12, '唇妆', NULL, 1);
INSERT INTO `category` VALUES (16, 12, '腮红/修容/高光', NULL, 1);
INSERT INTO `category` VALUES (17, 12, '彩妆工具', NULL, 1);
INSERT INTO `category` VALUES (18, NULL, '身体护理', NULL, 1);
INSERT INTO `category` VALUES (19, 18, '沐浴清洁', NULL, 1);
INSERT INTO `category` VALUES (20, 18, '身体保湿', NULL, 1);
INSERT INTO `category` VALUES (21, 18, '特殊护理', NULL, 1);
INSERT INTO `category` VALUES (22, 18, '脱毛产品', NULL, 1);
INSERT INTO `category` VALUES (23, NULL, '香氛', NULL, 1);
INSERT INTO `category` VALUES (24, 23, '香水', NULL, 1);
INSERT INTO `category` VALUES (25, 23, '香氛护理', NULL, 1);
INSERT INTO `category` VALUES (26, NULL, '美容仪器', NULL, 1);
INSERT INTO `category` VALUES (27, 26, '护肤仪器', NULL, 1);
INSERT INTO `category` VALUES (28, 26, '脱毛/修眉工具', NULL, 1);
INSERT INTO `category` VALUES (29, 26, '其他工具', NULL, 1);
INSERT INTO `category` VALUES (30, NULL, '保健食品', '', 1);

-- ----------------------------
-- Table structure for commission
-- ----------------------------
DROP TABLE IF EXISTS `commission`;
CREATE TABLE `commission`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int UNSIGNED NULL DEFAULT NULL COMMENT '员工user_id',
  `commission` decimal(10, 2) UNSIGNED NULL DEFAULT NULL COMMENT '提成金额',
  `year_month` int UNSIGNED NULL DEFAULT NULL COMMENT '所属期,如202601',
  `status` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '状态',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `commission_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `commission_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '员工提成(佣金)表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of commission
-- ----------------------------
INSERT INTO `commission` VALUES (1, 1, 943.60, 202601, 1, '2026-01-06 00:55:51');

-- ----------------------------
-- Table structure for customer
-- ----------------------------
DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `source_id` int UNSIGNED NULL DEFAULT NULL COMMENT '客户来源',
  `parent_id` int UNSIGNED NULL DEFAULT NULL COMMENT '推荐者id',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '客户性名',
  `phone` char(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '客户手机',
  `user_id` int UNSIGNED NULL DEFAULT NULL COMMENT '销售人员id',
  `province` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '省份',
  `city` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '城市',
  `county` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '区县',
  `address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '具体通信地址',
  `status` tinyint UNSIGNED NULL DEFAULT NULL COMMENT '状态 0-正常 1-锁定(跟进中...)',
  `level` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '客户等级: 1-一般客户 2-重点客户',
  `order_count` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '消费次数',
  `order_amount` decimal(10, 2) UNSIGNED NULL DEFAULT 0.00 COMMENT '消费总金额',
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '客户备注',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '添加时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `phone`(`phone` ASC) USING BTREE COMMENT '手机号码',
  INDEX `source_id`(`source_id` ASC) USING BTREE COMMENT '客户来源',
  INDEX `customer_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `customer_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `source_id` FOREIGN KEY (`source_id`) REFERENCES `customer_source` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 108 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '客户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of customer
-- ----------------------------
INSERT INTO `customer` VALUES (1, 1, 3, '韩楚风', '13800000001', 1, '北京市', '市辖区', '海淀区', '上地五街', 1, 1, 0, 0.00, '客户备注', '2025-12-27 13:49:32', '2025-12-29 06:57:03');
INSERT INTO `customer` VALUES (2, 2, NULL, '李纯风', '13800000002', 1, '北京市', '市辖区', '顺义区', '后沙峪', 1, 1, 0, 0.00, '客户备注', '2025-12-27 13:49:33', '2025-12-27 13:49:33');
INSERT INTO `customer` VALUES (3, 2, NULL, '张大千', '13800000003', 2, '上海市', '市辖区', '静安区', '静安寺', 1, 0, 0, 0.00, '客户备注', '2025-12-28 13:21:19', '2025-12-30 09:15:48');
INSERT INTO `customer` VALUES (4, 3, NULL, '催恩熙', '13800000004', 2, '广东省', '深圳市', '宝安区', '宝安中心', 1, 0, 0, 0.00, '客户备注', '2025-12-27 13:47:47', '2025-12-27 13:47:47');
INSERT INTO `customer` VALUES (5, 1, NULL, '李白', '13800000005', 1, '河北省', '石家庄市', '长安区', '人民路', 1, 1, 0, 0.00, '', '2025-12-29 05:50:05', '2025-12-29 05:50:05');
INSERT INTO `customer` VALUES (6, 1, 1, '杜甫', '13800000006', 1, '山西省', '太原市', '小店区', '人民路', 1, 1, 0, 0.00, '', '2025-12-29 05:54:13', '2025-12-29 05:54:13');
INSERT INTO `customer` VALUES (7, 3, NULL, '杨万里', '13800000007', 1, '内蒙古自治区', '乌海市', '海南区', '大草原', 1, 1, 0, 0.00, '', '2025-12-29 06:04:23', '2025-12-29 06:04:23');
INSERT INTO `customer` VALUES (8, 7, 3, '侯詩涵', '13800000008', 1, '深圳', '深圳', '龙岗区学园一巷97号', '龙岗区学园一巷97号', 1, 1, 0, 0.00, 'Always keep your eyes open. Keep watching. Because whatever you see can inspire you.                ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (9, 4, 4, '彭璐', '13800000009', 1, '中山', '中山', '乐丰六路219号', '乐丰六路219号', 0, 0, 0, 0.00, 'All the Navicat Cloud objects are located under different projects. You can share                   ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (10, 1, 7, '谢詩涵', '13800000010', 1, '中山', '中山', '乐丰六路876号', '乐丰六路876号', 0, 0, 0, 0.00, 'To successfully establish a new connection to local/remote server - no matter via                   ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (11, 7, 7, '杨致远', '13800000011', 1, '深圳', '深圳', '龙岗区布吉镇西环路648号', '龙岗区布吉镇西环路648号', 0, 1, 0, 0.00, 'SQL Editor allows you to create and edit SQL text, prepare and execute selected queries.            ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (12, 4, 6, '朱睿', '13800000012', 1, '东莞', '东莞', '坑美十五巷404号', '坑美十五巷404号', 0, 0, 0, 0.00, 'The repository database can be an existing MySQL, MariaDB, PostgreSQL, SQL Server,                  ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (13, 2, 5, '孟子异', '13800000013', 1, '成都市', '成都市', '成华区玉双路6号47号', '成华区玉双路6号47号', 0, 1, 0, 0.00, 'Navicat Monitor can be installed on any local computer or virtual machine and does                  ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (14, 1, 6, '尹云熙', '13800000014', 1, '上海市', '上海市', '闵行区宾川路437号', '闵行区宾川路437号', 1, 0, 0, 0.00, 'Such sessions are also susceptible to session hijacking, where a malicious user takes               ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (15, 9, 3, '雷子韬', '13800000015', 1, '上海市', '上海市', '黄浦区淮海中路328号', '黄浦区淮海中路328号', 1, 0, 0, 0.00, 'What you get by achieving your goals is not as important as what you become by achieving your goals.', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (16, 4, 6, '孙嘉伦', '13800000016', 4, '北京市', '北京市', '朝阳区三里屯路891号', '朝阳区三里屯路891号', 1, 1, 0, 0.00, 'The Synchronize to Database function will give you a full picture of all database differences.      ', '2025-06-29 09:02:32', '2025-01-02 00:17:56');
INSERT INTO `customer` VALUES (17, 3, 4, '萧詩涵', '13800000017', 1, '广州市', '广州市', '海珠区江南西路34号', '海珠区江南西路34号', 0, 0, 0, 0.00, 'I will greet this day with love in my heart. If the Show objects under schema in                    ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (18, 4, 3, '叶子韬', '13800000018', 4, '深圳', '深圳', '福田区深南大道374号', '福田区深南大道374号', 1, 0, 0, 0.00, 'To clear or reload various internal caches, flush tables, or acquire locks, control-click           ', '2025-08-30 18:51:39', '2025-10-07 15:55:28');
INSERT INTO `customer` VALUES (19, 1, 3, '陶震南', '13800000019', 1, '北京市', '北京市', '東城区東直門內大街145号', '東城区東直門內大街145号', 0, 1, 0, 0.00, 'The Synchronize to Database function will give you a full picture of all database differences.      ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (20, 6, 3, '段子韬', '13800000020', 1, '东莞', '东莞', '环区南街二巷988号', '环区南街二巷988号', 1, 1, 0, 0.00, 'You will succeed because most people are lazy. HTTP Tunneling is a method for connecting            ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (21, 3, 3, '曹安琪', '13800000021', 7, '北京市', '北京市', '西城区西長安街573号', '西城区西長安街573号', 0, 0, 0, 0.00, 'It wasn’t raining when Noah built the ark. Such sessions are also susceptible to                  ', '2025-06-12 07:24:02', '2025-02-23 08:52:48');
INSERT INTO `customer` VALUES (22, 1, 3, '邓云熙', '13800000022', 1, '深圳', '深圳', '罗湖区蔡屋围深南东路174号', '罗湖区蔡屋围深南东路174号', 0, 0, 0, 0.00, 'Creativity is intelligence having fun. A man’s best friends are his ten fingers.                  ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (23, 10, 3, '田震南', '13800000023', 7, '中山', '中山', '京华商圈华夏街927号', '京华商圈华夏街927号', 1, 1, 0, 0.00, 'To get a secure connection, the first thing you need to do is to install OpenSSL                    ', '2025-12-07 19:29:51', '2025-06-25 23:31:43');
INSERT INTO `customer` VALUES (24, 4, 3, '苏璐', '13800000024', 1, '北京市', '北京市', '东城区东单王府井东街467号', '东城区东单王府井东街467号', 0, 1, 0, 0.00, 'Navicat 15 has added support for the system-wide dark mode. Navicat Data Modeler                    ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (25, 9, 6, '余安琪', '13800000025', 1, '上海市', '上海市', '闵行区宾川路466号', '闵行区宾川路466号', 0, 1, 0, 0.00, 'I destroy my enemies when I make them my friends. If it scares you, it might be a good thing to try.', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (26, 9, 3, '孟詩涵', '13800000026', 6, '北京市', '北京市', '西城区西長安街741号', '西城区西長安街741号', 0, 0, 0, 0.00, 'Anyone who has ever made anything of importance was disciplined. If it scares you,                  ', '2025-03-18 13:42:50', '2025-01-25 09:25:57');
INSERT INTO `customer` VALUES (27, 2, 3, '萧震南', '13800000027', 3, '广州市', '广州市', '天河区天河路815号', '天河区天河路815号', 0, 1, 0, 0.00, 'It wasn’t raining when Noah built the ark. To start working with your server in                   ', '2025-01-21 09:23:02', '2025-07-23 17:02:46');
INSERT INTO `customer` VALUES (28, 9, 6, '武子韬', '13800000028', 1, '东莞', '东莞', '坑美十五巷598号', '坑美十五巷598号', 0, 0, 0, 0.00, 'Success consists of going from failure to failure without loss of enthusiasm.                       ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (29, 10, 5, '段岚', '13800000029', 4, '成都市', '成都市', '成华区双庆路23号', '成华区双庆路23号', 0, 0, 0, 0.00, 'Navicat Data Modeler enables you to build high-quality conceptual, logical and physical             ', '2025-03-10 14:33:00', '2025-05-05 17:34:03');
INSERT INTO `customer` VALUES (30, 9, 3, '袁震南', '13800000030', 1, '北京市', '北京市', '延庆区028县道313号', '延庆区028县道313号', 0, 0, 0, 0.00, 'It provides strong authentication and secure encrypted communications between two                   ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (31, 3, 7, '袁詩涵', '13800000031', 1, '成都市', '成都市', '成华区双庆路31号', '成华区双庆路31号', 0, 0, 0, 0.00, 'Navicat Cloud could not connect and access your databases. By which it means, it                    ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (32, 9, 2, '武秀英', '13800000032', 1, '成都市', '成都市', '成华区双庆路244号', '成华区双庆路244号', 1, 0, 0, 0.00, 'SSH serves to prevent such vulnerabilities and allows you to access a remote server\'s               ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (33, 3, 3, '孔杰宏', '13800000033', 3, '北京市', '北京市', '西城区西長安街388号', '西城区西長安街388号', 0, 0, 0, 0.00, 'Creativity is intelligence having fun. All the Navicat Cloud objects are located                    ', '2025-07-12 18:20:11', '2025-05-21 13:05:30');
INSERT INTO `customer` VALUES (34, 9, 4, '沈岚', '13800000034', 1, '广州市', '广州市', '天河区天河路504号', '天河区天河路504号', 0, 0, 0, 0.00, 'To successfully establish a new connection to local/remote server - no matter via                   ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (35, 8, 3, '高杰宏', '13800000035', 1, '上海市', '上海市', '闵行区宾川路940号', '闵行区宾川路940号', 0, 0, 0, 0.00, 'How we spend our days is, of course, how we spend our lives. It provides strong authentication      ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (36, 9, 2, '于宇宁', '13800000036', 1, '中山', '中山', '京华商圈华夏街821号', '京华商圈华夏街821号', 1, 1, 0, 0.00, 'Anyone who has never made a mistake has never tried anything new. Genius is an infinite             ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (37, 6, 5, '马安琪', '13800000037', 1, '北京市', '北京市', '東城区東直門內大街890号', '東城区東直門內大街890号', 1, 1, 0, 0.00, 'The Navigation pane employs tree structure which allows you to take action upon the                 ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (38, 5, 6, '廖晓明', '13800000038', 1, '北京市', '北京市', '东城区东单王府井东街606号', '东城区东单王府井东街606号', 0, 1, 0, 0.00, 'HTTP Tunneling is a method for connecting to a server that uses the same protocol                   ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (39, 7, 3, '吕杰宏', '13800000039', 8, '中山', '中山', '天河区大信商圈大信南路997号', '天河区大信商圈大信南路997号', 0, 0, 0, 0.00, 'SSH serves to prevent such vulnerabilities and allows you to access a remote server\'s               ', '2025-12-12 04:11:26', '2025-04-30 13:29:56');
INSERT INTO `customer` VALUES (40, 6, 6, '熊璐', '13800000040', 1, '上海市', '上海市', '浦东新区健祥路903号', '浦东新区健祥路903号', 1, 1, 0, 0.00, 'I destroy my enemies when I make them my friends. A comfort zone is a beautiful place,              ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (41, 8, 4, '苏晓明', '13800000041', 6, '上海市', '上海市', '闵行区宾川路484号', '闵行区宾川路484号', 0, 0, 0, 0.00, 'The On Startup feature allows you to control what tabs appear when you launch Navicat.              ', '2026-01-03 21:03:27', '2025-03-22 05:34:47');
INSERT INTO `customer` VALUES (42, 9, 1, '张秀英', '13800000042', 4, '深圳', '深圳', '罗湖区蔡屋围深南东路954号', '罗湖区蔡屋围深南东路954号', 1, 0, 0, 0.00, 'A query is used to extract data from the database in a readable format according                    ', '2025-05-23 08:50:14', '2025-12-23 22:13:30');
INSERT INTO `customer` VALUES (43, 10, 4, '方震南', '13800000043', 1, '上海市', '上海市', '徐汇区虹桥路477号', '徐汇区虹桥路477号', 0, 1, 0, 0.00, 'It wasn’t raining when Noah built the ark. It can also manage cloud databases such                ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (44, 9, 1, '钟晓明', '13800000044', 1, '上海市', '上海市', '浦东新区橄榄路760号', '浦东新区橄榄路760号', 1, 1, 0, 0.00, 'The Navigation pane employs tree structure which allows you to take action upon the                 ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (45, 4, 5, '罗嘉伦', '13800000045', 1, '东莞', '东莞', '东泰五街137号', '东泰五街137号', 0, 1, 0, 0.00, 'Anyone who has ever made anything of importance was disciplined. Navicat allows you                 ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (46, 4, 4, '孟睿', '13800000046', 1, '中山', '中山', '天河区大信商圈大信南路870号', '天河区大信商圈大信南路870号', 1, 0, 0, 0.00, 'If the plan doesn’t work, change the plan, but never the goal. The repository database            ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (47, 9, 4, '冯安琪', '13800000047', 2, '上海市', '上海市', '浦东新区健祥路509号', '浦东新区健祥路509号', 0, 0, 0, 0.00, 'Instead of wondering when your next vacation is, maybe you should set up a life you                 ', '2025-11-03 07:04:00', '2025-07-03 14:23:36');
INSERT INTO `customer` VALUES (48, 8, 4, '孟子异', '13800000048', 1, '北京市', '北京市', '朝阳区三里屯路627号', '朝阳区三里屯路627号', 0, 0, 0, 0.00, 'Difficult circumstances serve as a textbook of life for people. To successfully establish           ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (49, 2, 6, '严安琪', '13800000049', 1, '北京市', '北京市', '海淀区清河中街68号669号', '海淀区清河中街68号669号', 0, 1, 0, 0.00, 'Navicat Monitor requires a repository to store alerts and metrics for historical analysis.          ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (50, 9, 6, '谭震南', '13800000050', 1, '上海市', '上海市', '浦东新区橄榄路806号', '浦东新区橄榄路806号', 1, 1, 0, 0.00, 'Navicat Data Modeler enables you to build high-quality conceptual, logical and physical             ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (51, 10, 4, '汤云熙', '13800000051', 1, '广州市', '广州市', '白云区小坪东路280号', '白云区小坪东路280号', 1, 1, 0, 0.00, 'Navicat 15 has added support for the system-wide dark mode. You will succeed because                ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (52, 2, 3, '雷致远', '13800000052', 1, '北京市', '北京市', '海淀区清河中街68号822号', '海淀区清河中街68号822号', 0, 1, 0, 0.00, 'Typically, it is employed as an encrypted version of Telnet. Navicat Cloud could                    ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (53, 10, 3, '陶詩涵', '13800000053', 2, '北京市', '北京市', '西城区西長安街504号', '西城区西長安街504号', 1, 1, 0, 0.00, 'I will greet this day with love in my heart. To clear or reload various internal                    ', '2025-11-15 11:27:23', '2025-12-31 08:20:43');
INSERT INTO `customer` VALUES (54, 2, 3, '傅杰宏', '13800000054', 7, '深圳', '深圳', '罗湖区田贝一路478号', '罗湖区田贝一路478号', 0, 0, 0, 0.00, 'Monitored servers include MySQL, MariaDB and SQL Server, and compatible with cloud                  ', '2025-02-24 13:58:39', '2025-06-13 14:13:31');
INSERT INTO `customer` VALUES (55, 7, 7, '严宇宁', '13800000055', 3, '北京市', '北京市', '朝阳区三里屯路991号', '朝阳区三里屯路991号', 1, 1, 0, 0.00, 'Remember that failure is an event, not a person. After logged in the Navicat Cloud                  ', '2025-06-03 13:31:24', '2025-12-12 20:29:20');
INSERT INTO `customer` VALUES (56, 1, 3, '龙嘉伦', '13800000056', 1, '上海市', '上海市', '浦东新区健祥路140号', '浦东新区健祥路140号', 0, 1, 0, 0.00, 'Anyone who has ever made anything of importance was disciplined. A man is not old                   ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (57, 3, 4, '朱睿', '13800000057', 1, '成都市', '成都市', '成华区双庆路352号', '成华区双庆路352号', 0, 0, 0, 0.00, 'I destroy my enemies when I make them my friends. If opportunity doesn’t knock, build a door.     ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (58, 2, 3, '吕晓明', '13800000058', 1, '上海市', '上海市', '徐汇区虹桥路788号', '徐汇区虹桥路788号', 1, 1, 0, 0.00, 'If opportunity doesn’t knock, build a door. In the middle of winter I at last discovered          ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (59, 10, 3, '余璐', '13800000059', 1, '成都市', '成都市', '锦江区人民南路四段30号', '锦江区人民南路四段30号', 1, 0, 0, 0.00, 'The reason why a great man is great is that he resolves to be a great man.                          ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (60, 6, 3, '邓安琪', '13800000060', 1, '广州市', '广州市', '白云区小坪东路264号', '白云区小坪东路264号', 0, 1, 0, 0.00, 'Import Wizard allows you to import data to tables/collections from CSV, TXT, XML, DBF and more.     ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (61, 2, 3, '戴子韬', '13800000061', 1, '上海市', '上海市', '闵行区宾川路490号', '闵行区宾川路490号', 1, 0, 0, 0.00, 'I destroy my enemies when I make them my friends. You cannot save people, you can just love them.   ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (62, 1, 6, '贺安琪', '13800000062', 1, '东莞', '东莞', '坑美十五巷193号', '坑美十五巷193号', 0, 1, 0, 0.00, 'A query is used to extract data from the database in a readable format according                    ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (63, 7, 4, '莫云熙', '13800000063', 1, '成都市', '成都市', '成华区玉双路6号682号', '成华区玉双路6号682号', 0, 0, 0, 0.00, 'Import Wizard allows you to import data to tables/collections from CSV, TXT, XML, DBF and more.     ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (64, 9, 3, '叶子异', '13800000064', 1, '东莞', '东莞', '东泰五街674号', '东泰五街674号', 0, 1, 0, 0.00, 'SQL Editor allows you to create and edit SQL text, prepare and execute selected queries.            ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (65, 1, 1, '廖璐', '13800000065', 1, '上海市', '上海市', '浦东新区橄榄路28号', '浦东新区橄榄路28号', 1, 1, 0, 0.00, 'Navicat 15 has added support for the system-wide dark mode. To get a secure connection,             ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (66, 9, 2, '曹晓明', '13800000066', 1, '北京市', '北京市', '延庆区028县道262号', '延庆区028县道262号', 1, 0, 0, 0.00, 'If it scares you, it might be a good thing to try. The first step is as good as half over.          ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (67, 7, 1, '高嘉伦', '13800000067', 1, '北京市', '北京市', '朝阳区三里屯路219号', '朝阳区三里屯路219号', 1, 0, 0, 0.00, 'To start working with your server in Navicat, you should first establish a connection               ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (68, 6, 7, '赵致远', '13800000068', 1, '上海市', '上海市', '黄浦区淮海中路480号', '黄浦区淮海中路480号', 1, 0, 0, 0.00, 'You must be the change you wish to see in the world. The Information Pane shows the                 ', '2025-10-20 05:17:43', '2025-11-11 16:49:54');
INSERT INTO `customer` VALUES (69, 4, 5, '宋震南', '13800000069', 4, '深圳', '深圳', '罗湖区蔡屋围深南东路616号', '罗湖区蔡屋围深南东路616号', 1, 1, 0, 0.00, 'With its well-designed Graphical User Interface(GUI), Navicat lets you quickly and                  ', '2025-08-24 06:07:50', '2025-01-03 01:22:13');
INSERT INTO `customer` VALUES (70, 3, 4, '严秀英', '13800000070', 4, '中山', '中山', '京华商圈华夏街563号', '京华商圈华夏街563号', 1, 0, 0, 0.00, 'HTTP Tunneling is a method for connecting to a server that uses the same protocol                   ', '2025-04-15 23:35:57', '2025-12-02 16:16:55');
INSERT INTO `customer` VALUES (71, 4, 4, '黎晓明', '13800000071', 8, '深圳', '深圳', '龙岗区布吉镇西环路780号', '龙岗区布吉镇西环路780号', 1, 0, 0, 0.00, 'Typically, it is employed as an encrypted version of Telnet. Export Wizard allows                   ', '2025-06-05 17:00:00', '2025-01-28 12:41:24');
INSERT INTO `customer` VALUES (72, 6, 1, '龚震南', '13800000072', 1, '广州市', '广州市', '白云区小坪东路792号', '白云区小坪东路792号', 0, 1, 0, 0.00, 'Instead of wondering when your next vacation is, maybe you should set up a life you                 ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (73, 3, 4, '蔡子异', '13800000073', 1, '成都市', '成都市', '锦江区人民南路四段315号', '锦江区人民南路四段315号', 1, 0, 0, 0.00, 'Navicat is a multi-connections Database Administration tool allowing you to connect                 ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (74, 6, 6, '崔安琪', '13800000074', 1, '上海市', '上海市', '浦东新区健祥路581号', '浦东新区健祥路581号', 1, 0, 0, 0.00, 'Genius is an infinite capacity for taking pains. In the middle of winter I at last                  ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (75, 5, 6, '龙晓明', '13800000075', 1, '北京市', '北京市', '延庆区028县道285号', '延庆区028县道285号', 0, 0, 0, 0.00, 'A man’s best friends are his ten fingers. It can also manage cloud databases such                 ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (76, 7, 6, '邵震南', '13800000076', 1, '深圳', '深圳', '龙岗区布吉镇西环路755号', '龙岗区布吉镇西环路755号', 0, 1, 0, 0.00, 'Navicat Data Modeler is a powerful and cost-effective database design tool which                    ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (77, 8, 1, '贾秀英', '13800000077', 1, '深圳', '深圳', '罗湖区清水河一路408号', '罗湖区清水河一路408号', 1, 0, 0, 0.00, 'Monitored servers include MySQL, MariaDB and SQL Server, and compatible with cloud                  ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (78, 4, 2, '郭詩涵', '13800000078', 1, '北京市', '北京市', '東城区東直門內大街893号', '東城区東直門內大街893号', 1, 1, 0, 0.00, 'Instead of wondering when your next vacation is, maybe you should set up a life you                 ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (79, 2, 4, '姚致远', '13800000079', 1, '上海市', '上海市', '浦东新区橄榄路464号', '浦东新区橄榄路464号', 0, 1, 0, 0.00, 'It wasn’t raining when Noah built the ark. Actually it is just in an idea when                    ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (80, 5, 2, '魏云熙', '13800000080', 4, '深圳', '深圳', '罗湖区蔡屋围深南东路232号', '罗湖区蔡屋围深南东路232号', 1, 1, 0, 0.00, 'A query is used to extract data from the database in a readable format according                    ', '2025-09-09 12:41:34', '2025-05-22 04:16:23');
INSERT INTO `customer` VALUES (81, 9, 4, '梁詩涵', '13800000081', 1, '深圳', '深圳', '罗湖区蔡屋围深南东路946号', '罗湖区蔡屋围深南东路946号', 1, 1, 0, 0.00, 'After logged in the Navicat Cloud feature, the Navigation pane will be divided into                 ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (82, 4, 7, '傅璐', '13800000082', 1, '广州市', '广州市', '白云区机场路棠苑街五巷637号', '白云区机场路棠苑街五巷637号', 0, 1, 0, 0.00, 'You cannot save people, you can just love them. It wasn’t raining when Noah built the ark.        ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (83, 6, 5, '陈安琪', '13800000083', 1, '成都市', '成都市', '成华区双庆路119号', '成华区双庆路119号', 0, 0, 0, 0.00, 'The Information Pane shows the detailed object information, project activities, the                 ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (84, 7, 4, '孟云熙', '13800000084', 1, '成都市', '成都市', '锦江区人民南路四段705号', '锦江区人民南路四段705号', 1, 1, 0, 0.00, 'Navicat authorizes you to make connection to remote servers running on different                    ', '2025-09-13 14:14:56', '2025-02-21 07:57:55');
INSERT INTO `customer` VALUES (85, 3, 4, '周震南', '13800000085', 7, '广州市', '广州市', '天河区天河路95号', '天河区天河路95号', 0, 0, 0, 0.00, 'After comparing data, the window shows the number of records that will be inserted,                 ', '2025-05-08 06:21:28', '2025-10-20 15:01:16');
INSERT INTO `customer` VALUES (86, 5, 6, '杨岚', '13800000086', 1, '上海市', '上海市', '闵行区宾川路659号', '闵行区宾川路659号', 0, 0, 0, 0.00, 'All journeys have secret destinations of which the traveler is unaware.                             ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (87, 4, 2, '郭秀英', '13800000087', 4, '成都市', '成都市', '成华区玉双路6号885号', '成华区玉双路6号885号', 0, 1, 0, 0.00, 'Flexible settings enable you to set up a custom key for comparison and synchronization.             ', '2025-12-25 14:46:07', '2025-09-29 01:52:33');
INSERT INTO `customer` VALUES (88, 1, 1, '阎安琪', '13800000088', 1, '深圳', '深圳', '福田区深南大道761号', '福田区深南大道761号', 1, 1, 0, 0.00, 'Success consists of going from failure to failure without loss of enthusiasm.                       ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (89, 4, 3, '向璐', '13800000089', 1, '广州市', '广州市', '海珠区江南西路667号', '海珠区江南西路667号', 1, 0, 0, 0.00, 'There is no way to happiness. Happiness is the way. Secure SHell (SSH) is a program                 ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (90, 10, 4, '廖子异', '13800000090', 1, '深圳', '深圳', '龙岗区学园一巷115号', '龙岗区学园一巷115号', 1, 1, 0, 0.00, 'To connect to a database or schema, simply double-click it in the pane.                             ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (91, 3, 3, '潘致远', '13800000091', 1, '中山', '中山', '紫马岭商圈中山五路508号', '紫马岭商圈中山五路508号', 0, 0, 0, 0.00, 'It collects process metrics such as CPU load, RAM usage, and a variety of other resources           ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (92, 1, 6, '雷睿', '13800000092', 3, '北京市', '北京市', '房山区岳琉路532号', '房山区岳琉路532号', 1, 1, 0, 0.00, 'The Main Window consists of several toolbars and panes for you to work on connections,              ', '2025-08-09 05:00:17', '2025-01-06 16:36:00');
INSERT INTO `customer` VALUES (93, 6, 6, '于云熙', '13800000093', 2, '北京市', '北京市', '朝阳区三里屯路89号', '朝阳区三里屯路89号', 1, 0, 0, 0.00, 'In the Objects tab, you can use the List List, Detail Detail and ER Diagram ER Diagram              ', '2025-01-05 16:33:22', '2025-11-25 19:05:40');
INSERT INTO `customer` VALUES (94, 9, 4, '马子异', '13800000094', 1, '北京市', '北京市', '东城区东单王府井东街480号', '东城区东单王府井东街480号', 1, 0, 0, 0.00, 'To successfully establish a new connection to local/remote server - no matter via                   ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (95, 8, 4, '朱安琪', '13800000095', 1, '中山', '中山', '天河区大信商圈大信南路38号', '天河区大信商圈大信南路38号', 0, 1, 0, 0.00, 'Always keep your eyes open. Keep watching. Because whatever you see can inspire you.                ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (96, 5, 2, '顾杰宏', '13800000096', 1, '深圳', '深圳', '福田区景田东一街637号', '福田区景田东一街637号', 1, 0, 0, 0.00, 'Navicat Data Modeler enables you to build high-quality conceptual, logical and physical             ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (97, 1, 2, '邹云熙', '13800000097', 1, '东莞', '东莞', '坑美十五巷684号', '坑美十五巷684号', 0, 0, 0, 0.00, 'Secure Sockets Layer(SSL) is a protocol for transmitting private documents via the Internet.        ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (98, 10, 2, '朱安琪', '13800000098', 1, '东莞', '东莞', '珊瑚路250号', '珊瑚路250号', 0, 0, 0, 0.00, 'A man is not old until regrets take the place of dreams. In the middle of winter                    ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (99, 4, 3, '钟嘉伦', '13800000099', 1, '广州市', '广州市', '白云区小坪东路520号', '白云区小坪东路520号', 1, 1, 0, 0.00, 'Navicat Data Modeler is a powerful and cost-effective database design tool which                    ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (100, 2, 6, '高震南', '13800000100', 1, '深圳', '深圳', '罗湖区清水河一路667号', '罗湖区清水河一路667号', 0, 0, 0, 0.00, 'If the Show objects under schema in navigation pane option is checked at the Preferences            ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (101, 4, 3, '吴杰宏', '13800000101', 1, '深圳', '深圳', '罗湖区蔡屋围深南东路746号', '罗湖区蔡屋围深南东路746号', 0, 1, 0, 0.00, 'If the plan doesn’t work, change the plan, but never the goal. Remember that failure              ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (102, 7, 4, '邓睿', '13800000102', 1, '中山', '中山', '乐丰六路845号', '乐丰六路845号', 0, 1, 0, 0.00, 'What you get by achieving your goals is not as important as what you become by achieving your goals.', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (103, 10, 7, '韦杰宏', '13800000103', 1, '深圳', '深圳', '罗湖区蔡屋围深南东路764号', '罗湖区蔡屋围深南东路764号', 0, 0, 0, 0.00, 'A query is used to extract data from the database in a readable format according                    ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');
INSERT INTO `customer` VALUES (104, 7, 6, '邹嘉伦', '13800000104', 3, '成都市', '成都市', '成华区二仙桥东三路654号', '成华区二仙桥东三路654号', 0, 0, 0, 0.00, 'Import Wizard allows you to import data to tables/collections from CSV, TXT, XML, DBF and more.     ', '2025-12-10 17:20:00', '2025-10-03 22:55:15');
INSERT INTO `customer` VALUES (105, 4, 2, '姚震南', '13800000105', 1, '北京市', '北京市', '海淀区清河中街68号966号', '海淀区清河中街68号966号', 0, 1, 0, 0.00, 'You cannot save people, you can just love them. Navicat Monitor can be installed                    ', '2025-10-19 03:46:37', '2025-02-07 14:28:29');
INSERT INTO `customer` VALUES (106, 8, 6, '董晓明', '13800000106', 4, '北京市', '北京市', '東城区東直門內大街723号', '東城区東直門內大街723号', 0, 1, 0, 0.00, 'You can select any connections, objects or projects, and then select the corresponding              ', '2025-05-15 23:09:23', '2025-05-05 04:56:34');
INSERT INTO `customer` VALUES (107, 2, 6, '李震南', '13800000107', 1, '上海市', '上海市', '黄浦区淮海中路271号', '黄浦区淮海中路271号', 1, 1, 0, 0.00, 'If the Show objects under schema in navigation pane option is checked at the Preferences            ', '2026-01-05 13:21:59', '2026-01-05 13:21:59');

-- ----------------------------
-- Table structure for customer_source
-- ----------------------------
DROP TABLE IF EXISTS `customer_source`;
CREATE TABLE `customer_source`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '客户来源',
  `status` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '客户来源表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of customer_source
-- ----------------------------
INSERT INTO `customer_source` VALUES (1, '老客户推荐', 1);
INSERT INTO `customer_source` VALUES (2, '抖音', 1);
INSERT INTO `customer_source` VALUES (3, '快手', 1);
INSERT INTO `customer_source` VALUES (4, '微信', 1);
INSERT INTO `customer_source` VALUES (5, '微博', 1);
INSERT INTO `customer_source` VALUES (6, '官网', 1);
INSERT INTO `customer_source` VALUES (7, '商场广告', 1);
INSERT INTO `customer_source` VALUES (8, '地铁广告', 1);
INSERT INTO `customer_source` VALUES (9, '公交站牌广告', 1);
INSERT INTO `customer_source` VALUES (10, '公交车体广告', 1);

-- ----------------------------
-- Table structure for customer_tracking
-- ----------------------------
DROP TABLE IF EXISTS `customer_tracking`;
CREATE TABLE `customer_tracking`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `customer_id` int UNSIGNED NULL DEFAULT NULL COMMENT '客户id',
  `user_id` int UNSIGNED NULL DEFAULT NULL COMMENT '用户id',
  `tracking_way` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '跟踪方式',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '结果描述',
  `tracking_time` datetime NULL DEFAULT NULL COMMENT '跟踪时间',
  `status` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '跟踪状态 0失败 1-成功',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tracking_customer_id`(`customer_id` ASC) USING BTREE,
  INDEX `tracking_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `tracking_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `tracking_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '客户跟踪记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of customer_tracking
-- ----------------------------
INSERT INTO `customer_tracking` VALUES (1, 1, 1, '3', '客户暂无消费意向', '2025-12-27 02:54:21', 1, '2025-12-27 02:54:21');
INSERT INTO `customer_tracking` VALUES (2, 1, 1, '2', '客户最近出国旅游', '2025-12-27 03:06:48', 1, '2025-12-27 03:06:48');
INSERT INTO `customer_tracking` VALUES (3, 1, 1, '3', '客户最近被限制高消费', '2025-12-27 03:07:19', 1, '2025-12-27 03:07:19');
INSERT INTO `customer_tracking` VALUES (4, 2, 1, '1', '客户最近比较忙', '2025-12-27 04:26:41', 1, '2025-12-27 04:26:41');
INSERT INTO `customer_tracking` VALUES (5, 2, 1, '2', '客户最近肚子疼', '2025-12-27 04:27:44', 1, '2025-12-27 04:27:44');
INSERT INTO `customer_tracking` VALUES (6, 7, 1, '2', '电话未接通', '2025-12-30 01:32:04', 0, '2025-12-30 01:32:04');
INSERT INTO `customer_tracking` VALUES (7, 3, 1, '3', '鸡蛋里并没有放葱', '2025-12-30 03:12:57', 1, '2025-12-30 03:12:57');

-- ----------------------------
-- Table structure for department
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '部门编号',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '部门名称',
  `parent_id` int UNSIGNED NULL DEFAULT NULL COMMENT '上级部门id',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '部门描述',
  `manager_id` int UNSIGNED NULL DEFAULT NULL COMMENT '部门负责人的员工编号(外键)',
  `status` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '部门状态',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `department_name`(`name` ASC) USING BTREE,
  INDEX `manager_id`(`manager_id` ASC) USING BTREE,
  CONSTRAINT `manager_id` FOREIGN KEY (`manager_id`) REFERENCES `employee` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '部门表---企业组织架构核心数据表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of department
-- ----------------------------
INSERT INTO `department` VALUES (1, '总裁办公室', NULL, '总裁办公室', 1, 1, '2025-12-22 01:36:56');
INSERT INTO `department` VALUES (2, '人力资源部', NULL, '人力资源部', 2, 1, '2025-12-22 01:37:10');
INSERT INTO `department` VALUES (3, '人事行政部', 2, '人事行政部', 17, 1, '2025-12-22 01:37:40');
INSERT INTO `department` VALUES (4, '财务总部', NULL, '主管公司财务', 6, 1, '2025-12-23 00:58:16');
INSERT INTO `department` VALUES (5, '财务一部', 4, '财务一部', 1, 1, '2025-12-23 00:58:52');
INSERT INTO `department` VALUES (6, '法务部', NULL, '专门处理法律问题', 3, 1, '2025-12-23 12:47:13');
INSERT INTO `department` VALUES (7, '劳动纠纷部', 6, '专门处理劳动纠纷', 18, 1, '2025-12-23 12:48:11');

-- ----------------------------
-- Table structure for employee
-- ----------------------------
DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '员工id',
  `user_id` int UNSIGNED NULL DEFAULT NULL COMMENT '用户id',
  `department_id` int UNSIGNED NULL DEFAULT NULL COMMENT '部门id',
  `position_id` int UNSIGNED NULL DEFAULT NULL COMMENT '职位id(外键)',
  `work_no` int(6) UNSIGNED ZEROFILL NULL DEFAULT NULL COMMENT '工号',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '员工真实姓名',
  `photo` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '员工照片',
  `phone` char(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号码',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '电子邮箱',
  `gender` enum('male','female') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'male' COMMENT '性别',
  `birthday` date NULL DEFAULT NULL COMMENT '出生年月日',
  `education` enum('1','2','3','4','5') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '3' COMMENT '学历 1-高中以下 2-专科 3-本科 4-硕士 5-博士',
  `school` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '毕业院校',
  `major` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '主修专业',
  `province` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '省份',
  `city` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '城市',
  `county` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '区县',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '详细地址',
  `is_manager` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '是否为部门主管 0-否 1是',
  `status` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '员工状态 0 离职 2在职',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `emp_phone`(`phone` ASC) USING BTREE,
  UNIQUE INDEX `emp_email`(`email` ASC) USING BTREE,
  UNIQUE INDEX `emp_user_id`(`user_id` ASC) USING BTREE,
  INDEX `position_id`(`position_id` ASC) USING BTREE,
  INDEX `emp_department_id`(`department_id` ASC) USING BTREE,
  CONSTRAINT `emp_department_id` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `position_id` FOREIGN KEY (`position_id`) REFERENCES `position` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '员工表---企业组织架构核心表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of employee
-- ----------------------------
INSERT INTO `employee` VALUES (1, 1, 1, 4, 000001, '张三', 'uploads/avatar/08_r7r5I2p.webp', '13800000108', '13800000109@11.com', 'male', '2025-12-22', '1', '清华大学', '水利工程', '北京市', '市辖区', '海淀区', '后厂村', 1, 1, '2025-12-26 10:01:08', '2025-12-22 02:09:09');
INSERT INTO `employee` VALUES (2, 2, 2, 5, 000002, '李斯', 'uploads/avatar/27_SBd3p8Q.webp', '13800000110', '13800000110@gmail.com', 'male', '2025-12-22', '5', '清华大学', '水利工程', '陕西省', '西安市', '未央区', '凤城四路', 1, 1, '2025-12-25 12:31:21', '2025-12-22 02:12:41');
INSERT INTO `employee` VALUES (3, 3, 1, 2, 000003, '王五', 'uploads/avatar/03.webp', '13800000111', '13800000111@qq.com', 'male', '2025-12-22', '1', '清华大学', '水利工程', '广东省', '广州市', '南沙区', '英东大道', 1, 1, '2025-12-24 04:43:09', '2025-12-22 02:14:06');
INSERT INTO `employee` VALUES (4, 4, 1, 1, 000004, '风清扬', 'uploads/avatar/01_2DwZC44.png', '13800000112', '13800000111@126.com', 'male', '2025-12-22', '2', '杭州师范大学', '英语', '浙江省', '杭州市', '余杭区', '西湖路', 0, 1, '2025-12-23 09:02:50', '2025-12-22 03:07:59');
INSERT INTO `employee` VALUES (5, 7, 1, 1, 000005, '零零五', 'uploads/avatar/01_4Kcsd9f.png', '13800000113', '13800000113@126.com', 'male', '2025-12-22', '2', '杭州师范大学', '英语', '浙江省', '杭州市', '余杭区', '西湖路', 0, 1, '2025-12-23 09:03:04', '2025-12-22 05:42:10');
INSERT INTO `employee` VALUES (6, 13, 1, 1, 000006, '赵六', 'uploads/avatar/03_WmtMltH.webp', '13800000114', '13800000114@126.com', 'male', '2025-12-22', '1', '杭州师范大学', '英语', '浙江省', '杭州市', '余杭区', '西湖路', 0, 1, '2025-12-23 09:03:14', '2025-12-22 05:43:48');
INSERT INTO `employee` VALUES (7, 10, 1, 1, 000007, '杰克', 'uploads/avatar/08.webp', '13800000115', '13800000115@126.com', 'male', '2025-12-22', '2', '杭州师范大学', '法语', '浙江省', '杭州市', '余杭区', '西湖路', 0, 1, '2025-12-23 09:03:24', '2025-12-22 05:45:55');
INSERT INTO `employee` VALUES (8, 11, 1, 1, 000008, '张勇', 'uploads/avatar/02_7nCNVJe.webp', '13800000116', '13800000116@126.com', 'male', '2025-12-22', '1', '杭州师范大学', '法语', '浙江省', '杭州市', '余杭区', '西湖路', 0, 1, '2025-12-23 09:12:52', '2025-12-22 05:47:34');
INSERT INTO `employee` VALUES (9, 12, 1, 2, 000009, '逍遥子', 'uploads/avatar/31.webp', '13800000117', '13800000117@126.com', 'male', '2025-12-22', '4', '中央财经大学', '金融管理', '内蒙古自治区', '乌海市', '乌达区', '中山南路', 0, 1, '2025-12-23 11:45:33', '2025-12-22 06:13:30');
INSERT INTO `employee` VALUES (10, NULL, 1, 3, 000010, '娄嘉怡', 'uploads/avatar/16.jpg', '13800000118', '13800000118@126.com', 'female', '1990-12-01', '3', '中央戏剧学院', '导演', '湖北省', '襄阳市', '谷城县', '人民路', NULL, 1, '2025-12-23 09:02:19', '2025-12-22 08:55:43');
INSERT INTO `employee` VALUES (11, NULL, 2, 4, 000011, '丁元英', 'uploads/avatar/21.webp', '13800000119', '13800000120@126.com', 'female', '1970-12-22', '4', '中央财经学院', '考古', '天津市', '市辖区', '河西区', '大草原101号蒙古包', NULL, 1, '2025-12-24 03:46:57', '2025-12-22 09:00:28');
INSERT INTO `employee` VALUES (12, 19, 1, 1, 000012, '任我行', 'uploads/avatar/33.jpg', '13800000121', '13800000121@qq.com', 'male', '2025-12-22', '4', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2025-12-22 17:02:41', '2025-12-22 09:02:41');
INSERT INTO `employee` VALUES (13, 20, 2, 3, 000013, '芮小丹', 'uploads/avatar/04.webp', '13800000122', '13800000122@126.com', 'female', '2025-12-22', '3', '中国人民大学', '历史', '北京市', '市辖区', '东城区', '东城区工人体育馆', 0, 1, '2025-12-22 19:14:25', '2025-12-22 11:14:26');
INSERT INTO `employee` VALUES (14, 21, 3, 3, 000014, '叶子枫', 'uploads/avatar/31_lhHSFt9.webp', '13800000123', '13800000123@qq.com', 'female', '1970-12-22', '3', '中国传媒大学', '播音主持', '河北省', '秦皇岛市', '海港区', '人民路100号街心花园', 0, 1, '2025-12-22 14:53:38', '2025-12-22 11:16:48');
INSERT INTO `employee` VALUES (15, 22, 3, 1, 000015, '孙东旭', 'uploads/avatar/35.jpg', '13800000124', '13800000124@126.com', 'male', '1980-12-22', '4', '中国财经大学', '金融', '山西省', '太原市', '小店区', '人民路101号', 0, 1, '2025-12-22 14:48:27', '2025-12-22 11:19:19');
INSERT INTO `employee` VALUES (16, 23, 1, 1, 000016, '钱多多', 'uploads/avatar/06_EtdHAaB.webp', '13800000125', '13800000125@qq.com', 'female', '2025-12-23', '2', '杭州师范学院', '英语', '江苏省', '南京市', '玄武区', '中山南路', NULL, 1, '2025-12-23 14:42:45', '2025-12-23 06:42:46');
INSERT INTO `employee` VALUES (17, NULL, 4, 5, 000017, '李思思', 'uploads/avatar/15.jpg', '13800000126', '13800000126@126.com', 'female', '2025-12-07', '5', '中国传媒大学', '播音主持', '河北省', '石家庄市', '长安区', '人民路', NULL, 1, '2025-12-24 03:52:49', '2025-12-23 07:02:45');
INSERT INTO `employee` VALUES (18, 24, 7, 5, 000018, '李清照', 'uploads/avatar/23.jpg', '13800000127', '13800000127@qq.com', 'female', '1980-12-25', '4', '中国政法大学', '法律', '河北省', '秦皇岛市', '北戴河区', '中山路', NULL, 1, '2025-12-25 19:47:18', '2025-12-25 11:47:19');

-- ----------------------------
-- Table structure for llm_usage
-- ----------------------------
DROP TABLE IF EXISTS `llm_usage`;
CREATE TABLE `llm_usage`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '账号',
  `employee_id` int NULL DEFAULT NULL COMMENT '员工id(可空,密码登录模式取不到)',
  `session_key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '会话标识:令牌sha1前16位,反推不出令牌',
  `model` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模型',
  `round_no` tinyint NULL DEFAULT 0 COMMENT '循环轮次(第几次请求工具)',
  `prompt_tokens` int UNSIGNED NULL DEFAULT 0 COMMENT '输入token',
  `completion_tokens` int UNSIGNED NULL DEFAULT 0 COMMENT '输出token',
  `cached_tokens` int UNSIGNED NULL DEFAULT 0 COMMENT '缓存命中token',
  `reasoning_tokens` int UNSIGNED NULL DEFAULT 0 COMMENT '思考token',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发生时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_usage_time`(`created_at` ASC) USING BTREE,
  INDEX `idx_usage_user_time`(`username` ASC, `created_at` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '模型调用用量流水(每次请求一行)' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for position
-- ----------------------------
DROP TABLE IF EXISTS `position`;
CREATE TABLE `position`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `department_id` int UNSIGNED NULL DEFAULT NULL COMMENT '部门id',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '职位名称',
  `level` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '职位等级',
  `status` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '职位状态',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `position_name`(`name` ASC) USING BTREE,
  INDEX `department_id`(`department_id` ASC) USING BTREE,
  CONSTRAINT `department_id` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '职位表---企业组织架构核心表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of position
-- ----------------------------
INSERT INTO `position` VALUES (1, NULL, '总裁', 1, 1);
INSERT INTO `position` VALUES (2, NULL, '总经理', 1, 1);
INSERT INTO `position` VALUES (3, NULL, '副总经理', 1, 1);
INSERT INTO `position` VALUES (4, NULL, '主管', 1, 1);
INSERT INTO `position` VALUES (5, NULL, '普通职员', 1, 1);

-- ----------------------------
-- Table structure for product
-- ----------------------------
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `category_id` int UNSIGNED NULL DEFAULT NULL COMMENT '所属分类',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '商品名称',
  `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '商品封面图',
  `price` decimal(10, 2) NULL DEFAULT NULL COMMENT '商品价格',
  `stock_num` int UNSIGNED NULL DEFAULT NULL COMMENT '库存数量',
  `sale_num` int UNSIGNED NULL DEFAULT NULL COMMENT '销量',
  `commission_rate` decimal(10, 2) UNSIGNED NULL DEFAULT NULL COMMENT '销售提成比率',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '商品详情',
  `status` tinyint UNSIGNED NULL DEFAULT NULL COMMENT '商品状态 0 禁用 1-正常',
  `create_time` datetime NULL DEFAULT NULL COMMENT '添加时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `category_id`(`category_id` ASC) USING BTREE,
  CONSTRAINT `category_id` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '商品表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of product
-- ----------------------------
INSERT INTO `product` VALUES (1, 2, '紧致抗皱水光精华素', NULL, 100.00, 10000, 2000, 0.10, '<h3>紧致抗皱水光精华素</h3>', 1, '2025-12-25 11:18:11');
INSERT INTO `product` VALUES (2, 2, '贻贝祛痘水光精华素', NULL, 200.00, 10000, 2000, 0.10, '<h3>贻贝祛痘水光精华素</h3>', 1, '2025-12-25 11:18:11');
INSERT INTO `product` VALUES (3, 2, '三重胶原水光精华素', NULL, 300.00, 10000, 2000, 0.10, '<h3>三重胶原水光精华素</h3>', 1, '2025-12-25 11:18:11');
INSERT INTO `product` VALUES (4, 2, '三文鱼修护水光精华素', NULL, 400.00, 10000, 2000, 0.10, '<h3>三文鱼修护水光精华素</h3>', 1, '2025-12-25 11:18:11');
INSERT INTO `product` VALUES (5, 2, '青春水光精华素', NULL, 500.00, 10000, 2000, 0.10, '<h3>青春水光精华素</h3>', 1, '2025-12-25 11:18:11');
INSERT INTO `product` VALUES (6, 2, '氨甲环酸水光精华素', NULL, 600.00, 10000, 2000, 0.10, '<h3>氨甲环酸水光精华素</h3>', 1, '2025-12-25 11:18:11');
INSERT INTO `product` VALUES (7, 2, '玻尿酸水光精华素', 'product/17.jpg', 700.00, 10000, 2000, 0.10, '<h3>玻尿酸水光精华素</h3><p><img src=\"/media/editor/1767230507.186354.jpg\" alt=\"\" data-href=\"\" style=\"\"/></p>', 1, '2025-12-25 11:18:11');
INSERT INTO `product` VALUES (8, 30, '蛋白粉', 'product/29.jpg', 100.00, 100, 200, 0.10, '<p><span style=\"font-size: 48px;\"><strong>商品介绍</strong></span><span style=\"font-size: 48px;\">商品介绍商品介绍商品介绍商品介绍</span></p><p><img src=\"/media/editor/1767229904.930764.jpg\" alt=\"\" data-href=\"\" style=\"\"/></p>', 1, '2025-12-31 07:05:56');
INSERT INTO `product` VALUES (9, 2, '‌铂金三文鱼', 'product/03.webp', 137.00, 10000, 100, 0.10, '<p><span style=\"color: rgb(51, 51, 51); background-color: rgb(255, 255, 255); font-size: 48px;\">‌</span><span style=\"color: rgb(51, 51, 51); font-size: 48px;\"><strong>铂金三文鱼</strong></span></p><p><span style=\"color: rgb(51, 51, 51); background-color: rgb(255, 255, 255); font-size: 40px;\">PDRN成分强化敏感肌修复能力</span></p>', 1, '2026-01-02 08:41:41');
INSERT INTO `product` VALUES (10, 2, '碧寇家居水光1号', 'product/10.jpeg', 247.00, 2000, 200, 0.10, '<p><span style=\"font-size: 48px;\">碧寇家居水光1号</span></p>', 1, '2026-01-02 08:43:35');
INSERT INTO `product` VALUES (11, 2, '热玛吉微电流多态注氧水光', 'product/12.jpeg', 130.00, 10000, 200, 0.10, '<p><span style=\"font-size: 48px;\">热玛吉微电流多态注氧水光</span></p>', 1, '2026-01-02 08:45:16');
INSERT INTO `product` VALUES (12, 2, '华熙生物水光动能素', 'product/18.jpg', 137.00, 3000, 1000, 0.10, '<p><span style=\"font-size: 48px;\">华熙生物水光动能素</span></p>', 1, '2026-01-02 08:46:49');

-- ----------------------------
-- Table structure for sale_order
-- ----------------------------
DROP TABLE IF EXISTS `sale_order`;
CREATE TABLE `sale_order`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `customer_id` int UNSIGNED NULL DEFAULT NULL COMMENT '顾客id',
  `order_no` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '订单编号',
  `user_id` int UNSIGNED NULL DEFAULT NULL COMMENT '销售人员user_id',
  `amount` decimal(10, 2) UNSIGNED NULL DEFAULT NULL COMMENT '订单金额',
  `commission` decimal(10, 2) UNSIGNED NULL DEFAULT NULL COMMENT '提成金额',
  `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '销售单据照片',
  `status` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '订单状态 0-取消 1-正常',
  `pay_order_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '支付单号',
  `pay_status` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '支付状态',
  `pay_way` enum('wxpay','alipay','bank','cash') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '支付方式 wxpay-微信支付 alipay-支付宝 bank-转账 cash-现金',
  `pay_time` datetime NULL DEFAULT NULL COMMENT '支付时间',
  `express_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '快递单号',
  `express_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '快递公司名称',
  `express_status` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '快递状 0未发货1已发货',
  `consignee` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '收货人',
  `phone` char(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '联系电话',
  `province` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '省份',
  `city` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '城市',
  `county` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '区县',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '详细地址',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `order_no`(`order_no` ASC) USING BTREE COMMENT '订单编号',
  INDEX `customer_id`(`customer_id` ASC) USING BTREE COMMENT '客户id',
  INDEX `biz_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `biz_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '客户订单表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sale_order
-- ----------------------------
INSERT INTO `sale_order` VALUES (1, 1, 'order_001', 1, 1000.00, 100.00, NULL, 1, NULL, 1, 'alipay', NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, '2026-01-02 16:02:32', '2025-12-12 23:29:49');
INSERT INTO `sale_order` VALUES (2, 4, 'order_002', 2, 2000.00, 200.00, NULL, 1, NULL, 1, 'wxpay', NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, '2026-01-02 16:02:31', '2025-12-13 14:38:05');
INSERT INTO `sale_order` VALUES (3, 1, 'order_003', 3, 10000.00, 1000.00, NULL, 1, NULL, 1, 'bank', NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, '2026-01-02 16:02:30', '2025-12-13 15:00:36');
INSERT INTO `sale_order` VALUES (5, 1, '202601011447297326', 1, 2200.00, 220.00, NULL, 1, NULL, 1, 'wxpay', NULL, 'SF2012601021016', '顺丰快递', 1, '韩楚风', '13800000001', '北京市', '市辖区', '海淀区', '清华路', '2026-01-02 11:19:45', '2026-01-01 06:47:30');
INSERT INTO `sale_order` VALUES (6, 5, '202601021651197585', 1, 1067.00, 106.70, NULL, 1, NULL, 1, 'wxpay', NULL, NULL, NULL, 0, '李白', '13800000005', '', '', '', '人民路', '2026-01-02 16:51:19', '2026-01-02 08:51:19');
INSERT INTO `sale_order` VALUES (7, 6, '202601021656154492', 1, 1067.00, 106.70, NULL, 1, NULL, 1, 'bank', NULL, NULL, NULL, 0, '杜甫', '13800000006', '山西省', '太原市', '小店区', '人民路', '2026-01-03 16:56:15', '2026-01-02 08:56:15');
INSERT INTO `sale_order` VALUES (8, 7, '202601021657034650', 1, 1067.00, 106.70, NULL, 1, NULL, 1, 'cash', NULL, NULL, NULL, 0, '杨万里', '13800000007', '内蒙古自治区', '乌海市', '海南区', '大草原', '2026-01-04 16:57:03', '2026-01-02 08:57:03');
INSERT INTO `sale_order` VALUES (9, 5, '202601021657555249', 1, 384.00, 38.40, NULL, 1, NULL, 1, 'bank', NULL, NULL, NULL, 0, '李白', '13800000005', '河北省', '石家庄市', '长安区', '人民路', '2026-01-05 16:57:55', '2026-01-02 08:57:55');
INSERT INTO `sale_order` VALUES (10, 9, '202601051322186205', 1, 267.00, 26.70, NULL, 1, NULL, 1, 'wxpay', NULL, NULL, NULL, 0, '彭璐', '13800000009', '中山', '中山', '乐丰六路219号', '乐丰六路219号', '2026-01-05 14:18:51', '2026-01-05 05:22:19');
INSERT INTO `sale_order` VALUES (11, 15, '202601051325286131', 1, 1200.00, 120.00, NULL, 1, NULL, 1, 'wxpay', NULL, NULL, NULL, 0, '雷子韬', '13800000015', '上海市', '上海市', '黄浦区淮海中路328号', '黄浦区淮海中路328号', '2026-01-05 14:18:53', '2026-01-05 05:25:28');
INSERT INTO `sale_order` VALUES (12, 28, '202601051424125631', 1, 747.00, 74.70, NULL, 1, NULL, 1, 'wxpay', NULL, NULL, NULL, 0, '武子韬', '13800000028', '东莞', '东莞', '坑美十五巷598号', '坑美十五巷598号', '2026-01-05 14:25:20', '2026-01-05 06:24:13');
INSERT INTO `sale_order` VALUES (13, 90, '202601051424435020', 1, 437.00, 43.70, NULL, 1, NULL, 1, 'wxpay', NULL, NULL, NULL, 0, '廖子异', '13800000090', '深圳', '深圳', '龙岗区学园一巷115号', '龙岗区学园一巷115号', '2026-01-05 14:25:21', '2026-01-05 06:24:43');

-- ----------------------------
-- Table structure for sale_order_item
-- ----------------------------
DROP TABLE IF EXISTS `sale_order_item`;
CREATE TABLE `sale_order_item`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `order_id` int UNSIGNED NULL DEFAULT NULL COMMENT '订单id',
  `product_id` int UNSIGNED NULL DEFAULT NULL COMMENT '产品id',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '商品名称',
  `num` int UNSIGNED NULL DEFAULT NULL COMMENT '商品数量',
  `price` decimal(10, 2) UNSIGNED NULL DEFAULT NULL COMMENT '商品价格',
  `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '商品图片',
  `commission_rate` decimal(10, 2) UNSIGNED NULL DEFAULT NULL COMMENT '提成比率',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `order_id`(`order_id` ASC) USING BTREE,
  CONSTRAINT `order_id` FOREIGN KEY (`order_id`) REFERENCES `sale_order` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '订单商品表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sale_order_item
-- ----------------------------
INSERT INTO `sale_order_item` VALUES (1, 5, 1, '紧致抗皱水光精华素', 4, 100.00, NULL, 0.10);
INSERT INTO `sale_order_item` VALUES (2, 5, 2, '贻贝祛痘水光精华素', 4, 200.00, NULL, 0.10);
INSERT INTO `sale_order_item` VALUES (3, 5, 3, '三重胶原水光精华素', 3, 300.00, NULL, 0.10);
INSERT INTO `sale_order_item` VALUES (4, 5, 8, '蛋白粉', 1, 100.00, 'http://localhost:5173/media/product/29.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (5, 6, 8, '蛋白粉', 1, 100.00, 'http://localhost:5173/media/product/29.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (6, 6, 7, '玻尿酸水光精华素', 1, 700.00, 'http://localhost:5173/media/product/17.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (7, 6, 11, '热玛吉微电流多态注氧水光', 1, 130.00, 'http://localhost:5173/media/product/12.jpeg', 0.10);
INSERT INTO `sale_order_item` VALUES (8, 6, 12, '华熙生物水光动能素', 1, 137.00, 'http://localhost:5173/media/product/18.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (9, 7, 8, '蛋白粉', 1, 100.00, 'http://localhost:5173/media/product/29.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (10, 7, 7, '玻尿酸水光精华素', 1, 700.00, 'http://localhost:5173/media/product/17.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (11, 7, 11, '热玛吉微电流多态注氧水光', 1, 130.00, 'http://localhost:5173/media/product/12.jpeg', 0.10);
INSERT INTO `sale_order_item` VALUES (12, 7, 12, '华熙生物水光动能素', 1, 137.00, 'http://localhost:5173/media/product/18.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (13, 8, 8, '蛋白粉', 1, 100.00, 'http://localhost:5173/media/product/29.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (14, 8, 7, '玻尿酸水光精华素', 1, 700.00, 'http://localhost:5173/media/product/17.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (15, 8, 11, '热玛吉微电流多态注氧水光', 1, 130.00, 'http://localhost:5173/media/product/12.jpeg', 0.10);
INSERT INTO `sale_order_item` VALUES (16, 8, 12, '华熙生物水光动能素', 1, 137.00, 'http://localhost:5173/media/product/18.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (17, 9, 9, '‌铂金三文鱼', 1, 137.00, 'http://localhost:5173/media/product/03.webp', 0.10);
INSERT INTO `sale_order_item` VALUES (18, 9, 10, '碧寇家居水光1号', 1, 247.00, 'http://localhost:5173/media/product/10.jpeg', 0.10);
INSERT INTO `sale_order_item` VALUES (19, 10, 11, '热玛吉微电流多态注氧水光', 1, 130.00, 'http://localhost:5173/media/product/12.jpeg', 0.10);
INSERT INTO `sale_order_item` VALUES (20, 10, 12, '华熙生物水光动能素', 1, 137.00, 'http://localhost:5173/media/product/18.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (21, 11, 5, '青春水光精华素', 1, 500.00, NULL, 0.10);
INSERT INTO `sale_order_item` VALUES (22, 11, 7, '玻尿酸水光精华素', 1, 700.00, 'http://localhost:5173/media/product/17.jpg', 0.10);
INSERT INTO `sale_order_item` VALUES (23, 12, 5, '青春水光精华素', 1, 500.00, NULL, 0.10);
INSERT INTO `sale_order_item` VALUES (24, 12, 10, '碧寇家居水光1号', 1, 247.00, 'http://localhost:5173/media/product/10.jpeg', 0.10);
INSERT INTO `sale_order_item` VALUES (25, 13, 3, '三重胶原水光精华素', 1, 300.00, NULL, 0.10);
INSERT INTO `sale_order_item` VALUES (26, 13, 9, '‌铂金三文鱼', 1, 137.00, 'http://localhost:5173/media/product/03.webp', 0.10);

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单标题',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '前端路由地址',
  `parent_id` tinyint NULL DEFAULT NULL COMMENT '父级id',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单图标',
  `sort_order` tinyint NULL DEFAULT 0 COMMENT '排序',
  `permission_id` int UNSIGNED NULL DEFAULT NULL COMMENT '权限id',
  `permission_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单权限编码',
  `menu_type` enum('dir','nav','link','btn') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'nav' COMMENT '菜单类型(dir目录/nav导航/link链接/btn按钮)',
  `status` tinyint NULL DEFAULT 1 COMMENT '状态 0-禁用 1-启用',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `m_per_id`(`permission_code` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 68 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '菜单表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_menu
-- ----------------------------
INSERT INTO `sys_menu` VALUES (1, '系统管理', NULL, NULL, 'Setting', 1, 1, NULL, 'dir', 1, '2025-11-17 10:57:09', '2025-12-17 14:50:54');
INSERT INTO `sys_menu` VALUES (2, '权限管理', '/permission', 1, NULL, 1, 5, 'api:permission:list', 'nav', 1, '2025-11-17 10:57:35', '2025-12-18 06:22:53');
INSERT INTO `sys_menu` VALUES (3, '菜单管理', '/menu', 1, NULL, 3, 15, 'api:menu:list', 'nav', 1, '2025-11-17 10:57:49', '2025-12-18 06:23:15');
INSERT INTO `sys_menu` VALUES (4, '角色管理', '/role', 1, NULL, 2, 10, 'api:role:list', 'nav', 1, '2025-11-17 11:00:40', '2025-12-18 06:23:11');
INSERT INTO `sys_menu` VALUES (5, '账号管理', '/user', 1, NULL, 4, 20, 'api:user:list', 'nav', 1, '2025-11-17 11:01:18', '2025-12-19 06:51:46');
INSERT INTO `sys_menu` VALUES (6, '商城管理', '', NULL, 'Goods', 4, NULL, NULL, 'dir', 1, '2025-11-17 14:15:20', '2025-12-31 03:58:46');
INSERT INTO `sys_menu` VALUES (7, '商品管理', '/product', 6, '', 2, 74, 'api:product:list', 'nav', 1, '2025-11-17 14:16:40', '2025-12-31 06:05:01');
INSERT INTO `sys_menu` VALUES (8, '分类管理', '/category', 6, '', 1, 68, 'api:category:list', 'nav', 1, '2025-11-17 14:23:09', '2025-12-31 03:59:40');
INSERT INTO `sys_menu` VALUES (9, '订单管理', '', NULL, 'Setting', 5, NULL, NULL, 'dir', 1, '2025-11-17 14:31:00', '2026-01-02 16:18:59');
INSERT INTO `sys_menu` VALUES (10, '新增权限', NULL, 2, NULL, 0, 7, 'api:permission:create', 'btn', 1, '2025-12-05 16:35:51', '2025-12-11 05:28:07');
INSERT INTO `sys_menu` VALUES (12, '更新权限', '', 2, '', 0, 8, 'api:permission:update', 'btn', 1, '2025-12-07 10:26:27', '2025-12-07 10:26:27');
INSERT INTO `sys_menu` VALUES (13, '删除权限', '', 2, '', 0, 9, 'api:permission:destroy', 'btn', 1, '2025-12-07 10:26:47', '2025-12-07 10:26:47');
INSERT INTO `sys_menu` VALUES (14, '新增菜单', '', 3, '', 0, 12, 'api:menu:create', 'btn', 1, '2025-12-07 11:08:20', '2025-12-17 22:26:01');
INSERT INTO `sys_menu` VALUES (15, '更新菜单', '', 3, '', 0, 18, 'api:menu:update', 'btn', 1, '2025-12-07 11:08:39', '2025-12-07 11:08:39');
INSERT INTO `sys_menu` VALUES (16, '删除菜单', '', 3, '', 0, 19, 'api:menu:destroy', 'btn', 1, '2025-12-07 11:08:54', '2025-12-07 11:08:54');
INSERT INTO `sys_menu` VALUES (17, '新增角色', '', 4, '', 0, 12, 'api:role:create', 'btn', 1, '2025-12-07 11:09:31', '2025-12-07 11:13:00');
INSERT INTO `sys_menu` VALUES (18, '更新角色', '', 4, '', 0, 13, 'api:role:update', 'btn', 1, '2025-12-07 11:09:50', '2025-12-07 11:09:50');
INSERT INTO `sys_menu` VALUES (19, '删除角色', '', 4, '', 0, 14, 'api:role:destroy', 'btn', 1, '2025-12-07 11:10:02', '2025-12-07 11:10:02');
INSERT INTO `sys_menu` VALUES (20, '新增账号', '', 5, '', 0, 22, 'api:user:create', 'btn', 1, '2025-12-07 11:10:20', '2025-12-07 11:10:20');
INSERT INTO `sys_menu` VALUES (21, '更新账号', '', 5, '', 0, 23, 'api:user:update', 'btn', 1, '2025-12-07 11:10:38', '2025-12-07 11:10:38');
INSERT INTO `sys_menu` VALUES (22, '删除账号', '', 5, '', 0, 24, 'api:user:destroy', 'btn', 1, '2025-12-07 11:10:54', '2025-12-07 11:10:54');
INSERT INTO `sys_menu` VALUES (23, '组织架构', '', NULL, 'User', 2, 5, '', 'dir', 1, '2025-12-18 01:48:23', '2026-01-02 16:19:39');
INSERT INTO `sys_menu` VALUES (24, '客户管理', '', NULL, 'Goods', 3, NULL, NULL, 'dir', 1, '2025-12-18 02:02:08', '2025-12-31 03:58:50');
INSERT INTO `sys_menu` VALUES (26, '部门管理', '/department', 23, '', 1, 33, 'api:department:list', 'nav', 1, '2025-12-18 03:09:05', '2025-12-22 07:01:17');
INSERT INTO `sys_menu` VALUES (27, '职位管理', '/position', 23, '', 2, 38, 'api:position:list', 'nav', 1, '2025-12-18 03:12:39', '2025-12-22 07:04:56');
INSERT INTO `sys_menu` VALUES (28, '员工管理', '/employee', 23, '', 3, 43, 'api:employee:list', 'nav', 1, '2025-12-18 03:46:33', '2025-12-22 07:05:05');
INSERT INTO `sys_menu` VALUES (30, '员工详情', '/empDetail/:id', 28, '', 0, 47, 'api:employee:detail', 'link', 1, '2025-12-22 07:59:09', '2025-12-26 02:23:58');
INSERT INTO `sys_menu` VALUES (31, '部门员工', '/departmentEmp/:id', 26, '', 1, 43, 'api:employee:list', 'link', 1, '2025-12-25 06:43:00', '2025-12-25 06:43:00');
INSERT INTO `sys_menu` VALUES (32, '新增部门', '', 26, '', 1, 34, 'api:department:create', 'btn', 1, '2025-12-26 02:14:14', '2025-12-26 02:14:14');
INSERT INTO `sys_menu` VALUES (33, '编辑部门', '', 26, '', 2, 35, 'api:department:update', 'btn', 1, '2025-12-26 02:14:36', '2025-12-26 02:14:36');
INSERT INTO `sys_menu` VALUES (34, '删除部门', '', 26, '', 3, 36, 'api:department:destroy', 'btn', 1, '2025-12-26 02:14:57', '2025-12-26 02:14:57');
INSERT INTO `sys_menu` VALUES (35, '新增员工', '', 28, '', 1, 44, 'api:employee:create', 'btn', 1, '2025-12-26 02:15:20', '2025-12-26 02:15:20');
INSERT INTO `sys_menu` VALUES (36, '编辑员工', '', 28, '', 3, 45, 'api:employee:update', 'btn', 1, '2025-12-26 02:15:44', '2025-12-26 02:15:44');
INSERT INTO `sys_menu` VALUES (37, '删除员工', '', 28, '', 4, 46, 'api:employee:destroy', 'btn', 1, '2025-12-26 02:16:01', '2025-12-26 02:16:01');
INSERT INTO `sys_menu` VALUES (38, '新增职位', '', 27, '', 1, 39, 'api:position:create', 'btn', 1, '2025-12-26 02:18:43', '2025-12-26 02:20:04');
INSERT INTO `sys_menu` VALUES (39, '编辑职位', '', 27, '', 2, 40, 'api:position:update', 'btn', 1, '2025-12-26 02:19:01', '2025-12-26 02:20:09');
INSERT INTO `sys_menu` VALUES (40, '删除职位', '', 27, '', 3, 41, 'api:position:destroy', 'btn', 1, '2025-12-26 02:19:19', '2025-12-26 02:20:14');
INSERT INTO `sys_menu` VALUES (41, '客户来源管理', '/customerSource', 24, '', 1, 49, 'api:customer_source:list', 'nav', 1, '2025-12-29 00:39:28', '2025-12-30 00:35:47');
INSERT INTO `sys_menu` VALUES (42, '客户信息管理', '/customer', 24, '', 2, 54, 'api:customer', 'nav', 1, '2025-12-29 00:39:58', '2026-01-02 08:07:18');
INSERT INTO `sys_menu` VALUES (43, '客户跟踪记录', '/customerTracking', 24, '', 3, 59, 'api:customer_tracking:list', 'nav', 1, '2025-12-29 00:40:24', '2025-12-30 00:35:54');
INSERT INTO `sys_menu` VALUES (44, '客户详情', '/customerDetail/:id', 42, '', 1, 58, 'api:customer:detail', 'link', 1, '2025-12-29 06:09:36', '2026-01-02 08:18:17');
INSERT INTO `sys_menu` VALUES (45, '单个客户跟踪记录', '/customer/:id/tracking', 24, '', 1, 66, 'api:customer_tracking:list', 'link', 1, '2025-12-30 01:57:22', '2025-12-30 09:08:31');
INSERT INTO `sys_menu` VALUES (46, '我的客户', '/customerOfMe', 24, '', 4, 64, 'api:customer:of_me', 'nav', 1, '2025-12-30 05:53:25', '2025-12-30 09:04:20');
INSERT INTO `sys_menu` VALUES (47, '新增来源', '', 41, '', 1, 50, 'api:customer_source:create', 'btn', 1, '2025-12-31 03:50:22', '2025-12-31 03:50:22');
INSERT INTO `sys_menu` VALUES (48, '更新来源', '', 41, '', 2, 51, 'api:customer_source:update', 'btn', 1, '2025-12-31 03:50:38', '2025-12-31 03:50:38');
INSERT INTO `sys_menu` VALUES (49, '删除来源', '', 41, '', 3, 52, 'api:customer_source:destroy', 'btn', 1, '2025-12-31 03:50:58', '2025-12-31 03:50:58');
INSERT INTO `sys_menu` VALUES (50, '新增客户', '', 42, '', 1, 55, 'api:customer:create', 'btn', 1, '2025-12-31 03:51:19', '2025-12-31 03:51:19');
INSERT INTO `sys_menu` VALUES (51, '更新客户', '', 42, '', 2, 56, 'api:customer:update', 'btn', 1, '2025-12-31 03:51:50', '2025-12-31 03:51:50');
INSERT INTO `sys_menu` VALUES (52, '删除客户', '', 42, '', 3, 57, 'api:customer:destroy', 'btn', 1, '2025-12-31 03:52:07', '2025-12-31 03:52:07');
INSERT INTO `sys_menu` VALUES (53, '新增记录', '', 43, '', 1, 60, 'api:customer_tracking:create', 'btn', 1, '2025-12-31 03:53:35', '2025-12-31 03:53:35');
INSERT INTO `sys_menu` VALUES (54, '更新记录', '', 43, '', 2, 61, 'api:customer_tracking:update', 'btn', 1, '2025-12-31 03:53:51', '2025-12-31 03:53:51');
INSERT INTO `sys_menu` VALUES (55, '删除记录', '', 43, '', 3, 62, 'api:customer_tracking:destroy', 'btn', 1, '2025-12-31 03:54:04', '2025-12-31 03:54:04');
INSERT INTO `sys_menu` VALUES (56, '销售订单', '/saleOrder', 9, 'Setting', 1, 80, 'api:sale_order:list', 'nav', 1, '2026-01-02 00:35:26', '2026-01-02 00:43:28');
INSERT INTO `sys_menu` VALUES (57, '新增销售订单', '/orderCreate', 56, '', 1, 81, 'api:sale_order:create', 'link', 1, '2026-01-02 00:37:50', '2026-01-02 00:40:52');
INSERT INTO `sys_menu` VALUES (58, '更新销售订单', '', 56, '', 1, 82, 'api:sale_order:update', 'btn', 1, '2026-01-02 00:38:11', '2026-01-02 00:38:11');
INSERT INTO `sys_menu` VALUES (59, '删除销售订单', '', 56, '', 1, 83, 'api:sale_order:destroy', 'btn', 1, '2026-01-02 00:38:31', '2026-01-02 00:38:31');
INSERT INTO `sys_menu` VALUES (60, '销售订单详情', '', 56, '', 1, 84, 'api:sale_order:detail', 'btn', 1, '2026-01-02 00:38:46', '2026-01-02 00:38:46');
INSERT INTO `sys_menu` VALUES (61, '销售统计', '', NULL, 'Setting', 5, NULL, NULL, 'dir', 1, '2026-01-02 07:37:42', '2026-01-02 07:37:42');
INSERT INTO `sys_menu` VALUES (62, '销售数据统计', '/stat', 61, '', 1, 87, 'api:stat:top_sale_product', 'nav', 1, '2026-01-02 07:38:29', '2026-01-05 07:54:00');
INSERT INTO `sys_menu` VALUES (63, '销售提成管理', '', NULL, 'Goods', 5, NULL, NULL, 'dir', 1, '2026-01-05 15:05:56', '2026-01-05 15:05:56');
INSERT INTO `sys_menu` VALUES (64, '我的销售提成', '/myCommission', 63, '', 2, 90, 'api:commission:of_me', 'nav', 1, '2026-01-05 15:06:54', '2026-01-05 15:09:49');
INSERT INTO `sys_menu` VALUES (65, '员工销售提成', '/commission', 63, '', 1, 89, 'api:commission:list', 'nav', 1, '2026-01-05 15:09:41', '2026-01-05 15:09:41');
INSERT INTO `sys_menu` VALUES (66, '生成当月销售提成', '', 63, '', 1, 91, 'api:commission:create', 'btn', 1, '2026-01-05 15:10:22', '2026-01-05 15:10:22');
INSERT INTO `sys_menu` VALUES (67, 'Tokens 用量', '/llm-usage', 1, 'DataLine', 25, 93, 'api:llm_usage:summary', 'nav', 1, '2026-11-16 21:30:00', '2026-11-16 21:30:00');

-- ----------------------------
-- Table structure for sys_permission
-- ----------------------------
DROP TABLE IF EXISTS `sys_permission`;
CREATE TABLE `sys_permission`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `parent_id` int UNSIGNED NULL DEFAULT NULL COMMENT '上级id',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限名称',
  `code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限编码, 如api:permission:list',
  `url` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '接口地址',
  `method` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '请求方式',
  `status` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '状态: 0-禁用,1-启用',
  `is_public` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '是否默认公开: 0-不公开,1-公开',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 96 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '权限表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_permission
-- ----------------------------
INSERT INTO `sys_permission` VALUES (1, NULL, '权限管理', 'api:permission', '', '', 1, 0);
INSERT INTO `sys_permission` VALUES (2, NULL, '角色管理', 'api:role', '', '', 1, 0);
INSERT INTO `sys_permission` VALUES (3, NULL, '菜单管理', 'api:menu', '', '', 1, 0);
INSERT INTO `sys_permission` VALUES (4, NULL, '账号管理', 'api:user', '', '', 1, 0);
INSERT INTO `sys_permission` VALUES (5, 1, '权限列表', 'api:permission:list', '', '', 1, 1);
INSERT INTO `sys_permission` VALUES (6, 1, '权限详情', 'api:permission:detail', '/permission', 'get', 1, 0);
INSERT INTO `sys_permission` VALUES (7, 1, '新增权限', 'api:permission:create', '/permission', 'get', 1, 0);
INSERT INTO `sys_permission` VALUES (8, 1, '更新权限', 'api:permission:update', '/permission', 'post', 1, 0);
INSERT INTO `sys_permission` VALUES (9, 1, '删除权限', 'api:permission:destroy', '/permission', 'patch', 1, 0);
INSERT INTO `sys_permission` VALUES (10, 2, '角色列表', 'api:role:list', '/role', 'delete', 1, 1);
INSERT INTO `sys_permission` VALUES (11, 2, '角色详情', 'api:role:detail', '/role', 'get', 1, 0);
INSERT INTO `sys_permission` VALUES (12, 2, '新增角色', 'api:role:create', '/role', 'get', 1, 0);
INSERT INTO `sys_permission` VALUES (13, 2, '更新角色', 'api:role:update', '/role', 'post', 1, 0);
INSERT INTO `sys_permission` VALUES (14, 2, '删除角色', 'api:role:destroy', '/role', 'patch', 1, 0);
INSERT INTO `sys_permission` VALUES (15, 3, '菜单列表', 'api:menu:list', '/menu', 'delete', 1, 1);
INSERT INTO `sys_permission` VALUES (16, 3, '菜单详情', 'api:menu:detail', '/menu', 'get', 1, 0);
INSERT INTO `sys_permission` VALUES (17, 3, '新增菜单', 'api:menu:create', '/menu', 'get', 1, 0);
INSERT INTO `sys_permission` VALUES (18, 3, '更新菜单', 'api:menu:update', '/menu', 'post', 1, 0);
INSERT INTO `sys_permission` VALUES (19, 3, '删除菜单', 'api:menu:destroy', '/menu', 'patch', 1, 0);
INSERT INTO `sys_permission` VALUES (20, 4, '账号列表', 'api:user:list', '/user', 'get', 1, 0);
INSERT INTO `sys_permission` VALUES (21, 4, '账号详情', 'api:user:detail', '/user', 'get', 1, 0);
INSERT INTO `sys_permission` VALUES (22, 4, '新增账号', 'api:user:create', '/user', 'post', 1, 0);
INSERT INTO `sys_permission` VALUES (23, 4, '更新账号', 'api:user:update', '/user', 'patch', 1, 0);
INSERT INTO `sys_permission` VALUES (24, 4, '删除账号', 'api:user:destroy', '/user', 'delete', 1, 0);
INSERT INTO `sys_permission` VALUES (25, 25, '部门管理', 'api:department', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (26, NULL, '组织架构', 'api:organization', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (27, 26, '部门管理', 'api:department', '', NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (28, 26, '职位管理', 'api:position', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (29, 26, '员工管理', 'api:employee', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (30, NULL, '工作流管理', 'api:workflow', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (31, 30, '工作流模板管理', 'api:workflow:template', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (32, 30, '工作流节点管理', 'api:workflow:nodes', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (33, 27, '部门列表', 'api:department:list', NULL, NULL, 1, 1);
INSERT INTO `sys_permission` VALUES (34, 27, '新增部门', 'api:department:create', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (35, 27, '更新部门', 'api:department:update', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (36, 27, '删除部门', 'api:department:destroy', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (37, 27, '部门详情', 'api:department:detail', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (38, 28, '职位列表', 'api:position:list', NULL, NULL, 1, 1);
INSERT INTO `sys_permission` VALUES (39, 28, '新增职位', 'api:position:create', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (40, 28, '更新职位', 'api:position:update', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (41, 28, '删除职位', 'api:position:destroy', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (42, 28, '职位详情', 'api:position:detail', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (43, 29, '员工列表', 'api:employee:list', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (44, 29, '新增员工', 'api:employee:create', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (45, 29, '更新员工', 'api:employee:update', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (46, 29, '删除员工', 'api:employee:destroy', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (47, 29, '员工详情', 'api:employee:detail', NULL, NULL, 1, 1);
INSERT INTO `sys_permission` VALUES (48, 54, '客户列表', 'api:customer:list', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (49, NULL, '客户来源管理', 'api:customer_source', NULL, NULL, 1, 1);
INSERT INTO `sys_permission` VALUES (50, 49, '新增客户来源', 'api:customer_source:create', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (51, 49, '更新客户来源', 'api:customer_source:update', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (52, 49, '删除客户来源', 'api:customer_source:destroy', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (53, 49, '客户来源详情', 'api:customer_source:detail', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (54, NULL, '客户信息管理', 'api:customer', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (55, 54, '新增客户', 'api:customer:create', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (56, 54, '更新客户', 'api:customer:update', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (57, 54, '删除客户', 'api:customer:destroy', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (58, 54, '客户详情', 'api:customer:detail', NULL, NULL, 1, 1);
INSERT INTO `sys_permission` VALUES (59, NULL, '客户跟踪记录', 'api:customer_tracking', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (60, 59, '新增客户跟踪记录', 'api:customer_tracking:create', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (61, 59, '更新客户跟踪记录', 'api:customer_tracking:update', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (62, 59, '删除客户跟踪记录', 'api:customer_tracking:destroy', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (63, 59, '客户跟踪记录详情', 'api:customer_tracking:detail', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (64, 54, '我的客户', 'api:customer:of_me', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (65, 49, '客户来源列表', 'api:customer_source:list', NULL, NULL, 1, 1);
INSERT INTO `sys_permission` VALUES (66, 59, '客户跟踪记录列表', 'api:customer_tracking:list', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (67, NULL, '分类管理', 'api:category', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (68, 67, '分类列表', 'api:category:list', NULL, NULL, 1, 1);
INSERT INTO `sys_permission` VALUES (69, 67, '新增分类', 'api:category:create', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (70, 67, '更新分类', 'api:category:update', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (71, 67, '删除分类', 'api:category:destroy', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (72, 67, '分类详情', 'api:category:detail', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (73, NULL, '商品管理', 'api:product', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (74, 73, '商品列表', 'api:product:list', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (75, 73, '新增商品', 'api:product:create', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (76, 73, '更新商品', 'api:product:update', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (77, 73, '删除商品', 'api:product:destroy', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (78, 73, '商品详情', 'api:product:detail', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (79, NULL, '销售订单管理', 'api:sale_order', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (80, 79, '销售订单列表', 'api:sale_order:list', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (81, 79, '新增销售订单', 'api:sale_order:create', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (82, 79, '更新销售订单', 'api:sale_order:update', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (83, 79, '删除销售订单', 'api:sale_order:destroy', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (84, 79, '销售订单详情', 'api:sale_order:detail', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (85, 79, '销售订单商品列表', 'api:sale_order_item:list', NULL, NULL, 1, 1);
INSERT INTO `sys_permission` VALUES (86, NULL, '销售数据统计', 'api:stat', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (87, 86, '热销商品统计', 'api:stat:top_sale_product', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (88, NULL, '销售提成管理', 'api:commission', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (89, 88, '查看所有员工的销售提成', 'api:commission:list', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (90, 88, '我的销售提成', 'api:commission:of_me', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (91, 88, '生成当月销售提成数据', 'api:commission:create', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (92, NULL, 'Tokens用量管理', 'api:llm_usage', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (93, 92, '查看各账号Tokens消耗', 'api:llm_usage:summary', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (94, 92, '查看Tokens消耗明细', 'api:llm_usage:list', NULL, NULL, 1, 0);
INSERT INTO `sys_permission` VALUES (95, NULL, '查询当前登录人', 'api:user:whoami', NULL, NULL, 1, 1);

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色名称',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色说明',
  `status` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '角色状态 1启用 0禁用',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES (1, '超级管理员', '拥有几乎所有的功能权限', 1, '2025-12-29 06:30:17', '2025-10-25 12:05:37');
INSERT INTO `sys_role` VALUES (2, '二级管理员', '拥有账号管理相关权限', 1, '2025-12-30 04:34:17', '2025-10-25 12:05:49');
INSERT INTO `sys_role` VALUES (3, '销售顾问', '查看个人业绩、录单、查看激励', 1, '2026-01-02 08:23:18', '2025-10-25 12:06:14');
INSERT INTO `sys_role` VALUES (4, '华东销售部', '华东销售部', 0, '2025-12-19 06:29:42', '2025-12-03 12:04:24');
INSERT INTO `sys_role` VALUES (5, '华南销售部', NULL, 1, '2025-12-03 13:01:36', '2025-12-03 13:01:36');
INSERT INTO `sys_role` VALUES (6, '中原销售部', NULL, 1, '2025-12-03 13:05:20', '2025-12-03 13:05:20');
INSERT INTO `sys_role` VALUES (7, '粤港澳大湾区销售', NULL, 1, '2025-12-03 13:06:30', '2025-12-03 13:06:30');
INSERT INTO `sys_role` VALUES (8, '江浙销售部', NULL, 1, '2025-12-03 13:07:38', '2025-12-03 13:07:38');
INSERT INTO `sys_role` VALUES (9, '台州销售部', NULL, 1, '2025-12-03 13:08:29', '2025-12-03 13:08:29');
INSERT INTO `sys_role` VALUES (16, '测试角色01', '测试角色01', 1, '2025-12-18 03:24:13', '2025-12-16 12:36:22');

-- ----------------------------
-- Table structure for sys_role_permission
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_permission`;
CREATE TABLE `sys_role_permission`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_id` int UNSIGNED NULL DEFAULT NULL COMMENT '角色id',
  `permission_id` int UNSIGNED NULL DEFAULT NULL COMMENT '权限id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `per_role_id`(`role_id` ASC) USING BTREE,
  INDEX `per_id`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `r_per_id` FOREIGN KEY (`permission_id`) REFERENCES `sys_permission` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `r_role_id` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 293 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色权限表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_role_permission
-- ----------------------------
INSERT INTO `sys_role_permission` VALUES (1, 1, 1);
INSERT INTO `sys_role_permission` VALUES (2, 1, 2);
INSERT INTO `sys_role_permission` VALUES (3, 1, 3);
INSERT INTO `sys_role_permission` VALUES (4, 1, 4);
INSERT INTO `sys_role_permission` VALUES (5, 1, 5);
INSERT INTO `sys_role_permission` VALUES (6, 1, 6);
INSERT INTO `sys_role_permission` VALUES (7, 1, 7);
INSERT INTO `sys_role_permission` VALUES (8, 1, 8);
INSERT INTO `sys_role_permission` VALUES (9, 1, 9);
INSERT INTO `sys_role_permission` VALUES (10, 1, 10);
INSERT INTO `sys_role_permission` VALUES (11, 1, 11);
INSERT INTO `sys_role_permission` VALUES (12, 1, 12);
INSERT INTO `sys_role_permission` VALUES (13, 1, 13);
INSERT INTO `sys_role_permission` VALUES (14, 1, 14);
INSERT INTO `sys_role_permission` VALUES (15, 1, 15);
INSERT INTO `sys_role_permission` VALUES (16, 1, 16);
INSERT INTO `sys_role_permission` VALUES (17, 1, 17);
INSERT INTO `sys_role_permission` VALUES (18, 1, 18);
INSERT INTO `sys_role_permission` VALUES (19, 1, 19);
INSERT INTO `sys_role_permission` VALUES (20, 1, 20);
INSERT INTO `sys_role_permission` VALUES (21, 1, 21);
INSERT INTO `sys_role_permission` VALUES (22, 1, 22);
INSERT INTO `sys_role_permission` VALUES (23, 1, 23);
INSERT INTO `sys_role_permission` VALUES (24, 1, 24);
INSERT INTO `sys_role_permission` VALUES (26, 5, 1);
INSERT INTO `sys_role_permission` VALUES (27, 5, 5);
INSERT INTO `sys_role_permission` VALUES (28, 5, 6);
INSERT INTO `sys_role_permission` VALUES (29, 5, 7);
INSERT INTO `sys_role_permission` VALUES (30, 5, 8);
INSERT INTO `sys_role_permission` VALUES (31, 5, 9);
INSERT INTO `sys_role_permission` VALUES (32, 6, 1);
INSERT INTO `sys_role_permission` VALUES (33, 6, 5);
INSERT INTO `sys_role_permission` VALUES (34, 6, 6);
INSERT INTO `sys_role_permission` VALUES (35, 6, 7);
INSERT INTO `sys_role_permission` VALUES (36, 6, 8);
INSERT INTO `sys_role_permission` VALUES (37, 6, 9);
INSERT INTO `sys_role_permission` VALUES (38, 7, 1);
INSERT INTO `sys_role_permission` VALUES (39, 7, 5);
INSERT INTO `sys_role_permission` VALUES (40, 7, 6);
INSERT INTO `sys_role_permission` VALUES (41, 7, 7);
INSERT INTO `sys_role_permission` VALUES (42, 7, 8);
INSERT INTO `sys_role_permission` VALUES (43, 7, 9);
INSERT INTO `sys_role_permission` VALUES (44, 8, 1);
INSERT INTO `sys_role_permission` VALUES (45, 8, 5);
INSERT INTO `sys_role_permission` VALUES (46, 8, 6);
INSERT INTO `sys_role_permission` VALUES (47, 8, 7);
INSERT INTO `sys_role_permission` VALUES (48, 8, 8);
INSERT INTO `sys_role_permission` VALUES (49, 8, 9);
INSERT INTO `sys_role_permission` VALUES (50, 9, 1);
INSERT INTO `sys_role_permission` VALUES (51, 9, 5);
INSERT INTO `sys_role_permission` VALUES (52, 9, 6);
INSERT INTO `sys_role_permission` VALUES (53, 9, 7);
INSERT INTO `sys_role_permission` VALUES (54, 9, 8);
INSERT INTO `sys_role_permission` VALUES (55, 9, 9);
INSERT INTO `sys_role_permission` VALUES (87, 2, 20);
INSERT INTO `sys_role_permission` VALUES (88, 2, 21);
INSERT INTO `sys_role_permission` VALUES (89, 2, 22);
INSERT INTO `sys_role_permission` VALUES (90, 2, 23);
INSERT INTO `sys_role_permission` VALUES (191, 16, 20);
INSERT INTO `sys_role_permission` VALUES (193, 4, 4);
INSERT INTO `sys_role_permission` VALUES (194, 4, 20);
INSERT INTO `sys_role_permission` VALUES (195, 4, 21);
INSERT INTO `sys_role_permission` VALUES (196, 4, 22);
INSERT INTO `sys_role_permission` VALUES (197, 4, 23);
INSERT INTO `sys_role_permission` VALUES (198, 4, 24);
INSERT INTO `sys_role_permission` VALUES (200, 1, 26);
INSERT INTO `sys_role_permission` VALUES (201, 1, 27);
INSERT INTO `sys_role_permission` VALUES (202, 1, 28);
INSERT INTO `sys_role_permission` VALUES (203, 1, 29);
INSERT INTO `sys_role_permission` VALUES (204, 1, 33);
INSERT INTO `sys_role_permission` VALUES (205, 1, 34);
INSERT INTO `sys_role_permission` VALUES (206, 1, 35);
INSERT INTO `sys_role_permission` VALUES (207, 1, 36);
INSERT INTO `sys_role_permission` VALUES (208, 1, 37);
INSERT INTO `sys_role_permission` VALUES (209, 1, 38);
INSERT INTO `sys_role_permission` VALUES (210, 1, 39);
INSERT INTO `sys_role_permission` VALUES (211, 1, 40);
INSERT INTO `sys_role_permission` VALUES (212, 1, 41);
INSERT INTO `sys_role_permission` VALUES (213, 1, 42);
INSERT INTO `sys_role_permission` VALUES (214, 1, 43);
INSERT INTO `sys_role_permission` VALUES (215, 1, 44);
INSERT INTO `sys_role_permission` VALUES (216, 1, 45);
INSERT INTO `sys_role_permission` VALUES (217, 1, 46);
INSERT INTO `sys_role_permission` VALUES (218, 1, 47);
INSERT INTO `sys_role_permission` VALUES (219, 1, 48);
INSERT INTO `sys_role_permission` VALUES (220, 1, 49);
INSERT INTO `sys_role_permission` VALUES (221, 1, 50);
INSERT INTO `sys_role_permission` VALUES (222, 1, 51);
INSERT INTO `sys_role_permission` VALUES (223, 1, 52);
INSERT INTO `sys_role_permission` VALUES (224, 1, 53);
INSERT INTO `sys_role_permission` VALUES (225, 1, 54);
INSERT INTO `sys_role_permission` VALUES (226, 1, 55);
INSERT INTO `sys_role_permission` VALUES (227, 1, 56);
INSERT INTO `sys_role_permission` VALUES (228, 1, 57);
INSERT INTO `sys_role_permission` VALUES (229, 1, 58);
INSERT INTO `sys_role_permission` VALUES (230, 1, 59);
INSERT INTO `sys_role_permission` VALUES (231, 1, 60);
INSERT INTO `sys_role_permission` VALUES (232, 1, 61);
INSERT INTO `sys_role_permission` VALUES (233, 1, 62);
INSERT INTO `sys_role_permission` VALUES (234, 1, 63);
INSERT INTO `sys_role_permission` VALUES (235, 2, 58);
INSERT INTO `sys_role_permission` VALUES (236, 2, 55);
INSERT INTO `sys_role_permission` VALUES (242, 3, 64);
INSERT INTO `sys_role_permission` VALUES (262, 3, 66);
INSERT INTO `sys_role_permission` VALUES (275, 3, 74);
INSERT INTO `sys_role_permission` VALUES (280, 3, 79);
INSERT INTO `sys_role_permission` VALUES (281, 3, 80);
INSERT INTO `sys_role_permission` VALUES (282, 3, 81);
INSERT INTO `sys_role_permission` VALUES (283, 3, 82);
INSERT INTO `sys_role_permission` VALUES (284, 3, 83);
INSERT INTO `sys_role_permission` VALUES (285, 3, 84);
INSERT INTO `sys_role_permission` VALUES (286, 3, 85);
INSERT INTO `sys_role_permission` VALUES (287, 3, 86);
INSERT INTO `sys_role_permission` VALUES (288, 3, 87);
INSERT INTO `sys_role_permission` VALUES (289, 3, 78);
INSERT INTO `sys_role_permission` VALUES (290, 3, 56);
INSERT INTO `sys_role_permission` VALUES (291, 3, 58);
INSERT INTO `sys_role_permission` VALUES (292, 3, 55);
INSERT INTO `sys_role_permission` VALUES (293, 1, 92);
INSERT INTO `sys_role_permission` VALUES (294, 1, 93);
INSERT INTO `sys_role_permission` VALUES (295, 1, 94);

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '账号',
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '密码',
  `phone` char(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '电子邮箱',
  `status` tinyint(1) NULL DEFAULT 1 COMMENT '账号状态 1启用, 2禁用',
  `is_superuser` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '是否为超级管理员 0-否 1-是',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (1, 'admin', 'pbkdf2_sha256$1200000$rP2I0TrCQ0rv3r0En0TQLX$Sw/0RTubov5xbK48EAQ3ozhaVFlGKW60/r5YnXFMLWA=', '13800000128', 'admin@126.com', 1, 1, '2025-12-26 02:33:45', '2025-10-25 12:09:34');
INSERT INTO `sys_user` VALUES (2, 'user001', 'pbkdf2_sha256$1200000$4wOvzzvwOhRMtpiVxHsyDC$96jm5OAWBVtKuraVFqIuCMux4PpE2sbLZ6XKrLca0uU=', '13800000129', '13800000129@qq.com', 1, 0, '2025-12-25 08:08:23', '2025-11-18 08:38:24');
INSERT INTO `sys_user` VALUES (3, 'user002', 'pbkdf2_sha256$600000$zF903i0KM1Kdd280ywTD1J$y8clUuOgb1ou0yng6mRa+Cu8YzuXpL4bs9q6ti+h70s=', '13800000112', '13800000112@qq.com', 1, 0, '2025-12-15 21:19:33', '2025-11-18 09:16:05');
INSERT INTO `sys_user` VALUES (4, 'user003', 'pbkdf2_sha256$600000$zF903i0KM1Kdd280ywTD1J$y8clUuOgb1ou0yng6mRa+Cu8YzuXpL4bs9q6ti+h70s=', '13800000130', '13800000130@qq.com', 1, 0, '2025-12-15 21:19:34', '2025-11-18 09:25:37');
INSERT INTO `sys_user` VALUES (6, 'user004', 'pbkdf2_sha256$600000$zF903i0KM1Kdd280ywTD1J$y8clUuOgb1ou0yng6mRa+Cu8YzuXpL4bs9q6ti+h70s=', '13800000131', '13800000131@qq.com', 1, 0, '2025-12-15 21:19:36', '2025-12-07 09:22:17');
INSERT INTO `sys_user` VALUES (7, 'test001', 'pbkdf2_sha256$600000$KcJ47CQ4Am7mXC2Q5z9APj$mmHqF3dre0VCA3f282ea0VQCDn+mRc+e7riOp9wDGgk=', '13800000111', '13800000111@126.com', 1, 0, '2025-12-10 06:46:25', '2025-12-10 06:46:25');
INSERT INTO `sys_user` VALUES (8, 'test002', 'pbkdf2_sha256$1200000$EtHVAeuWGayCr1TCe6ZhfY$pSd2aLYr17bA47isGtN+pRGz5eOPj4U5OIfgAp724xg=', '13800000132', '13800000132@sina.com', 1, 0, '2025-12-18 07:13:52', '2025-12-10 06:49:36');
INSERT INTO `sys_user` VALUES (10, 'test003', 'pbkdf2_sha256$600000$pUVG4rHQh8lQKBALeJ9tMC$YVY01nNfV5lfyBrfzaJ+OyHZIbXffMasGhEdvuwXxTQ=', '13800000133', '13800000133@qq.com', 1, 0, '2025-12-10 14:22:50', '2025-12-10 14:22:50');
INSERT INTO `sys_user` VALUES (11, 'test004', 'pbkdf2_sha256$600000$VpWmffKyFT6EEW2ZpC33F9$H+o5K99iClP7ULQHNsecpvXCt7aIeg5BT01T+NpZDpc=', '13800000134', '13800000134@qq.com', 1, 0, '2025-12-11 01:05:45', '2025-12-11 01:05:45');
INSERT INTO `sys_user` VALUES (12, 'test005', 'pbkdf2_sha256$1200000$RsGIxb3IdY7rX8QAn7GYas$/G1A3aTCpsxwiT5CVfAfkNSrfbCxXqYSeW6WNZjfnoQ=', '13800000135', 'test005@163.com', 1, 0, '2025-12-18 17:35:36', '2025-12-18 07:00:06');
INSERT INTO `sys_user` VALUES (13, 'test006', 'pbkdf2_sha256$1200000$GLmoCFpa08n7F7iaN1BSif$/yaqYf4DQHs/1e0GrggjsBXflMbRAIinRtFh+ejTVVo=', '13800000136', '13800000136@126.com', 1, 0, '2025-12-19 13:58:44', '2025-12-19 01:30:45');
INSERT INTO `sys_user` VALUES (14, 'zhengping', 'pbkdf2_sha256$1200000$UoficsDda2zlI6XqDSGz8b$FBC7DTzeiwbLNnshvPXLgVQ8xhv7v8J7NFTzGXY2QO4=', NULL, NULL, 1, 0, '2025-12-22 08:44:07', '2025-12-22 08:44:07');
INSERT INTO `sys_user` VALUES (15, 'wuyuan', 'pbkdf2_sha256$1200000$ncWnGYV1QnCvQ5Oy5YHb3A$wfOfLtYyNoxOnvx6x+S57mkUEC3fOp9fM5fnYqxyWj8=', NULL, NULL, 1, 0, '2025-12-22 08:47:06', '2025-12-22 08:47:06');
INSERT INTO `sys_user` VALUES (16, 'niexiaoqian', 'pbkdf2_sha256$1200000$UMoyMsMrrpei9AXOKEnHWn$dtj6hOsq+EOxGnfPpxbHDRUa3HYdFwIPBIPHH5JvbUg=', NULL, NULL, 1, 0, '2025-12-22 08:50:12', '2025-12-22 08:50:12');
INSERT INTO `sys_user` VALUES (17, 'loujiayi', 'pbkdf2_sha256$1200000$ihje5OMhCnK83rhKXUJLFk$cw5lJjvzc6jDDaabZBymWxtZzuGSdrP7jDSKOipPOuY=', NULL, NULL, 1, 0, '2025-12-22 08:55:43', '2025-12-22 08:55:43');
INSERT INTO `sys_user` VALUES (18, 'dingyuanying', 'pbkdf2_sha256$1200000$RD1TKsiUmXKyUfmBgzU74q$cyKr57XnOMp04IVeWQpNP8Eb6HVUp/Ar8hO+oreVBWU=', NULL, NULL, 1, 0, '2025-12-22 09:00:28', '2025-12-22 09:00:28');
INSERT INTO `sys_user` VALUES (19, 'renwoxing', 'pbkdf2_sha256$1200000$QLTKsZCpMRORdsubw5Oivl$mgvPa4Vd1SrwFALpO3JnJPgKd8Xp0MWUka35QhiUWz8=', NULL, NULL, 1, 0, '2025-12-22 09:02:41', '2025-12-22 09:02:41');
INSERT INTO `sys_user` VALUES (20, 'ruixiaodan', 'pbkdf2_sha256$1200000$zkdBFlc9HSGfu5XlqnjvsF$z4f8ZSdpEVY/X1pmpypS4i1B5YZIL4BhevVjCFLCrko=', NULL, NULL, 1, 0, '2025-12-22 11:14:25', '2025-12-22 11:14:25');
INSERT INTO `sys_user` VALUES (21, 'yezifeng', 'pbkdf2_sha256$1200000$2xaISQH9DmGEqFh44OhfHu$k7fmTVVsItbin/4UBKEhENinn73eT94ZtAkKfUwWZ7c=', NULL, NULL, 1, 0, '2025-12-22 11:16:48', '2025-12-22 11:16:48');
INSERT INTO `sys_user` VALUES (22, 'sundongxu', 'pbkdf2_sha256$1200000$gMxypz6Nd9iq8sriN1ax5x$Fb5YJo4uOrF3RlQyuAHgeeSVvLmdBXZBEEXFlagQ8EE=', NULL, NULL, 1, 0, '2025-12-22 11:19:19', '2025-12-22 11:19:19');
INSERT INTO `sys_user` VALUES (23, 'qianduoduo', 'pbkdf2_sha256$1200000$p2idowDtdb6objFmGauKgg$/6fF5Z4pKus+40nk/7r95oaqeD4Bw1epc+eO84oxQuU=', NULL, NULL, 1, 0, '2025-12-23 06:42:46', '2025-12-23 06:42:46');
INSERT INTO `sys_user` VALUES (24, 'liqingzhao', 'pbkdf2_sha256$1200000$yiZ1UdfdM1NdqzMbznfItZ$bKMWieUUH6oSpoqD/CbVcKRrMWxnr+Q65aYzAdpJAdg=', NULL, NULL, 1, 0, '2025-12-25 11:47:19', '2025-12-25 11:47:19');

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int UNSIGNED NULL DEFAULT NULL COMMENT '账号id',
  `role_id` int UNSIGNED NULL DEFAULT NULL COMMENT '角色id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `u_r_user_id`(`user_id` ASC) USING BTREE,
  INDEX `u_r_role_id`(`role_id` ASC) USING BTREE,
  CONSTRAINT `u_r_role_id` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `u_r_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 58 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户角色表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------
INSERT INTO `sys_user_role` VALUES (1, 1, 1);
INSERT INTO `sys_user_role` VALUES (2, 1, 2);
INSERT INTO `sys_user_role` VALUES (3, 3, 2);
INSERT INTO `sys_user_role` VALUES (4, 3, 3);
INSERT INTO `sys_user_role` VALUES (5, 4, 2);
INSERT INTO `sys_user_role` VALUES (10, 2, 3);
INSERT INTO `sys_user_role` VALUES (12, 6, 2);
INSERT INTO `sys_user_role` VALUES (13, 7, 1);
INSERT INTO `sys_user_role` VALUES (14, 7, 2);
INSERT INTO `sys_user_role` VALUES (15, 7, 3);
INSERT INTO `sys_user_role` VALUES (32, 10, 1);
INSERT INTO `sys_user_role` VALUES (33, 10, 2);
INSERT INTO `sys_user_role` VALUES (41, 11, 8);
INSERT INTO `sys_user_role` VALUES (42, 11, 9);
INSERT INTO `sys_user_role` VALUES (43, 8, 1);
INSERT INTO `sys_user_role` VALUES (44, 8, 2);
INSERT INTO `sys_user_role` VALUES (45, 12, 3);
INSERT INTO `sys_user_role` VALUES (46, 13, 3);
INSERT INTO `sys_user_role` VALUES (47, 14, 2);
INSERT INTO `sys_user_role` VALUES (48, 15, 3);
INSERT INTO `sys_user_role` VALUES (49, 16, 2);
INSERT INTO `sys_user_role` VALUES (50, 17, 2);
INSERT INTO `sys_user_role` VALUES (51, 18, 1);
INSERT INTO `sys_user_role` VALUES (52, 19, 2);
INSERT INTO `sys_user_role` VALUES (53, 20, 2);
INSERT INTO `sys_user_role` VALUES (54, 21, 2);
INSERT INTO `sys_user_role` VALUES (55, 22, 2);
INSERT INTO `sys_user_role` VALUES (56, 23, 3);
INSERT INTO `sys_user_role` VALUES (57, 24, 3);

SET FOREIGN_KEY_CHECKS = 1;
