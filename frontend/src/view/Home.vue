<script setup>
import { ref } from 'vue'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

// State
const selectedInputType = ref('')
const inputText = ref('')
const result = ref(null)
const imageFile = ref(null)
const imagePreview = ref(null)
const isDetec = ref(false)

// Methods
const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

const handleDetect = async () => {
  const toastLoading = toast.loading('Loading...')
  result.value = null
  isDetec.value = true
  toastLoading

  if (selectedInputType.value === 'text') {
    if (!inputText.value.trim()) return

    const res = await fetch('/api/detect-text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: inputText.value }),
    })

    result.value = await res.json()
    isDetec.value = false
    toast.success('Deteksi Selesai')
    toast.remove(toastLoading)
  } else if (selectedInputType.value === 'image') {
    if (!imageFile.value) return alert('Pilih gambar terlebih dahulu.')

    const formData = new FormData()
    formData.append('image', imageFile.value)

    const res = await fetch('/api/detect-image', {
      method: 'POST',
      body: formData,
    })

    result.value = await res.json()
    isDetec.value = false
    toast.remove(toastLoading)
    toast.success('Deteksi Selesai')
  }
}
</script>

<template>
  <div class="text-black">
    <div class="text-2xl font-bold mb-4">Deteksi Iklan Judi Online</div>

    <div class="grid gap-8 px-4 py-8 mb-8 rounded-xl bg-white shadow-lg">
      <div class="text-xl font-semibold">Pilih Jenis Input</div>
      <div class="flex font-bold text-blue-700">
        <button
          class="p-4 rounded-l border-2 border-blue-700 hover:bg-blue-700 hover:text-white"
          :class="selectedInputType === 'text' ? 'bg-blue-700 text-white' : 'bg-white'"
          @click="selectedInputType = 'text'"
        >
          Teks
        </button>
        <button
          class="p-4 border-t-2 border-b-2 border-blue-700 hover:bg-blue-700 hover:text-white"
          :class="selectedInputType === 'image' ? 'bg-blue-700 text-white' : 'bg-white'"
          @click="selectedInputType = 'image'"
        >
          Gambar
        </button>
        <button
          class="p-4 rounded-r border-2 border-blue-700 hover:bg-blue-700 hover:text-white"
          :class="selectedInputType === 'video' ? 'bg-blue-700 text-white' : 'bg-white'"
        >
          Video
        </button>
      </div>

      <div v-if="selectedInputType === 'text'" class="flex flex-col gap-4">
        <textarea
          v-model="inputText"
          rows="4"
          placeholder="Masukkan teks untuk deteksi"
          class="border-2 rounded p-2 w-full"
        ></textarea>
      </div>

      <div v-if="selectedInputType === 'image'" class="flex flex-col gap-4">
        <input type="file" @change="handleImageUpload" accept="image/*" />
        <div v-if="imagePreview">
          <img :src="imagePreview" class="max-w-md mt-4 rounded shadow" />
        </div>
      </div>

      <div class="flex">
        <button
          v-if="!isDetect"
          @click="handleDetect"
          class="font-bold text-white rounded bg-blue-700 p-4"
        >
          Deteksi Sekarang
        </button>
        <button
          v-else
          disabled
          @click="handleDetect"
          class="font-bold text-white rounded bg-blue-700 p-4"
        >
          Deteksi Sekarang
        </button>
      </div>
    </div>

    <div v-if="result" class="grid gap-8 px-4 py-8 rounded-xl bg-white shadow-lg">
      <div class="text-xl font-semibold">Hasil Deteksi :</div>
      <div class="flex">
        <div class="text-xl font-semibold me-2">Status :</div>
        <div
          class="text-xl"
          :class="result.raw_confidence > 0.5 ? 'text-red-600' : 'text-green-600'"
        >
          {{
            result.raw_confidence > 0.5
              ? '❌ Terindikasi Iklan Judi'
              : '✔️ Tidak Terindikasi Iklan Judi'
          }}
        </div>
      </div>
      <div class="flex">
        <div class="text-xl font-semibold me-2">Kepastian :</div>
        <div class="text-xl">{{ result.confidence }}</div>
      </div>
    </div>
  </div>
</template>
