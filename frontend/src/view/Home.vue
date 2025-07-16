<script setup>
import { ref } from 'vue'

// State
const selectedInputType = ref('')
const isJudi = ref(true)

// Methods
const handleInputType = (type) => {
  selectedInputType.value = type
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
          @click="handleInputType('text')"
        >
          Teks
        </button>
        <button
          class="p-4 border-t-2 border-b-2 border-blue-700 hover:bg-blue-700 hover:text-white"
          :class="selectedInputType === 'image' ? 'bg-blue-700 text-white' : 'bg-white'"
          @click="handleInputType('image')"
        >
          Gambar
        </button>
        <button
          class="p-4 rounded-r border-2 border-blue-700 hover:bg-blue-700 hover:text-white"
          :class="selectedInputType === 'video' ? 'bg-blue-700 text-white' : 'bg-white'"
          @click="handleInputType('video')"
        >
          Video
        </button>
      </div>
      <div class="flex flex-col gap-4">
        <div class="text-xl font-semibold">Upload Gambar atau Masukkan URL</div>
        <input type="file" name="" id="" class="border-2 rounded w-1/2" />
        <input
          type="text"
          name=""
          id=""
          placeholder="URL gambar (jpg/png/webp"
          class="border-2 rounded w-1/2 p-1"
        />
      </div>
      <div class="flex">
        <button class="font-bold text-white rounded bg-blue-700 p-4">Deteksi Sekarang</button>
      </div>
    </div>
    <div class="grid gap-8 px-4 py-8 rounded-xl bg-white shadow-lg">
      <div class="text-xl font-semibold">Hasil Deteksi :</div>
      <div class="flex">
        <div class="text-xl font-semibold me-2">Status :</div>
        <div class="text-xl text-red-600" v-if="!isJudi">❌ Terindikasi Iklan Judi</div>
        <div class="text-xl text-green-600" v-else>✔️ Tidak Terindikasi Iklan Judi</div>
      </div>
      <div class="flex">
        <div class="text-xl font-semibold me-2">Kepastian :</div>
        <div class="text-xl">94%</div>
      </div>
      <div class="flex">
        <div class="text-xl font-semibold me-2">Kata Kunci :</div>
      </div>
    </div>

    <!-- <div class="mt-8">
      <div v-if="selectedInputType === 'text'">Form input teks di sini...</div>
      <div v-else-if="selectedInputType === 'image'">Upload gambar di sini...</div>
      <div v-else-if="selectedInputType === 'video'">Upload video di sini...</div>
    </div> -->
  </div>
</template>
