// 后端地址: 8000 是 FastAPI。CORS 已在后端全放开, 前端直接跨域调
const BASE = 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const resp = await fetch(BASE + path, options)
  if (!resp.ok) {
    let msg = `HTTP ${resp.status}`
    try { msg = (await resp.json()).detail || msg } catch { /* 非 JSON 响应 */ }
    throw new Error(msg)
  }
  return resp.json()
}

export function listDocs() {
  return request('/api/documents')
}

export function uploadPdf(file) {
  const form = new FormData()
  form.append('file', file)          // 字段名要和后端 UploadFile 参数一致
  return request('/api/documents', { method: 'POST', body: form })
}

export function deleteDoc(docId) {
  return request('/api/documents/' + docId, { method: 'DELETE' })
}

export function ask(question) {
  return request('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
}
