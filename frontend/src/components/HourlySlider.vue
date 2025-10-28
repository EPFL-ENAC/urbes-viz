<template>
  <div class="pb-8">
    <div class="slider-container">
      <v-btn class="play-button" density="compact" flat @click="togglePlay">{{
        playing ? 'Pause' : 'Play'
      }}</v-btn>
    </div>
    <div id="slider-hourly" ref="sliderHTML" class="slider-styled" />
  </div>
</template>

<script setup lang="ts">
import noUiSlider, { PipsMode, type API } from 'nouislider'
import 'nouislider/dist/nouislider.css'

import { defineModel, onUnmounted, onMounted, ref } from 'vue'

const sliderHTML = ref<HTMLDivElement | null>(null)
const slider = ref<API | null>(null)
const playing = ref(false)
const modelValue = defineModel<number>({ required: true })

const emit = defineEmits<{
  (e: 'playing', value: boolean): void
}>()

let playInterval: any

// Support fractional hours for smooth interpolation
const STEPS_PER_HOUR = 12
const MAX_VALUE = 23 + (STEPS_PER_HOUR - 1) / STEPS_PER_HOUR // 23.9 for 10 steps

const formatHour = {
  to: (value: number) => {
    const hours = Math.floor(value)
    const minutes = Math.round((value - hours) * 60)
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
  },
  from: (value: string) => {
    const [hours, minutes] = value.split(':').map(Number)
    return hours + minutes / 60
  }
}

const formatHourSimple = {
  to: (value: number) => {
    const hour = Math.floor(value)
    // Only show labels at whole hours
    return value % 1 === 0 && hour % 3 === 0 ? `${hour.toString().padStart(2, '0')}h` : ''
  },
  from: (value: string) => {
    return parseInt(value.replace('h', ''))
  }
}

const formatNumber = {
  to: (value: number) => {
    return Math.round(value * 100) / 100 // Keep 2 decimal places
  },
  from: (value: string) => {
    return Number(value)
  }
}

const createSlider = () => {
  if (!sliderHTML.value) return
  slider.value = noUiSlider.create(sliderHTML.value, {
    start: modelValue.value,
    tooltips: [formatHour],
    format: formatNumber,
    range: {
      min: 0,
      max: MAX_VALUE
    },
    step: 1 / STEPS_PER_HOUR, // Sub-hour steps for smooth interpolation
    pips: {
      mode: PipsMode.Steps,
      filter: (value: number) => {
        // Show pip marks at whole hours divisible by 3
        return value % 1 === 0 && value % 3 === 0 ? 1 : 0
      },
      format: formatHourSimple
    }
  })

  slider.value.on('update', (value) => {
    const numValue = Number(value)
    if (!isNaN(numValue)) modelValue.value = numValue
  })
}

const play = () => {
  if (playing.value) return
  playing.value = true
  emit('playing', true)

  playInterval = setInterval(() => {
    if (slider.value) {
      const nextValue = modelValue.value + 1 / STEPS_PER_HOUR
      // Loop back to 0 after reaching max
      const wrappedValue = nextValue > MAX_VALUE ? 0 : nextValue
      slider.value.set(wrappedValue)
    }
  }, 50) // 100ms per frame = smooth 10fps animation
}

const stop = () => {
  playing.value = false
  emit('playing', false)
  clearInterval(playInterval)
}

const togglePlay = () => {
  playing.value ? stop() : play()
}

onMounted(createSlider)
onUnmounted(stop)
</script>

<style scoped>
.slider-container {
  position: relative;
  z-index: 100;
  padding-top: 25px;
}

.play-button {
  position: absolute;
  top: -35px;
  right: 0;
}

.slider-styled {
  width: 100%;
  height: 10px;
  padding: 0 0;
}

:deep().noUi-connect {
  background: #00aaff;
}

:deep().noUi-handle {
  height: 18px;
  width: 18px;
  top: -5px;
  right: -9px; /* half the width */
  border-radius: 9px;
}

:deep().noUi-handle:before,
:deep().noUi-handle:after {
  display: none;
}

:deep().noUi-pips {
  padding: 2px;
}
:deep().noUi-touch-area {
  padding: 15px;
  cursor: move;
}

:deep().noUi-value {
  padding-top: 4px;
}
</style>
