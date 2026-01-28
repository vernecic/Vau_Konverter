<script setup>
import { ref } from 'vue'
import axios from 'axios'

const file = ref(null)
const uploadedFile = ref(null)

const downloadLink = ref('')
const downloadReady = ref(false)

const openInput = () => {
  file.value.click()
}
const uploadFile = () => {
  uploadedFile.value = file.value.files[0]
}

const URL = '/api/upload'
const data = ref(null)

const fileUploadUrl = ref('')

const convertFile = async () => {
  try {
    const response = await axios.post(URL)
    data.value = response.data
    fileUploadUrl.value = data.value.upload_url
    const fileId = data.value.file_id
    const mp3key = data.value.key

    const putResponse = await fetch(fileUploadUrl.value, {
      method: 'PUT',
      body: uploadedFile.value,
      headers: {
        'Content-Type': 'audio/mpeg',
      },
    })
    if (putResponse.ok) {
      console.log('Fajl je gore')
      const notifyBackend = await axios.post('/api/convert', { file_id: fileId, mp3_key: mp3key })

      downloadLink.value = notifyBackend.data.wav_url
      console.log('Download Link:', downloadLink.value)
      console.log('Konverzija gotova!')
      downloadReady.value = true
    }

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
      Easily convert your<span class="text-slate-900 font-semibold">.mp3</span> files to
      <span class="text-slate-900 font-semibold">.wav</span>
    </p>
    <div
      class="flex flex-col gap-4 items-center border border-slate-600 rounded-xl border-dashed p-10 mt-5 w-150"
    >
      <img src="/public/upload.svg" class="w-40" />
      <input class="hidden" type="file" ref="file" accept=".mp3" @change="uploadFile" />
      <button
        class="py-2 px-4 rounded-lg font-semibold border-slate-500 border-2 hover:bg-slate-500 transition duration-200 cursor-pointer"
        @click="openInput"
      >
        Upload your .mp3 file Dajte nam 5
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
      <div v-if="downloadReady">
        <a
          :href="downloadLink"
          download
          class="rounded-lg py-2 px-4 bg-green-500 text-white font-semibold"
          >Preuzmi .wav</a
        >
      </div>
    </div>
  </div>
</template>
