<script setup lang="ts">
import MapLibreMap from '@/components/MapLibreMap.vue'
import { useTheme } from 'vuetify'

import type { Parameters } from '@/utils/jsonWebMap'
import { computed, ref, shallowRef, watch } from 'vue'

const props = defineProps<{
  styleUrl: string
}>()

const map = ref<InstanceType<typeof MapLibreMap>>()

const parameters = shallowRef<Parameters>({})

const variableSelected = ref<string>('t2')

const idxImage = ref<number>(0)

const center = {
  lat: 46.882,
  lng: 8.1321
}

const zoom = 8

const possibleLayers = [
  { id: 'buildings-layer', label: 'Buildings Layer' },
  { id: 'wrf-layer', label: 'Weather Data (WRF)' },
  { id: 'areas-layer', label: 'Areas Layer' },
  { id: 'roads-layer', label: 'Roads Layer' },
  { id: 'roads_swiss_statistics-layer', label: 'Swiss Roads Statistics' },
  { id: 'roads_swiss_statistics_projection-layer', label: 'Projected Swiss Roads Statistics' },
  { id: 'gws_data-layer', label: 'GWS Data' },
  { id: 'statpop_data-layer', label: 'Statistical Population Data' }
]
const layersSelected = ref<string[]>(['roads_swiss_statistics-layer'])

const isWrfSelected = computed(() => layersSelected.value.includes('wrf-layer'))

const syncAllLayersVisibility = (layersSelected: string[]) => {
  for (let { id: layer } of possibleLayers) {
    if (layersSelected.includes(layer)) {
      map.value?.setLayerVisibility(layer, true)
    } else {
      map.value?.setLayerVisibility(layer, false)
    }
  }
}
watch(
  () => layersSelected.value,
  (layersSelected) => {
    console.log(layersSelected)
    syncAllLayersVisibility(layersSelected)
  }
)

const vuetifyTheme = useTheme()

const theme = ref('style/dark.json') // Default theme
const themes = [
  { value: 'style/light.json', label: 'Light' },
  { value: 'style/dark.json', label: 'Dark' },
  { value: 'style/none.json', label: 'None' }
]

watch(
  () => theme.value,
  (theme) => {
    vuetifyTheme.global.name.value = theme === 'style/light.json' ? 'light' : 'dark'
  }
)
</script>

<template>
  <v-container class="fill-height pa-0 overflow-hidden" fluid>
    <v-row class="fill-height overflow-y-hidden">
      <v-col cols="2" md="2" class="params-col border-e-md overflow-y-auto overflow-x-hidden">
        <v-card flat>
          <v-card-title class="ml-2"> <h2>LAYERS</h2> </v-card-title>
          <v-card-text class="d-flex flex-column">
            <v-checkbox
              v-for="(item, index) in possibleLayers"
              :key="index"
              v-model="layersSelected"
              class="py-4"
              hide-details
              :value="item.id"
            >
              <template #label>
                <h3>{{ item.label.toUpperCase() }}</h3>
              </template>
            </v-checkbox>
          </v-card-text>
        </v-card>
        <v-card v-if="isWrfSelected" class="mt-10" flat>
          <v-card-title> <h3>Variables WRF data</h3></v-card-title>
          <v-card-text>
            <v-radio-group v-model="variableSelected" hide-details>
              <v-radio label="U10" value="u10"></v-radio>
              <v-radio label="T2" value="t2"></v-radio>
            </v-radio-group>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col id="map-time-input-container" cols="10" md="10" class="py-0 pl-0 d-flex flex-column">
        <MapLibreMap
          :key="theme"
          ref="map"
          :center="center"
          :style-spec="theme"
          :popup-layer-ids="parameters.popupLayerIds"
          :zoom="zoom"
          :max-zoom="20"
          :min-zoom="6"
          :idx-image="idxImage"
          :variable-selected="variableSelected"
          :callback-loaded="() => syncAllLayersVisibility(layersSelected)"
          class="flex-grow-1"
        />
        <div class="theme-selector">
          <v-select
            v-model="theme"
            :items="themes"
            item-value="value"
            item-title="label"
            label="Theme"
            dense
            hide-details
            outlined
          />
        </div>

        <v-card v-if="isWrfSelected" flat class="mt-auto border-t-md pb-4 px-4">
          <v-card-title> Time </v-card-title>
          <v-card-text>
            <v-slider v-model="idxImage" :min="0" :max="41"></v-slider>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.v-slider-thumb__label span.thumb-label-nowrap {
  white-space: nowrap;
}

.params-col {
  max-height: 100vh;
}

.no-min-height {
  height: 32px;
}

.theme-selector {
  position: absolute;
  bottom: 16px;
  right: 16px;
  z-index: 1000;
}
</style>
