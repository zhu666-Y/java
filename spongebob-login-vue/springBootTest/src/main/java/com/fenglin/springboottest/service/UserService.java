package com.fenglin.springboottest.service;

import com.fenglin.springboottest.entity.User;

/**
 * 用户业务接口
 */
public interface UserService {

    /**
     * 注册：用户名查重 + BCrypt 加密入库
     *
     * @param username 用户名
     * @param password 明文密码
     * @return 已入库的用户（含主键）
     * @throws com.fenglin.springboottest.common.AuthException 用户名已被占用时抛出
     */
    User register(String username, String password);

    /**
     * 登录：查询数据库并校验 BCrypt 密码
     *
     * @param username 用户名
     * @param password 明文密码
     * @return 校验通过的用户实体
     * @throws com.fenglin.springboottest.common.AuthException 用户名不存在或密码错误时抛出
     */
    User login(String username, String password);
}
