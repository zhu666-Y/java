-- ============================================================
-- 幂等初始化脚本：每次开机启动都可以安全重复执行
-- 与 spongebob.sql 的区别：这里不 DROP，不会清掉已有用户数据
-- 由 scripts\init-db.bat 自动执行
-- ============================================================

CREATE DATABASE IF NOT EXISTS spongebob
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_general_ci;

USE spongebob;

CREATE TABLE IF NOT EXISTS t_user (
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

-- 内置测试账号：spongebob / 123456
-- 已存在则跳过，永远不会覆盖你自己注册的数据
INSERT INTO t_user (username, password)
SELECT 'spongebob', '$2b$10$KjcjZgjm9o64gjAbKprHvO8AL1yXDyK5Y6ppH/U2cdQPzloQ2GUli'
WHERE NOT EXISTS (SELECT 1 FROM t_user WHERE username = 'spongebob');
