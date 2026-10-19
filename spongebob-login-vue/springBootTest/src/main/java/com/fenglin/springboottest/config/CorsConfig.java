package com.fenglin.springboottest.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * 跨域配置：允许前端直连 http://localhost:8081/api/** 调用接口。
 * 说明：开发时走 Vite 代理（5173 -> 8081）不需要它，
 * 但前端生产构建后用 file:// 打开、或部署在不同域名/端口时需要。
 */
@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("*")   // 学习项目放开所有来源；生产环境应改成具体域名
                .allowedMethods("*")
                .allowedHeaders("*")
                .maxAge(3600);         // 预检请求结果缓存 1 小时，减少 OPTIONS 次数
    }
}
