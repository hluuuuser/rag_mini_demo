<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { ask } from '../api'

const question = ref('')
const asking = ref(false)
const answer = ref('')
const sources = ref([])

async function handleAsk() {
  const q = question.value.trim()
  if (!q) return ElMessage.warning('先输入问题')
  asking.value = true
  answer.value = ''
  sources.value = []
  try {
    const res = await ask(q)
    answer.value = res.answer
    sources.value = res.sources
  } catch (e) {
    ElMessage.error('请求失败: ' + e.message)
  } finally {
    asking.value = false
  }
}
</script>

<template>
  <el-card shadow="never">
    <template #header>向知识库提问</template>

    <div class="ask-row">
      <el-input v-model="question" placeholder="例如: 什么是操作系统?"
                @keyup.enter="handleAsk" clearable />
      <el-button type="primary" :loading="asking" @click="handleAsk">提问</el-button>
    </div>

    <div v-if="answer" class="result">
      <h4>回答</h4>
      <p class="answer-text">{{ answer }}</p>

      <h4 v-if="sources.length">引用来源</h4>
      <div class="sources">
        <el-card v-for="s in sources" :key="s.index" shadow="hover" class="source-card">
          <template #header>
            <div class="source-head">
              <el-tag size="small" type="info">来源 {{ s.index }}</el-tag>
              <span class="source-meta">第 {{ s.page }} 页 · 相关度 {{ s.score }}</span>
            </div>
          </template>
          {{ s.text }}
        </el-card>
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.ask-row { display: flex; gap: 12px; }
.result { margin-top: 20px; }
.answer-text { white-space: pre-wrap; line-height: 1.8; }
.sources { display: flex; flex-direction: column; gap: 12px; }
.source-card { border-left: 3px solid #409eff; }
.source-head { display: flex; align-items: center; gap: 10px; }
.source-meta { color: #999; font-size: 12px; }
</style>
