<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listDocs, uploadPdf, deleteDoc } from '../api'

const file = ref(null)
const uploading = ref(false)
const docs = ref([])
const loading = ref(false)

function onFileChange(uploadFile) {
  file.value = uploadFile.raw      // el-upload 包装对象 .raw 才是原生 File
}
function onFileRemove() {
  file.value = null
}

async function handleUpload() {
  if (!file.value) return ElMessage.warning('先选择 PDF 文件')
  uploading.value = true
  try {
    const res = await uploadPdf(file.value)
    ElMessage.success(`入库成功: ${res.chunk_count} 个切片`)
    file.value = null
    await loadDocs()
  } catch (e) {
    ElMessage.error('入库失败: ' + e.message)
  } finally {
    uploading.value = false
  }
}

async function loadDocs() {
  loading.value = true
  try { docs.value = await listDocs() } finally { loading.value = false }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确认删除「${row.filename}」? chroma 向量和 MySQL 记录会一并移除`, '警告', { type: 'warning' })
  } catch { return }               // 用户点了取消, 静默返回
  try {
    await deleteDoc(row.doc_id)
    ElMessage.success('已删除')
    await loadDocs()
  } catch (e) {
    ElMessage.error('删除失败: ' + e.message)
  }
}

onMounted(loadDocs)
</script>

<template>
  <div>
    <el-card shadow="never" class="mb">
      <template #header>上传文档</template>
      <div class="upload-row">
        <el-upload :auto-upload="false" :limit="1" accept=".pdf"
                   :on-change="onFileChange" :on-remove="onFileRemove">
          <el-button>选择 PDF</el-button>
        </el-upload>
        <el-button type="primary" :loading="uploading" @click="handleUpload">上传入库</el-button>
      </div>
      <p class="tip">首次上传会加载 embedding 模型(约 100MB), 耐心等 1~2 分钟</p>
    </el-card>

    <el-card shadow="never">
      <template #header>已入库文档</template>
      <el-table :data="docs" v-loading="loading" empty-text="还没有文档, 先上传一份">
        <el-table-column prop="filename" label="文件名" />
        <el-table-column prop="chunk_count" label="切片数" width="100" />
        <el-table-column prop="created_at" label="入库时间" width="180" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.mb { margin-bottom: 16px; }
.upload-row { display: flex; gap: 12px; align-items: center; }
.tip { margin-top: 12px; color: #999; font-size: 12px; }
</style>
