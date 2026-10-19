package com.fenglin.springboottest.common;

/**
 * 业务异常：登录 / 注册失败时携带一旬友好的提示语。
 * 由 Controller 捕获后映射成 Result.error(message)。
 */
public class AuthException extends RuntimeException {
    public AuthException(String message) {
        super(message);
    }
}
