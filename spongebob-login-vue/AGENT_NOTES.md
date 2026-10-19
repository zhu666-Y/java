# AGENT_NOTES.md — 给 AI 助手看的运维卡片

> **这是写给 AI 的，不是写给用户的。**
> 目的：下次会话直接照做，不要重新探索目录、不要重复踩坑、不要重新推导路径。
> 电脑每次重置：`node_modules/` 和 `target/` 会被删除；MySQL 数据、`.m2` 依赖缓存、已装软件都还在。
> 上次验证日期：**2026-10-14**（npm install ✅、mvnw.cmd package ✅、init-db.sql 建库建表 ✅、dev 模式 5173+8081 联调 ✅、build-release 单 jar ✅、GBK 脚本已重生、**登录后端会话认证已完成并全链路验证**）。

---

## 0. 一句话启动（按这个来，别绕路）

项目根目录（本项目实际位置，注意在「新建文件夹」里）：

```
C:\Users\Administrator\Desktop\新建文件夹\spongebob-login-vue\
```

- **（最快·重置后首推）双击 `scripts\start-jar.bat`**：直接跑项目根目录里 `spongebob-login.jar`（build-release 自动拷贝出来、重置后依然保留），无需 node、无需编译，顺带幂等建好数据库。一条命令把整套应用起在 http://localhost:8081
- **开机自动启动（可选）**：以管理员身份双击 `scripts\install-autostart.bat` 一次，注册「登录时自动跑 start-jar.bat」（沙箱里不能跑 schtasks，所以这步交给你在真实 cmd 里执行）。卸载用 `scripts\uninstall-autostart.bat`
- **用户双击**：`scripts\start-all.bat`（会 pause 并自动打开浏览器，dev 模式 5173+8081）
- **PowerShell 无暂停启动**：`$env:SPONGE_NO_PAUSE='1'; & ".\scripts\start-all.bat"`（在根目录执行）
- **停止**：`scripts\stop-all.bat`（或 `$env:SPONGE_NO_PAUSE='1'; & ".\scripts\stop-all.bat"`）
- **单 jar 发布**：`scripts\build-release.bat`（前端构建打进后端，一个 jar 跑完整应用，无需 node）

脚本会自动完成：检查/启动 MySQL → 幂等建库建表 → 缺 jar 就 `mvnw.cmd package` → 缺 node_modules 就 `npm install` → 起后端(8081) → 起前端(5173) → 健康探测确认就绪。**不需要手动做任何一步。**

## 1. 项目结构（别再 find 了）

```
C:\Users\Administrator\Desktop\新建文件夹\spongebob-login-vue\   ← 前端 Vue3+Vite（根目录）
├── gen_scripts.py   ← ★ 全部 .bat 的唯一正确来源（UTF-8 的 .py，跑它用 GBK 重生 .bat）
├── scripts\         ← 启动/停止脚本（GBK/ANSI-936 编码、无 BOM、相对路径）
│   ├── env.bat        ← 所有路径/端口/账号配置，唯一可能要改的文件
│   ├── helpers.bat    ← killport / apiup / waitapi 三个工具函数
│   ├── init-db.bat    ← 幂等数据库初始化（跑 sql/init-db.sql，不删数据）
│   ├── start-all.bat / stop-all.bat          ← 一键启动/停止
│   └── start/stop-backend.bat、start/stop-frontend.bat ← 分开控制
├── src\               ← 页面代码（Login/Register/Home 三视图 + users.js 数据层）
├── springBootTest\    ← 内嵌的后端副本（Spring Boot 3.4.5 + MyBatis-Plus 3.5.7）
│   ├── .mvn\ mvnw mvnw.cmd   ← Maven wrapper 3.9.9（PATH 上没有 mvn，必须用这个）
│   ├── sql\spongebob.sql   ← 销毁式重建（DROP TABLE，重置用）
│   ├── sql\init-db.sql     ← 幂等初始化（开机自动跑这个）
│   └── src\main\resources\static\ ← build-release 后是 Vue 构建产物
└── vite.config.js     ← dev(5173)/preview(4173) 都配了 /api → 8081 代理
D:\workSpace\springBootTest\ ← IDEA 工作区的另一份后端（源码与内嵌副本一致）
```

**脚本全部用 `%~dp0` 取自身目录再 `..` 向上，整文件夹搬到哪里都能跑（相对路径，无硬编码绝对路径）。**

## 2. 环境事实（直接用，别再 where/ls 找）

| 项 | 值 |
|---|---|
| MySQL | `C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`，root / 123456，服务名 MySQL80，库 spongebob |
| JDK 17 | `C:\Program Files\Java\jdk-17`（env.bat 优先用它；PATH 上默认是 Java 21，也能编） |
| Maven | 项目里 `mvnw.cmd`（wrapper 3.9.9，缓存在 `~\.m2\wrapper\dists`）。**PATH 上没有 mvn 命令** |
| Node | PATH 上有（系统 20.11 + WorkBuddy 托管 22），npm 可直接用；env.bat 也会补 `D:\Program Files\nodejs` |
| 后端 | 8081 端口。登录认证接口：`POST /api/user/login`、`POST /api/user/register`、`GET /api/user/me`（需登录，未登录返回 HTTP 401）、`POST /api/user/logout`。统一返回 `{code,message,data}`，并带标准 HTTP 状态码（成功 200 / 业务错误 500 / 未登录 401） |
| 前端 | 5173 端口（Vite 代理 /api → 8081），preview 是 4173 |
| 测试账号 | spongebob / 123456（BCrypt 加密存 t_user 表） |

