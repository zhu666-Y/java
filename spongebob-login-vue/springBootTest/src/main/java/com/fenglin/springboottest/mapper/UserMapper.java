package com.fenglin.springboottest.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.fenglin.springboottest.entity.User;

/**
 * 用户表 Mapper，继承 BaseMapper 后即拥有常用 CRUD 能力
 */
public interface UserMapper extends BaseMapper<User> {
}
