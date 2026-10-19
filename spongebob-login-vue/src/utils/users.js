// 用户数据层：调用 Spring Boot 后端接口
// 后端地址通过 Vite 代理转发（/api -> http://localhost:8081，见 vite.config.js）
// 登录态由后端 HttpSession 维护：登录成功后浏览器自动携带 JSESSIONID Cookie。

async function request(path, options) {
  try {
    const res = await fetch(path, options)
    if (!res.ok) {
      // 401（未登录）也尝试解析后端返回的信息
      let payload = {}
      try { payload = await res.json() } catch { /* 忽略 */ }
      return { ok: false, code: res.status, message: payload.message || ('服务器开小差了（HTTP ' + res.status + '）') }
    }
    return await res.json()
  } catch {
    return { ok: false, code: 0, message: '连不上海底服务器，请确认后端已启动～' }
  }
}

// 注册：后端校验用户名查重并入库 MySQL
export async function registerUser({ username, password }) {
  const res = await request('/api/user/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  return { ok: res.code === 200, message: res.message }
}

// 登录：后端查询数据库校验，成功后在服务端建立会话
export async function verifyUser({ username, password }) {
  const res = await request('/api/user/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  return { ok: res.code === 200, message: res.message, user: res.data }
}

// 获取当前登录用户（需已登录）：后端校验会话，返回 { id, username }
export async function getCurrentUser() {
  return request('/api/user/me', { method: 'GET' })
}

// 登出：让后端会话失效
export async function logoutUser() {
  return request('/api/user/logout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  })
}
