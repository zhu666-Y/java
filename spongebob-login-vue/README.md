# 海绵宝宝登录项目（前端 + 后端一体）

Vue 3 + Vite 前端，Spring Boot 3 + MyBatis-Plus + MySQL 后端，前后端分离开发。

## 快速启动（推荐）

双击 **`scripts\start-all.bat`**，等它跑完会自动打开浏览器。

> **重置后最快的启动方式**：双击 **`scripts\start-jar.bat`**。它直接运行项目根目录里那份 `spongebob-login.jar`（由 `build-release.bat` 生成并拷贝出来，重置后 `target/` 虽被删但根目录文件保留），无需 Node、无需编译，顺带帮你建好数据库。访问 http://localhost:8081 即是完整应用。
>
> **想开机自动启动**：以管理员身份双击 **`scripts\install-autostart.bat`** 一次即可（卸载用 `uninstall-autostart.bat`）。

脚本会自动完成所有事（包括每次开机后依赖被清空的情况）：

1. 检查 MySQL 并幂等初始化数据库（不会覆盖已有数据）
2. 后端没有 jar 就自动编译（Maven wrapper，无需装 Maven）
3. 前端没有 node_modules 就自动 `npm install`
4. 启动后端（8081）和前端（5173），并确认它们真的就绪

| 访问项 | 地址 |
|---|---|
| 登录页 | http://localhost:5173 |
| 后端接口 | http://localhost:8081 |
| 测试账号 | spongebob / 123456 |

## 停止项目

双击 **`scripts\stop-all.bat`**（MySQL 是系统服务，保持运行即可）。

## 发布成单个 jar（可选）

双击 **`scripts\build-release.bat`**：自动构建前端并打进后端，产出一个 jar。
之后不需要 node，只要：

```
java -jar springBootTest\target\springBootTest-0.0.1-SNAPSHOT.jar
```

浏览器打开 http://localhost:8081 就是完整的登录应用（前后端同一个服务，同源无跨域）。

## 目录说明

```
scripts\    启动/停止/发布脚本（.bat 是 GBK 编码、相对路径；改中文请保持 ANSI/GBK，勿存 UTF-8）
gen_scripts.py  所有 .bat 的唯一来源：若某个 .bat 中文乱码，在项目根目录跑 `python gen_scripts.py` 即可以 GBK 重新生成（无需手改）
src\        前端源码（登录/注册/主页）
springBootTest\  后端源码（Spring Boot + MyBatis-Plus）
springBootTest\sql\spongebob.sql  完全重置数据库用（会删数据！）
```

## 后端接口（登录认证）

登录态由后端 **HttpSession** 管理：登录成功后浏览器自动携带 `JSESSIONID` Cookie，后续 `/me`、`/logout` 等接口据此识别当前用户。所有接口统一返回 `{ code, message, data }`。

| 方法 | 路径 | 说明 | 成功/失败 |
|---|---|---|---|
| POST | `/api/user/login` | 登录 `{username, password}` | 200 + `data:{id,username}`；错密/无用户 500；空值或超长(>20/>50) 400 |
| POST | `/api/user/register` | 注册 `{username, password}`（BCrypt 加密入库，用户名查重） | 200；用户名已存在 500 |
| GET | `/api/user/me` | 获取当前登录用户（**需已登录**） | 200 + 当前用户；未登录 **401** |
| POST | `/api/user/logout` | 使后端会话失效（前端同时清理本地存储） | 200 |

> 测试账号：`spongebob / 123456`（密码以 BCrypt 加密存于 `spongebob.t_user` 表）。
> 想重置数据库：`springBootTest/sql/spongebob.sql`（会删数据）；日常开机只用 `init-db.sql`（幂等、不删数据）。

## 常见问题

- **改了后端代码没生效**：重跑 `scripts\start-all.bat`（脚本检测不到源码变化，会直接用旧 jar；想强制重新编译，删掉 `springBootTest\target` 文件夹再启动）
- **端口被占用**：启动脚本会自动清理 8081/5173 端口占用进程
- **依赖装得慢**：`npm config set registry https://registry.npmmirror.com` 换国内镜像
- **MySQL 没启动**：Win+R 输入 `services.msc`，找到 MySQL80 右键启动（脚本也会尝试自动启动）
- **想改数据库账号/端口/安装路径**：只改 `scripts\env.bat`，其它脚本都引用它

## 技术栈版本

Vue 3.4 / Vite 5 / vue-router 4 · Spring Boot 3.4.5 / MyBatis-Plus 3.5.7 / Java 17 · MySQL 8.0（密码 BCrypt 加密存储）
