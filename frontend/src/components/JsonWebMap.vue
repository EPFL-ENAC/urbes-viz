<script setup lang="ts">
import MapLibreMap from '@/components/MapLibreMap.vue'

import type { Parameters } from '@/utils/jsonWebMap'
import { onMounted, ref, shallowRef, triggerRef, watch } from 'vue'

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
  'buildings-layer',
  'wrf-layer',
  'areas-layer',
  'roads-layer',
  'roads_swiss_statistics-layer',
  'roads_swiss_statistics_projection-layer',
  'gws_data-layer',
  'statpop_data-layer'
]

const layersSelected = ref<string[]>(['roads_swiss_statistics-layer'])

const syncAllLayersVisibility = (layersSelected: string[]) => {
  for (let layer of possibleLayers) {
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
</script>

<template>
  <v-container class="fill-height pa-0 overflow-hidden" fluid>
    <v-row class="fill-height overflow-y-hidden">
      <v-col cols="2" md="2" class="pl-6 params-col border-e-md overflow-y-auto overflow-x-hidden">
        <v-card flat>
          <v-card-title> Layers </v-card-title>
          <v-card-text>
            <v-checkbox
              v-for="(item, index) in possibleLayers"
              :key="index"
              v-model="layersSelected"
              density="compact"
              class="no-min-height"
              hide-details
              :label="item"
              :value="item"
            />
          </v-card-text>
        </v-card>
        <v-card flat>
          <v-card-title> Variables WRF data</v-card-title>
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
          ref="map"
          :center="center"
          :style-spec="styleUrl"
          :popup-layer-ids="parameters.popupLayerIds"
          :zoom="zoom"
          :max-zoom="20"
          :min-zoom="6"
          :idx-image="idxImage"
          :variable-selected="variableSelected"
          :callback-loaded="() => syncAllLayersVisibility(layersSelected)"
          class="flex-grow-1"
        />

        <v-card flat class="mt-auto border-t-md pb-4 px-4">
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
</style>
