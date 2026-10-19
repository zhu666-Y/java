-- ============================================================
-- 海绵宝宝登录项目数据库初始化脚本
-- 项目：springBootTest（后端） + spongebob-login-vue（前端）
-- 说明：创建 spongebob 库和 t_user 表，供 MyBatis-Plus 访问
-- 使用方式：mysql -uroot -p123456 < spongebob.sql
--          或在 Navicat / IDEA Database 面板中直接执行
-- ============================================================

-- 如果库已存在则先删除（可按需注释掉这行）
-- DROP DATABASE IF EXISTS spongebob;

CREATE DATABASE IF NOT EXISTS spongebob
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_general_ci;

USE spongebob;

-- 用户表
DROP TABLE IF EXISTS t_user;
CREATE TABLE t_user (
    id          BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    username    VARCHAR(20)  NOT NULL                COMMENT '用户名（唯一）',
    password    VARCHAR(100) NOT NULL                COMMENT '密码（BCrypt 加密存储）',
    create_time DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_username (username)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '用户表';

-- 测试数据：用户名 spongebob，密码 123456
-- 密码字段为 BCrypt 加密结果，后端校验时使用 matches() 比对
INSERT INTO t_user (username, password) VALUES
('spongebob', '$2b$10$KjcjZgjm9o64gjAbKprHvO8AL1yXDyK5Y6ppH/U2cdQPzloQ2GUli');