## 3. 已知坑（都踩过，别再踩）

1. **脚本必须 GBK 无 BOM**：旧版 .bat 曾被存成 UTF-8-BOM（`efbbbf`），cmd 把 BOM 当乱码、首行命令直接报错。现在由 `gen_scripts.py` 统一以 `encoding='gbk'` 写出（无 BOM）。**若哪天 .bat 又变乱码，别手改，直接重跑 `python gen_scripts.py` 即可恢复。**
2. **沙箱端口注入**：从 Agent 工具后台启动 Spring Boot 时，配置的 8081 可能被环境覆盖成随机端口。脚本已用 `--server.port=%BACKEND_PORT%` 显式锁定。
3. **沙箱 http_proxy 拦本地回环**：Bash 里 curl localhost 必须加 `--noproxy '*'`，否则误报服务挂了。
4. **PowerShell 任务结束会杀子进程**：后台 PowerShell 跑 start-all 后，等任务结束，`start` 起的服务窗口会被一起回收。验证服务要在任务存活期间 curl；用户双击场景无此问题。
5. **Bash 里跑 `./mvnw` 会被 safe-delete 钩子干扰**：本机 Bash 工具的中文目录名 + 钩子会拼错临时文件路径，导致 `ClassNotFoundException: classworlds.Launcher`。**验证后端编译请用 PowerShell 跑 `mvnw.cmd`，不要跑 bash 的 `./mvnw`。** 用户双击 .bat 走的就是 mvnw.cmd，不受影响。
6. **cmd.exe 不能从 Bash 直接调**：测试 .bat 要用 PowerShell 工具：`& ".\scripts\x.bat"`，并设 `$env:SPONGE_NO_PAUSE='1'` 跳过 pause，否则后台卡住。
7. **幂等 vs 销毁 SQL**：日常启动只跑 `init-db.sql`（不删数据）。想清空重置才用 `spongebob.sql`（DROP TABLE）。别搞反。
8. **netstat 双栈**：同一端口 IPv4/IPv6 两行同 PID，killport 里已做空格分隔去重。

## 4. 启动后的验证清单（30 秒搞定）

```
curl --noproxy '*' -X POST http://localhost:5173/api/user/login -H "Content-Type: application/json" -d '{"username":"spongebob","password":"123456"}'
→ 期待 {"code":200,"message":"登录成功..."}
netstat -ano | findstr ":8081 :5173" → 两个端口都在 LISTENING
```

## 5. 单 jar 发布模式

- `build-release.bat`：npm build → dist 拷进后端 static → mvnw package，产物 `springBootTest\target\springBootTest-0.0.1-SNAPSHOT.jar`（约 31MB）
- 跑法：`java -jar jar路径`，浏览器直接开 http://localhost:8081 就是登录页（同源，无需代理/CORS）
- 注意：发布后 start-backend.bat 起的就是这个带前端的 jar；改了前端代码要重跑 build-release 才生效

## 6. 项目还缺什么（用户没催就别主动大改）

- "忘记密码"只有提示语，没有真正的找回/重置流程（需后端加 reset 接口 + 邮件/SMS，暂未做）
- 无 ESLint/Prettier/.editorconfig 等工程规范文件（学习项目可不加）
- 后端 /user/* 的旧 Thymeleaf 演示代码还在（UserController + templates），是用户的学习痕迹，别动
- README.md 里的路径用的是相对写法（正确）；本文档旧版曾误写成 `Desktop\spongebob-login-vue`（少了「新建文件夹」），已修正

## 7. 登录后端认证（已完成，2026-10-14）

采用 **Spring 自带 HttpSession**（嵌入式 Tomcat 内存会话，零新依赖、重置后也无需重建），登录后浏览器自动带 `JSESSIONID` Cookie。

- **`POST /api/user/login`** `{username,password}` → 200 + `data:{id,username}`（脱敏，不含密码哈希）；错误密码/无用户返回 500 + 提示；空值/超长(>20/>50)返回 400
- **`POST /api/user/register`** → 用户名查重（已存在 500），BCrypt 加密入库，返回 200 + 用户信息
- **`GET /api/user/me`** → 已登录 200 + 当前用户；未登录 **401**（前端据此跳回 /login）
- **`POST /api/user/logout`** → 使服务端会话失效 200

后端新增文件：`common/UserVO.java`（脱敏用户信息）、`common/AuthException.java`（业务异常）。
`UserService` 改为返回 `User` 实体、失败时抛 `AuthException`；`UserApiController` 全部返回 `ResponseEntity<Result>`（规范状态码）。
前端胶水（`src/utils/users.js`、`src/views/HomeView.vue`）：`HomeView` 挂载时调 `/me` 验活、登出调 `/logout` 使后端会话失效，登录态以前端 + 后端双重校验。

> 验证记录：login→200(data)、wrong pw→500、未登录/me→401、带 cookie /me→200、logout→200、logout 后再 /me→401、注册+登录+ /me 全过。单 jar（含前端新产物）已重打到根目录 `spongebob-login.jar` 与 `D:\spongebob-login.jar`。
