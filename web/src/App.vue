<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const templates = ref([])
const selectedId = ref('')
const values = ref({})
const copies = ref(1)
const preview = ref('')
const error = ref('')
const notice = ref('')
const busy = ref(false)
const previewBusy = ref(false)
const selected = computed(() => templates.value.find(item => item.id === selectedId.value))
const example = { 'storage-box': { title: 'WINTER DECOR', contents: 'Lights, ornaments, hooks', location: 'Garage / shelf 2' }, 'jar-can': { contents: 'PEACH JAM', date: '2026-09-26', note: 'Use by spring' }, 'todo-list': { title: 'WEEKEND JOBS', item1: 'Fix garden tap', item2: 'Sort garage', item3: 'Pick up soil' }, 'project-card': { project: 'PANTRY REFRESH', task: 'Sort upper shelves', owner: 'Rion', status: 'NEXT' } }

onMounted(async () => {
  try {
    const response = await fetch('/api/templates')
    if (!response.ok) throw new Error('Unable to load templates.')
    templates.value = (await response.json()).templates
    selectedId.value = templates.value[0]?.id || ''
  } catch (e) { error.value = e.message }
})

let timer
let previewRequest = 0
watch(selectedId, () => { previewRequest++; clearTimeout(timer); values.value = {}; preview.value = ''; previewBusy.value = false; error.value = ''; notice.value = '' })
watch(values, () => {
  previewRequest++
  clearTimeout(timer)
  if (!Object.values(values.value).some(Boolean)) { preview.value = ''; previewBusy.value = false }
  timer = setTimeout(() => updatePreview(previewRequest), 250)
}, { deep: true })

function payload() { return { template: selectedId.value, values: values.value, copies: Number(copies.value) } }
function useExample() { values.value = { ...example[selectedId.value] }; notice.value = ''; error.value = '' }
function clearFields() { values.value = {}; preview.value = ''; previewBusy.value = false; error.value = ''; notice.value = '' }
function clearField(id) {
  values.value[id] = ''
  error.value = ''
  notice.value = ''
  document.getElementById(`field-${id}`)?.focus()
}
function clear() { clearFields(); copies.value = 1 }

async function updatePreview(requestId) {
  if (!selected.value || !Object.values(values.value).some(Boolean)) { preview.value = ''; return }
  previewBusy.value = true
  try {
    const response = await fetch('/api/preview', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload()) })
    const svg = response.ok ? await response.text() : ''
    if (requestId === previewRequest) preview.value = svg
  } catch { if (requestId === previewRequest) preview.value = '' }
  finally { if (requestId === previewRequest) previewBusy.value = false }
}

async function printLabel() {
  if (busy.value) return
  busy.value = true; error.value = ''; notice.value = ''
  try {
    const response = await fetch('/api/print', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload()) })
    const result = await response.json()
    if (!response.ok) throw new Error(result.error || 'Could not print the label.')
    notice.value = `${result.copies} ${result.copies === 1 ? 'label' : 'labels'} sent to the printer.`
  } catch (e) { error.value = e.message }
  finally { busy.value = false }
}
</script>

<template>
  <div class="shell">
    <header class="topbar"><div class="brand"><span class="brand-icon">▧</span><span>ZeLabel</span></div><a class="account" href="/oauth2/sign_out">Sign out <span aria-hidden="true">↗</span></a></header>
    <main>
      <div class="intro"><div class="eyebrow">HOUSEHOLD PRINT STUDIO</div><h1>Make a label.</h1><p>Choose a layout, add your words, and send it to the Zebra printer.</p></div>
      <div class="workspace">
        <section class="editor" aria-labelledby="choose-heading">
          <div class="section-heading"><div><span class="step">01 / TEMPLATE</span><h2 id="choose-heading">What are you labeling?</h2></div></div>
          <div class="template-grid">
            <button v-for="item in templates" :key="item.id" type="button" class="template-card" :class="{ active: selectedId === item.id }" :aria-pressed="selectedId === item.id" @click="selectedId = item.id">
              <span class="card-top"><span class="card-category">{{ item.category }}</span><span class="card-size">{{ item.size }} in</span></span>
              <strong>{{ item.name }}</strong><span class="card-description">{{ item.description }}</span>
            </button>
          </div>
          <form v-if="selected" @submit.prevent="printLabel">
            <div class="section-heading content-heading"><div><span class="step">02 / CONTENT</span><h2>Make it yours.</h2></div><div class="content-actions"><button type="button" class="text-button" @click="useExample">Use example</button><button type="button" class="text-button" :disabled="!Object.values(values).some(Boolean)" @click="clearFields">Clear fields</button></div></div>
            <div class="fields"><div v-for="field in selected.fields" :key="field.id" class="field"><label :for="`field-${field.id}`">{{ field.label }} <span v-if="field.required" class="required">*</span></label><div class="input-wrap"><input :id="`field-${field.id}`" v-model="values[field.id]" type="text" :placeholder="field.placeholder" :maxlength="field.maxLength" :required="field.required" autocomplete="off"><button v-if="values[field.id]" type="button" class="field-clear" :aria-label="`Clear ${field.label}`" @click="clearField(field.id)"><span aria-hidden="true">×</span></button></div><small>{{ (values[field.id] || '').length }} / {{ field.maxLength }}</small></div></div>
            <div class="mobile-preview"><div class="preview-heading"><div><span class="step">LIVE PREVIEW</span><h2>Check your label.</h2></div><span class="preview-badge">{{ selected?.size }} in</span></div><div class="preview-stage"><div v-if="preview" class="preview-art" :class="{ square: selected?.size === '2×2' }" v-html="preview"></div><div v-else class="preview-empty">Add content to see your label.</div></div></div>
            <div class="actions"><label class="copies">Copies<select v-model.number="copies" aria-label="Number of copies"><option v-for="n in 10" :key="n" :value="n">{{ n }}</option></select></label><button type="button" class="clear" @click="clear">Clear</button><button class="print" type="submit" :disabled="busy">{{ busy ? 'Sending…' : 'Print label' }} <span aria-hidden="true">↗</span></button></div>
            <p v-if="error" class="message error" role="alert">{{ error }}</p><p v-if="notice" class="message success" role="status">{{ notice }}</p>
          </form>
        </section>
        <aside class="preview-panel"><div class="preview-heading"><div><span class="step">LIVE PREVIEW</span><h2>Ready to print.</h2></div><span class="preview-badge">{{ selected?.size || '—' }} in</span></div><div class="preview-stage"><div v-if="preview" class="preview-art" :class="{ square: selected?.size === '2×2' }" v-html="preview"></div><div v-else class="preview-empty"><span class="empty-icon">▧</span><strong>Your label will appear here</strong><span>Add content or tap “Use example” to see it.</span></div></div><p class="preview-note">{{ previewBusy ? 'Updating preview…' : 'Preview is approximate. Check the first physical print for alignment.' }}</p></aside>
      </div>
    </main><footer>ZeLabel <span>·</span> Made for the household</footer>
  </div>
</template>
