package com.fenglin.springboottest.common;

/**
 * 登录后返回给前端的安全用户信息（不含密码哈希）
 */
public class UserVO {
    private Long id;
    private String username;

    public UserVO() {
    }

    public UserVO(Long id, String username) {
        this.id = id;
        this.username = username;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }
}
