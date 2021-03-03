/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : localhost:3306
 Source Schema         : quotes

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 22/02/2021 00:25:42
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for author
-- ----------------------------
DROP TABLE IF EXISTS `author`;
CREATE TABLE `author`  (
  `author_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '唯一标识ID',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '作家姓名',
  `birthdate` date NULL DEFAULT NULL COMMENT '作家出生日期',
  `bio` varchar(10000) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '作家小传',
  PRIMARY KEY (`author_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1000 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for quote
-- ----------------------------
DROP TABLE IF EXISTS `quote`;
CREATE TABLE `quote`  (
  `quote_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '唯一标识ID',
  `text` varchar(10000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '引用的语句',
  `author_id` int(0) NULL DEFAULT NULL COMMENT '作家ID',
  PRIMARY KEY (`quote_id`) USING BTREE,
  INDEX `author_id`(`author_id`) USING BTREE,
  CONSTRAINT `quote_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author` (`author_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1000 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for quote_ref_tag
-- ----------------------------
DROP TABLE IF EXISTS `quote_ref_tag`;
CREATE TABLE `quote_ref_tag`  (
  `quote_tag_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '唯一标识ID',
  `quote_id` int(0) NOT NULL COMMENT '语句ID',
  `tag_id` int(0) NOT NULL COMMENT '标签ID',
  PRIMARY KEY (`quote_tag_id`) USING BTREE,
  INDEX `quote_id`(`quote_id`) USING BTREE,
  INDEX `tag_id`(`tag_id`) USING BTREE,
  CONSTRAINT `quote_ref_tag_ibfk_1` FOREIGN KEY (`quote_id`) REFERENCES `quote` (`quote_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `quote_ref_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1000 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag`  (
  `tag_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '唯一标识ID',
  `tag` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标签名称',
  PRIMARY KEY (`tag_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1000 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
