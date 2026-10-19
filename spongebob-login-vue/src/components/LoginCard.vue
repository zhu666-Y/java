<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { verifyUser } from '../utils/users'

const router = useRouter()

// 表单状态：用 Vue 的响应式绑定替代原生 DOM 操作
const username = ref('')
const password = ref('')
const remember = ref(false)
const isSubmitting = ref(false)
const showToast = ref(false)
const isError = ref(false)
const toastMessage = ref('')
let toastTimer = null

// 页面加载时恢复"记住我"的用户名
onMounted(() => {
  const saved = localStorage.getItem('spongebob-remember')
  if (saved) {
    username.value = saved
    remember.value = true
  }
})

function showToastMsg(message, error = false, duration = 2600) {
  toastMessage.value = message
  isError.value = error
  showToast.value = true
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (showToast.value = false), duration)
}

// 忘记密码：暂未开通找回功能，给出友好提示（替代原来的死链接）
function onForgotPassword() {
  showToastMsg('找回功能还没开通，请联系比奇堡管理员重置密码～', true)
}

async function onSubmit() {
  const name = username.value.trim()
  if (!name || !password.value) return
  if (isSubmitting.value) return // 防重复提交

  isSubmitting.value = true
  try {
    // 登录校验：调用 Spring Boot 后端（MySQL 数据库 + BCrypt）
    const res = await verifyUser({ username: name, password: password.value })
    showToastMsg(res.ok ? '🎉 ' + res.message : res.message, !res.ok)
    if (!res.ok) return

    // 记住我：持久化用户名
    if (remember.value) {
      localStorage.setItem('spongebob-remember', name)
    } else {
      localStorage.removeItem('spongebob-remember')
    }

    // 记录登录态，跳转主页
    sessionStorage.setItem('spongebob-user', name)
    setTimeout(() => router.push('/home'), 1200)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="card">
    <div class="avatar">🧽</div>
    <h1>海绵宝宝登录</h1>
    <p class="subtitle">欢迎来到比奇堡海底世界！</p>

    <form @submit.prevent="onSubmit">
      <div class="field">
        <label for="username">用户名</label>
        <span class="icon">🍍</span>
        <input
          v-model="username"
          type="text"
          id="username"
          placeholder="请输入你的名字"
          maxlength="20"
          autocomplete="username"
          required
        />
      </div>

      <div class="field">
        <label for="password">密码</label>
        <span class="icon">🔑</span>
        <input
          v-model="password"
          type="password"
          id="password"
          placeholder="蟹堡秘方可不外传哦"
          maxlength="50"
          autocomplete="current-password"
          required
        />
      </div>

      <div class="row">
        <label class="remember"><input type="checkbox" v-model="remember" /> 记住我</label>
        <a href="#" @click.prevent="onForgotPassword">忘记密码？</a>
      </div>

      <button type="submit" class="btn" :disabled="isSubmitting">
        {{ isSubmitting ? '潜 水 中 …' : '登 录 🌊' }}
      </button>
    </form>

    <p class="footer">还没有账号？ <router-link to="/register">和派大星一起注册</router-link></p>

    <div class="toast" :class="{ show: showToast, error: isError }">{{ toastMessage }}</div>
  </div>
</template>

<style scoped>
  /* 登录卡片 */
  .card {
    position: relative;
    z-index: 5;
    width: 360px;
    padding: 38px 32px 32px;
    background: #fffef0;
    border: 6px solid var(--sponge-yellow-deep);
    border-radius: 28px 28px 30px 30px;
    box-shadow: 0 16px 40px rgba(0,0,0,0.35);
    text-align: center;
    /* 海绵质感的孔洞感 */
    background-image:
      radial-gradient(circle at 12% 18%, rgba(245,197,24,0.35) 6px, transparent 7px),
      radial-gradient(circle at 82% 12%, rgba(245,197,24,0.3) 5px, transparent 6px),
      radial-gradient(circle at 25% 85%, rgba(245,197,24,0.3) 7px, transparent 8px),
      radial-gradient(circle at 90% 78%, rgba(245,197,24,0.35) 6px, transparent 7px),
      radial-gradient(circle at 55% 55%, rgba(245,197,24,0.18) 5px, transparent 6px);
  }

  .avatar {
    width: 84px; height: 84px;
    margin: -64px auto 10px;
    background: var(--sponge-yellow);
    border: 5px solid var(--sponge-yellow-deep);
    border-radius: 50% 50% 48% 48%;
    display: flex; align-items: center; justify-content: center;
    font-size: 46px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.25);
  }

  h1 {
    color: var(--sea-deep);
    font-size: 26px;
    letter-spacing: 1px;
    margin-bottom: 4px;
    text-shadow: 1px 1px 0 var(--sponge-yellow-deep);
  }
  .subtitle { color: var(--sea-mid); font-size: 13px; margin-bottom: 22px; }

  .field { position: relative; margin-bottom: 16px; text-align: left; }
  .field label {
    display: block;
    font-size: 13px;
    color: var(--sea-deep);
    margin-bottom: 6px;
    font-weight: bold;
  }
  .field input {
    width: 100%;
    padding: 12px 14px 12px 40px;
    border: 3px solid var(--sponge-yellow-deep);
    border-radius: 14px;
    font-size: 15px;
    background: #fffdf5;
    outline: none;
    transition: border-color .2s, box-shadow .2s;
  }
  .field input:focus {
    border-color: var(--sea-light);
    box-shadow: 0 0 0 3px rgba(63,182,201,0.3);
  }
  .field .icon {
    position: absolute;
    left: 13px; bottom: 11px;
    font-size: 18px;
  }

  .row { display: flex; justify-content: space-between; align-items: center; font-size: 12px; margin-bottom: 20px; }
  .row a { color: var(--coral); text-decoration: none; }
  .row a:hover { text-decoration: underline; }
  .remember { color: var(--sea-mid); display: flex; align-items: center; gap: 5px; }

  .btn {
    width: 100%;
    padding: 13px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(180deg, var(--sponge-yellow) 0%, var(--sponge-yellow-deep) 100%);
    color: var(--sea-deep);
    font-size: 17px;
    font-weight: bold;
    letter-spacing: 2px;
    cursor: pointer;
    box-shadow: 0 6px 0 #c79a0a, 0 8px 14px rgba(0,0,0,0.25);
    transition: transform .08s, box-shadow .08s;
  }
  .btn:active { transform: translateY(4px); box-shadow: 0 2px 0 #c79a0a, 0 4px 8px rgba(0,0,0,0.25); }
  .btn:hover { filter: brightness(1.05); }
  .btn:disabled { cursor: wait; opacity: 0.75; }

  .footer { margin-top: 18px; font-size: 12px; color: var(--sea-mid); }
  .footer a { color: var(--coral); text-decoration: none; }
  .footer a:hover { text-decoration: underline; }

  /* 提示：成功 / 错误两种样式 */
  .toast {
    position: fixed;
    top: 24px; left: 50%;
    transform: translateX(-50%) translateY(-120%);
    background: var(--sponge-yellow);
    color: var(--sea-deep);
    padding: 12px 24px;
    border-radius: 30px;
    font-weight: bold;
    box-shadow: 0 6px 16px rgba(0,0,0,0.3);
    transition: transform .4s ease;
    z-index: 50;
  }
  .toast.show { transform: translateX(-50%) translateY(0); }
  .toast.error { background: var(--coral); color: #fff; }
</style>
