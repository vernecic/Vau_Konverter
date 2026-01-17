<script setup>
import { ref } from 'vue'
import axios from 'axios'

const file = ref(null)
const uploadedFile = ref(null)

const openInput = () => {
  file.value.click()
}
const uploadFile = () => {
  uploadedFile.value = file.value.files[0]
}

const URL = 'http://127.0.0.1:5000/upload'
const data = ref(null)

const fileUploadUrl = ref('')

const convertFile = async () => {
  try {
    const response = await axios.post(URL)
    data.value = response.data
    fileUploadUrl.value = data.value.upload_url
    console.log(fileUploadUrl.value)
  } catch (error) {
    console.log(error)
  }
}
</script>
<template>
  <div
    class="bg-linear-to-l from-zinc-300 to-zinc-400 min-h-screen flex justify-center items-center flex-col font-inter text-slate-800"
  >
    <div class="text-5xl 0 font-bold">VauKonverter</div>
    <p class="mt-2">
      Easily convert your <span class="text-slate-900 font-semibold">.mp3</span> files to
      <span class="text-slate-900 font-semibold">.wav</span>
    </p>
    <div
      class="flex flex-col gap-4 items-center border border-slate-600 rounded-xl border-dashed p-10 mt-5 w-[600px]"
    >
      <img src="/public/upload.svg" class="w-40" />
      <input class="hidden" type="file" ref="file" accept=".mp3" @change="uploadFile" />
      <button
        class="py-2 px-4 rounded-lg font-semibold border-slate-500 border-2 hover:bg-slate-500 transition duration-200 cursor-pointer"
        @click="openInput"
      >
        Upload your .mp3 file
      </button>
      <div v-if="uploadedFile" class="flex flex-col">
        <p class="flex gap-2">
          <span class="font-bold">File chosen: </span> {{ uploadedFile.name }}
        </p>
        <button
          class="border-2 border-[#5985E1] rounded-lg py-1 font-semibold px-2 mt-2 hover:bg-[#5985E1] hover:text-white transition duration-200 cursor-pointer"
          @click="convertFile"
        >
          Convert to .wav
        </button>
      </div>
    </div>
  </div>
</template>
