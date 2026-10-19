package com.fenglin.springboottest.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.fenglin.springboottest.common.AuthException;
import com.fenglin.springboottest.entity.User;
import com.fenglin.springboottest.mapper.UserMapper;
import com.fenglin.springboottest.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

/**
 * 用户业务实现：MySQL 持久层由 MyBatis-Plus 提供
 */
@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;

    /** BCrypt 加密器：同一明文每次加密结果不同，校验时用 matches() */
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public User register(String username, String password) {
        // 1. 用户名查重
        User exist = userMapper.selectOne(
                new QueryWrapper<User>().eq("username", username));
        if (exist != null) {
            throw new AuthException("这个名字已经被别人抢先注册啦～");
        }

        // 2. 密码加密入库（不存明文）
        User user = new User();
        user.setUsername(username);
        user.setPassword(passwordEncoder.encode(password));
        user.setCreateTime(LocalDateTime.now());
        user.setUpdateTime(LocalDateTime.now());
        userMapper.insert(user);
        return user;
    }

    @Override
    public User login(String username, String password) {
        User user = userMapper.selectOne(
                new QueryWrapper<User>().eq("username", username));
        if (user == null) {
            throw new AuthException("查无此人，你还没注册哦～");
        }
        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new AuthException("密码错误，蟹堡秘方可不外传！");
        }
        return user;
    }
}
