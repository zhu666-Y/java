<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCurrentUser, logoutUser } from '../utils/users'

const router = useRouter()
const username = ref('')
const loading = ref(true)

onMounted(async () => {
  // 登录态校验：向后端 /me 验活，未登录则跳回登录页
  const res = await getCurrentUser()
  loading.value = false
  if (!res.ok || res.code === 401) {
    router.replace('/login')
    return
  }
  username.value = res.data?.username || sessionStorage.getItem('spongebob-user') || ''
})

async function logout() {
  // 通知后端使会话失效（前端本地存储一并清理，双保险）
  await logoutUser()
  sessionStorage.removeItem('spongebob-user')
  router.push('/login')
}
</script>

<template>
  <div class="card" v-if="!loading">
    <div class="avatar">🪼</div>
    <h1>欢迎回来，{{ username }}！</h1>
    <p class="subtitle">今天的比奇堡天气晴朗，适合抓水母～</p>

    <div class="ocean">
      <span>🌊</span><span>🐚</span><span>🦀</span><span>🐠</span><span>⭐</span><span>🐙</span>
    </div>

    <button class="btn" @click="logout">退 出 登 录 🏠</button>

    <p class="footer">海绵宝宝 · 比奇堡海底世界</p>
  </div>
</template>

<style scoped>
  /* 主页卡片：与登录页同风格 */
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
    font-size: 22px;
    letter-spacing: 1px;
    margin-bottom: 4px;
    text-shadow: 1px 1px 0 var(--sponge-yellow-deep);
    word-break: break-all;
  }
  .subtitle { color: var(--sea-mid); font-size: 13px; margin-bottom: 22px; }

  .ocean {
    display: flex;
    justify-content: center;
    gap: 12px;
    font-size: 32px;
    margin-bottom: 26px;
  }
  .ocean span { animation: float 2.5s ease-in-out infinite; }
  .ocean span:nth-child(2) { animation-delay: .3s; }
  .ocean span:nth-child(3) { animation-delay: .6s; }
  .ocean span:nth-child(4) { animation-delay: .9s; }
  .ocean span:nth-child(5) { animation-delay: 1.2s; }
  .ocean span:nth-child(6) { animation-delay: 1.5s; }
  @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }

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

  .footer { margin-top: 18px; font-size: 12px; color: var(--sea-mid); }
</style>
