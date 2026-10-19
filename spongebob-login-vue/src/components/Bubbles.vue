<script setup>
import { ref, onMounted } from 'vue'

// 在挂载时随机生成气泡参数，保持与原网页一致的效果
const bubbles = ref([])

onMounted(() => {
  const count = 18
  const arr = []
  for (let i = 0; i < count; i++) {
    const size = 6 + Math.random() * 22
    arr.push({
      width: size + 'px',
      height: size + 'px',
      left: Math.random() * 100 + '%',
      duration: (6 + Math.random() * 8) + 's',
      delay: (Math.random() * 6) + 's'
    })
  }
  bubbles.value = arr
})
</script>

<template>
  <div class="bubbles">
    <div
      v-for="(b, i) in bubbles"
      :key="i"
      class="bubble"
      :style="{
        width: b.width,
        height: b.height,
        left: b.left,
        animationDuration: b.duration,
        animationDelay: b.delay
      }"
    ></div>
  </div>
</template>

<style scoped>
  /* 上升的气泡 */
  .bubbles { position: absolute; inset: 0; pointer-events: none; }
  .bubble {
    position: absolute;
    bottom: -60px;
    background: var(--bubble);
    border-radius: 50%;
    opacity: 0.5;
    animation: rise linear infinite;
  }
  @keyframes rise {
    0%   { transform: translateY(0) translateX(0) scale(1); opacity: 0.5; }
    100% { transform: translateY(-110vh) translateX(30px) scale(1.3); opacity: 0; }
  }
</style>
