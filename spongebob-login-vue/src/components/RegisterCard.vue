<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '../utils/users'

const router = useRouter()

// 表单状态
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const isSubmitting = ref(false)

// 提示
const showToast = ref(false)
const isError = ref(false)
const toastMessage = ref('')
let toastTimer = null

function showToastMsg(message, error = false, duration = 2600) {
  toastMessage.value = message
  isError.value = error
  showToast.value = true
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (showToast.value = false), duration)
}

async function onSubmit() {
  const name = username.value.trim()

  // 前端校验
  if (name.length < 2) {
    showToastMsg('名字至少要 2 个字哦～', true)
    return
  }
  if (password.value.length < 6) {
    showToastMsg('密码至少 6 位，像蟹堡秘方一样保密！', true)
    return
  }
  if (password.value !== confirmPassword.value) {
    showToastMsg('两次输入的密码不一样啦～', true)
    return
  }

  if (isSubmitting.value) return // 防重复提交

  isSubmitting.value = true
  try {
    // 注册：调用 Spring Boot 后端（用户名查重 + 入库 MySQL）
    const res = await registerUser({ username: name, password: password.value })
    if (!res.ok) {
      showToastMsg(res.message, true)
      return
    }

    // 成功：提示后跳回登录页
    showToastMsg('🎉 ' + res.message)
    setTimeout(() => router.push('/login'), 1600)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="card">
    <div class="avatar">⭐</div>
    <h1>和派大星一起注册</h1>
    <p class="subtitle">加入比奇堡，成为海底的一员！</p>

    <form @submit.prevent="onSubmit">
      <div class="field">
        <label for="reg-username">用户名</label>
        <span class="icon">🍍</span>
        <input
          v-model="username"
          type="text"
          id="reg-username"
          placeholder="给自己起个海底名字"
          maxlength="20"
          autocomplete="username"
          required
        />
      </div>

      <div class="field">
        <label for="reg-password">密码</label>
        <span class="icon">🔑</span>
        <input
          v-model="password"
          type="password"
          id="reg-password"
          placeholder="至少 6 位，别告诉痞老板"
          maxlength="50"
          autocomplete="new-password"
          required
        />
      </div>

      <div class="field">
        <label for="reg-confirm">确认密码</label>
        <span class="icon">🔒</span>
        <input
          v-model="confirmPassword"
          type="password"
          id="reg-confirm"
          placeholder="再输一遍密码"
          maxlength="50"
          autocomplete="new-password"
          required
        />
      </div>

      <div class="row">
        <label class="remember"><input type="checkbox" /> 我已阅读《比奇堡公约》</label>
      </div>

      <button type="submit" class="btn" :disabled="isSubmitting">
        {{ isSubmitting ? '注 册 中 …' : '注 册 🌟' }}
      </button>
    </form>

    <p class="footer">已经有账号了？ <router-link to="/login">回海底登录</router-link></p>

    <div class="toast" :class="{ show: showToast, error: isError }">{{ toastMessage }}</div>
  </div>
</template>

<style scoped>
  /* 注册卡片（与登录页同风格） */
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
    font-size: 24px;
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
