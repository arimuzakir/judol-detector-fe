<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

// API BASE URL
const baseUrl = import.meta.env.VITE_API_BASE_URL

// State
const selectedInputType = ref('text')
const inputText = ref('')
const result = ref(null)
const imageFile = ref(null)
const videoFile = ref(null)
const imagePreview = ref(null)
const isDetec = ref(false)
const textInput = ref(null)
const detectionTime = ref(null)
const fileInfo = ref(null)

// Methods
const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

onMounted(() => {
  if (selectedInputType.value === 'text') {
    focusTextInput()
  }
})

const focusTextInput = () => {
  nextTick(() => {
    textInput.value?.focus()
  })
}

const handleVideoUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  videoFile.value = file
}

const handleDetect = async () => {
  const toastLoading = toast.loading('Loading...')
  result.value = null
  detectionTime.value = null
  fileInfo.value = null
  isDetec.value = true

  const startTime = performance.now()

  try {
    if (selectedInputType.value === 'text') {
      if (!inputText.value.trim()) {
        toast.error('Masukkan teks terlebih dahulu.')
        return
      }
      console.log('base url : ', baseUrl)
      console.log(import.meta.env.VITE_API_BASE_URL)

      const res = await fetch(`${baseUrl}/detect-text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText.value }),
      })

      if (!res.ok) throw new Error('Gagal deteksi teks')
      result.value = await res.json()
    } else if (selectedInputType.value === 'image') {
      if (!imageFile.value) {
        toast.error('Pilih gambar terlebih dahulu.')
        return
      }

      const formData = new FormData()
      formData.append('image', imageFile.value)

      const res = await fetch(`${baseUrl}/detect-image`, {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) throw new Error('Gagal deteksi gambar')
      result.value = await res.json()

      fileInfo.value = {
        name: imageFile.value.name,
        size: (imageFile.value.size / 1024 / 1024).toFixed(2) + ' MB',
      }
    } else if (selectedInputType.value === 'video') {
      if (!videoFile.value) {
        toast.error('Pilih video terlebih dahulu.')
        return
      }

      const formData = new FormData()
      formData.append('video', videoFile.value)

      const res = await fetch(`${baseUrl}/detect-video`, {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) throw new Error('Gagal deteksi video')
      result.value = await res.json()

      fileInfo.value = {
        name: videoFile.value.name,
        size: (videoFile.value.size / 1024 / 1024).toFixed(2) + ' MB',
      }
    }

    const endTime = performance.now()
    detectionTime.value = ((endTime - startTime) / 1000).toFixed(2) + ' detik'

    toast.success('Deteksi Selesai')
  } catch (error) {
    console.error(error)
    toast.error('Terjadi kesalahan saat mendeteksi.')
  } finally {
    isDetec.value = false
    toast.remove(toastLoading)
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
          class="p-2 rounded-l border-2 border-blue-700 hover:bg-blue-700 hover:text-white"
          :class="selectedInputType === 'text' ? 'bg-blue-700 text-white' : 'bg-white'"
          @click="
            () => {
              selectedInputType = 'text'
              focusTextInput()
            }
          "
        >
          Teks
        </button>
        <button
          class="p-2 border-t-2 border-b-2 border-blue-700 hover:bg-blue-700 hover:text-white"
          :class="selectedInputType === 'image' ? 'bg-blue-700 text-white' : 'bg-white'"
          @click="selectedInputType = 'image'"
        >
          Gambar
        </button>
        <button
          class="p-2 rounded-r border-2 border-blue-700 hover:bg-blue-700 hover:text-white"
          :class="selectedInputType === 'video' ? 'bg-blue-700 text-white' : 'bg-white'"
          @click="selectedInputType = 'video'"
        >
          Video
        </button>
      </div>

      <div v-if="selectedInputType === 'text'" class="flex flex-col gap-4">
        <textarea
          ref="textInput"
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

      <div v-if="selectedInputType === 'video'" class="flex flex-col gap-4">
        <input type="file" accept="video/*" @change="handleVideoUpload" />
      </div>

      <div class="flex">
        <button
          :disabled="isDetec"
          @click="handleDetect"
          class="font-bold text-white rounded bg-blue-700 p-2 flex items-center gap-2 transition"
          :class="isDetec ? 'cursor-not-allowed opacity-70' : 'cursor-pointer hover:bg-blue-800'"
        >
          <svg
            v-if="isDetec"
            class="animate-spin h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
          </svg>
          <span>{{ isDetec ? 'Sedang Memproses...' : 'Deteksi Sekarang' }}</span>
        </button>
      </div>
    </div>

    <div v-if="result" class="grid gap-8 px-4 py-8 rounded-xl bg-white shadow-lg">
      <div class="text-xl font-semibold">Hasil Deteksi :</div>
      <div class="flex">
        <div class="text-xl font-semibold me-2">Status :</div>
        <div
          class="text-xl"
          :class="
            result?.raw_confidence != null
              ? result.raw_confidence > 0.5
                ? 'text-red-600'
                : 'text-green-600'
              : 'text-yellow-500'
          "
        >
          {{
            result?.raw_confidence != null
              ? result.raw_confidence > 0.5
                ? '❌ Terindikasi Iklan Judi'
                : '✔️ Tidak Terindikasi Iklan Judi'
              : '⚠️ Teks tidak ditemukan'
          }}
        </div>
      </div>
      <div class="flex">
        <div class="text-xl font-semibold me-2">Persentase Kata Judi Online :</div>
        <div class="text-xl">{{ result.confidence }}</div>
      </div>
      <div v-if="fileInfo" class="flex flex-col text-lg gap-2">
        <div><strong>Nama File:</strong> {{ fileInfo.name }}</div>
        <div><strong>Ukuran File:</strong> {{ fileInfo.size }}</div>
      </div>

      <div v-if="detectionTime" class="text-lg">
        <strong>Waktu Proses:</strong> {{ detectionTime }}
      </div>
    </div>
  </div>
</template>
