<template>
  <div class="page">
    <header class="topbar">
      <span class="brand">RAG 知识库问答</span>
      <nav>
        <RouterLink to="/chat" class="nav-link">聊天问答</RouterLink>
        <RouterLink to="/knowledge" class="nav-link">知识库</RouterLink>
      </nav>
    </header>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #f5f7fa; font-family: system-ui, sans-serif; }
.page { max-width: 960px; margin: 0 auto; padding: 16px; }
.topbar { display: flex; justify-content: space-between; align-items: center; padding: 12px 4px; }
.brand { font-size: 18px; font-weight: 600; }
.nav-link { margin-left: 16px; color: #666; text-decoration: none; padding: 6px 12px; border-radius: 6px; }
.nav-link.router-link-active { background: #409eff; color: #fff; }
.content { margin-top: 8px; }
</style>
