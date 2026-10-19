package com.fenglin.springboottest.controller;

import com.fenglin.springboottest.common.AuthException;
import com.fenglin.springboottest.common.Result;
import com.fenglin.springboottest.common.UserVO;
import com.fenglin.springboottest.entity.User;
import com.fenglin.springboottest.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * 前后端分离接口：供 Vue 前端（海绵宝宝登录页）调用。
 * 前端通过 Vite 代理把 /api 转发到本服务的 8081 端口。
 *
 * <p>登录态采用服务端 HttpSession 管理（嵌入式 Tomcat 内存会话，无需额外依赖、
 * 重置后也无需重建），登录成功后会在 Cookie 中写入 JSESSIONID，
 * 后续 /me、/logout 等接口据此识别当前用户。</p>
 */
@RestController
@RequestMapping("/api/user")
public class UserApiController {

    /** 存放在 Session 中的登录用户键名 */
    public static final String SESSION_KEY = "SPONGE_USER";

    /** 用户名 / 密码长度上限，与数据库字段、前端 maxlength 保持一致 */
    private static final int USERNAME_MAX = 20;
    private static final int PASSWORD_MAX = 50;

    @Autowired
    private UserService userService;

    /**
     * 登录接口
     * 请求体：{ "username": "...", "password": "..." }
     * 成功时建立会话并返回脱敏后的用户信息（不含密码）。
     */
    @PostMapping("/login")
    public ResponseEntity<Result> login(@RequestBody Map<String, String> body, HttpSession session) {
        String username = body.get("username");
        String password = body.get("password");
        if (username == null || username.isBlank()
                || password == null || password.isBlank()) {
            return ResponseEntity.badRequest().body(Result.error("用户名和密码不能为空～"));
        }
        username = username.trim();
        if (username.length() > USERNAME_MAX || password.length() > PASSWORD_MAX) {
            return ResponseEntity.badRequest().body(Result.error("用户名或密码长度超出限制～"));
        }
        try {
            User user = userService.login(username, password);
            // 把脱敏后的用户信息放进会话（不存密码哈希）
            session.setAttribute(SESSION_KEY, new UserVO(user.getId(), user.getUsername()));
            return ResponseEntity.ok(Result.success("登录成功，欢迎回到比奇堡！",
                    new UserVO(user.getId(), user.getUsername())));
        } catch (AuthException e) {
            return ResponseEntity.status(500).body(Result.error(e.getMessage()));
        }
    }

    /**
     * 注册接口
     * 请求体：{ "username": "...", "password": "..." }
     */
    @PostMapping("/register")
    public ResponseEntity<Result> register(@RequestBody Map<String, String> body) {
        String username = body.get("username");
        String password = body.get("password");
        if (username == null || username.isBlank()
                || password == null || password.isBlank()) {
            return ResponseEntity.badRequest().body(Result.error("用户名和密码不能为空～"));
        }
        username = username.trim();
        if (username.length() > USERNAME_MAX || password.length() > PASSWORD_MAX) {
            return ResponseEntity.badRequest().body(Result.error("用户名或密码长度超出限制～"));
        }
        try {
            User user = userService.register(username, password);
            return ResponseEntity.ok(Result.success("注册成功，欢迎加入比奇堡！",
                    new UserVO(user.getId(), user.getUsername())));
        } catch (AuthException e) {
            return ResponseEntity.status(500).body(Result.error(e.getMessage()));
        }
    }

    /**
     * 获取当前登录用户（需已登录）。
     * 未登录返回 HTTP 401，前端据此跳回登录页。
     */
    @GetMapping("/me")
    public ResponseEntity<Result> me(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session == null) {
            return ResponseEntity.status(401).body(Result.unauthorized("你还没登录呢～"));
        }
        UserVO user = (UserVO) session.getAttribute(SESSION_KEY);
        if (user == null) {
            return ResponseEntity.status(401).body(Result.unauthorized("你还没登录呢～"));
        }
        return ResponseEntity.ok(Result.success("已登录", user));
    }

    /**
     * 登出接口：让服务端的会话失效（前端同时清理本地存储）。
     */
    @PostMapping("/logout")
    public ResponseEntity<Result> logout(HttpSession session) {
        session.invalidate();
        return ResponseEntity.ok(Result.success("已退出登录，比奇堡随时欢迎你回来～"));
    }
}
