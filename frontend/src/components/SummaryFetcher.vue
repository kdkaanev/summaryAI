<template>
  <div class="max-w-xl mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">AI Обобщаване Кънчо</h1>
    <input
      v-model="url"
      type="text"
      placeholder="Въведи линк..."
      class="border p-2 w-full rounded mb-4"
    />
    <button
      @click="fetchSummary"
      :disabled="loading"
      class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
    >
      {{ loading ? 'Генерирам...' : 'Обобщи' }}
    </button>

    <div v-if="error" class="text-red-500 mt-4">{{ error }}</div>

    <div v-if="summary" class="mt-4 p-3 border rounded bg-gray-50">
      <h2 class="font-semibold mb-2">Резюме:</h2>
      <p>{{ summary }}</p>
      <article>


        <p class="text-sm text-gray-500 mt-2" v-for="point in key_points" :key="point">
          - {{ point }}
        </p>

      </article>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SummaryFetcher',
  data() {
    return {
      url: '',
      summary: '',
      key_points: [
      ],
      loading: false,
      error: ''
    }
  },
  methods: {
    async fetchSummary() {
      this.error = ''
      this.summary = ''
      if (!this.url.trim()) {
        this.error = 'Моля, въведи валиден линк.'
        return
      }
      try {
        this.loading = true
        const res = await axios.post('https://summaryai-6tu0.onrender.com/api/summarize/', {
          url: this.url
        })
        this.summary = res.data.summary
        this.key_points = res.data.key_points || []
      } catch (err) {
        this.error = err.response?.data?.error || 'Възникна грешка при заявката.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
input:disabled,
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
