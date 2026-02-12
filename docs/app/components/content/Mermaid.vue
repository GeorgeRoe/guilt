<script setup lang="ts">
import mermaid from 'mermaid'

const diagramId = `mermaid-${Math.random().toString(36).substr(2, 9)}`
const renderedSvg = ref('')
const error = ref(false)
const contentRef = ref<HTMLElement | null>(null)

async function renderDiagram() {
  if (!contentRef.value) return

  let content = contentRef.value.textContent || ''
  
  content = content.trim()

  if (!content) return

  try {
    mermaid.initialize({ 
      startOnLoad: false,
      theme: 'dark',
      securityLevel: 'loose',
    })

    const { svg } = await mermaid.render(diagramId, content)
    renderedSvg.value = svg
    error.value = false
  } catch (e) {
    error.value = true
  }
}

onMounted(() => {
  renderDiagram()
})
</script>

<template>
  <u-card
    v-if="renderedSvg"
    class="flex justify-center p-4"
    v-html="renderedSvg"
  />
  <u-alert v-else-if="error" color="error" title="Error rendering diagram" />
  <u-skeleton v-else class="h-12" />

  <div ref="contentRef" :style="{ display: 'none' }">
    <slot />
  </div>
</template>