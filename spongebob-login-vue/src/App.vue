<script setup>
// 顶层布局：海底背景 + 装饰，路由出口渲染登录/注册页
import Bubbles from './components/Bubbles.vue'
</script>

<template>
  <div class="rays"></div>
  <Bubbles />
  <div class="star">⭐</div>
  <div class="pineapple">🍍</div>
  <div class="seabed"></div>

  <router-view />
</template>

<style scoped>
  /* 海底光线 */
  .rays {
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      115deg,
      rgba(255, 255, 255, 0.05) 0px,
      rgba(255, 255, 255, 0.05) 40px,
      transparent 40px,
      transparent 120px
    );
    pointer-events: none;
  }

  /* 海床 */
  .seabed {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 90px;
    background: linear-gradient(180deg, #e8c170 0%, #d4a843 100%);
    border-radius: 50% 50% 0 0 / 30px 30px 0 0;
    box-shadow: inset 0 8px 0 rgba(255,255,255,0.2);
  }

  /* 派大星（小装饰） */
  .star {
    position: absolute;
    bottom: 70px; left: 8%;
    font-size: 60px;
    filter: drop-shadow(0 4px 4px rgba(0,0,0,0.3));
    animation: wiggle 3s ease-in-out infinite;
  }
  .pineapple {
    position: absolute;
    bottom: 80px; right: 9%;
    font-size: 70px;
    filter: drop-shadow(0 4px 4px rgba(0,0,0,0.3));
    animation: sway 4s ease-in-out infinite;
  }
  @keyframes wiggle { 0%,100%{transform:rotate(-6deg)} 50%{transform:rotate(6deg)} }
  @keyframes sway   { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
</style>
