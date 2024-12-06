<script setup lang="ts">
import 'maplibre-gl/dist/maplibre-gl.css'
import LoadingCircle from '@/components/LoadingCircle.vue'
import LegendMap from '@/components/LegendMap.vue'

import {
  FullscreenControl,
  Map as Maplibre,
  NavigationControl,
  Popup,
  ScaleControl,
  VectorTileSource,
  type FilterSpecification,
  type LngLatLike,
  type StyleSetterOptions,
  type StyleSpecification,
  addProtocol
} from 'maplibre-gl'
import type { LegendColor } from '@/utils/legendColor'
import { computed, onMounted, ref, watch } from 'vue'

import { Protocol } from 'pmtiles'

const props = withDefaults(
  defineProps<{
    styleSpec: string | StyleSpecification
    center?: LngLatLike
    zoom?: number
    aspectRatio?: number
    minZoom?: number
    maxZoom?: number
    filterIds?: string[]
    popupLayerIds?: string[]
    areaLayerIds?: string[]
    idxImage?: number
    variableSelected?: string
    legendColors?: LegendColor[]
    continuousColor?: boolean
    callbackLoaded?: () => void
  }>(),
  {
    center: undefined,
    zoom: 12,
    idxImage: 0,
    variableSelected: 't2',
    aspectRatio: undefined,
    minZoom: undefined,
    maxZoom: undefined,
    filterIds: undefined,
    legendColors: undefined,
    callbackLoaded: undefined,
    popupLayerIds: () => [],
    areaLayerIds: () => []
  }
)

const loading = ref(true)
const container = ref<HTMLDivElement | null>(null)
let map: Maplibre | undefined = undefined
const hasLoaded = ref(false)
const protocol = new Protocol()

const popup = ref<Popup>(
  new Popup({
    closeButton: false,
    maxWidth: '800px'
  })
)

function displaySegmentTime(t0: number, t1: number) {
  // Start time of the recording
  const startTime = new Date('2018-10-24T08:30:00')

  // Calculate the midpoint in milliseconds
  const timestamp = (t0 + t1) / 2

  // Create a new date by adding the midpoint to the start time
  const segmentTime = new Date(startTime.getTime() + timestamp)

  // Format the time as hours:minutes
  let hours = segmentTime.getHours()
  let minutes = segmentTime.getMinutes()

  // Ensuring two-digit minutes format
  const displayMinutes = minutes < 10 ? '0' + minutes : minutes

  // Return the formatted time
  return `${hours}:${displayMinutes}`
}

const urlSource = computed(() => {
  const idx = ~~props.idxImage
  const id = idx.toLocaleString('en-US', {
    minimumIntegerDigits: 3,
    useGrouping: false
  })
  return `/geodata/output_images_${props.variableSelected}/${props.variableSelected}_${id}.png`
})

watch(urlSource, (url) => {
  if (map) {
    const source = map.getSource('wrf-data') as maplibregl.ImageSource
    source.updateImage({ url: url })
  }
})
addProtocol('pmtiles', protocol.tile)

onMounted(() => {
  // Find the base url depending on the environment
  // If dev it should be geodata/
  // If prod it should be https://enacit4r-cdn.epfl.ch/utnc-viz/
  const baseUrl = import.meta.env.DEV ? '/geodata' : 'https://enacit4r-cdn.epfl.ch/utnc-viz'

  addProtocol('pmtiles', protocol.tile)
  map = new Maplibre({
    container: container.value as HTMLDivElement,
    style: props.styleSpec,
    center: props.center,
    zoom: props.zoom,
    minZoom: props.minZoom,
    maxZoom: props.maxZoom,
    attributionControl: false
  })

  // map.showTileBoundaries = true
  map.addControl(new NavigationControl({}))
  map.addControl(new ScaleControl({}))
  map.addControl(
    new FullscreenControl({
      container: document.getElementById('map-time-input-container') ?? undefined
    })
  )

  // filterLayers(props.filterIds)

  let hoveredStateId: number = -1

  map.on('load', () => {
    // filterLayers(props.filterIds)
    if (!map) return
    hasLoaded.value = true
    loading.value = false
    map.resize()

    map.addSource('areas', {
      type: 'vector',
      url: `pmtiles://${baseUrl}/hoheitsgebiet.pmtiles`,
      minzoom: 5,
      maxzoom: 17
    })

    map.addLayer({
      id: 'areas-layer',
      type: 'fill', // or 'line', 'circle', etc., depending on your data
      source: 'areas',
      'source-layer': 'hoheitsgebiet'
    })

    map.addSource('roads_swiss_statistics', {
      type: 'vector',
      url: `pmtiles://${baseUrl}/roads_swiss_statistics.pmtiles`
    })

    map.addLayer({
      id: 'roads_swiss_statistics-layer',
      type: 'line',
      source: 'roads_swiss_statistics',
      'source-layer': 'roads_swiss_statistics',
      paint: {
        'line-color': [
          'interpolate',
          ['linear'],
          ['get', 'DWV_PW'], // Using DWV as the base metric for traffic intensity
          0,
          '#b0e0e6', // Light color for low traffic
          5000,
          '#4682b4', // Moderate traffic
          10000,
          '#ff4500', // High traffic
          20000,
          '#8b0000' // Very high traffic
        ],
        'line-width': [
          'interpolate',
          ['linear'],
          ['get', 'DTV_PW'], // Adjusting line width based on daily traffic volume
          0,
          0.5, // Thin lines for lower traffic
          5000,
          2,
          10000,
          4,
          20000,
          6
        ],
        'line-opacity': 0.8
      }
    })

    map.addSource('roads_swiss_statistics_projection', {
      type: 'vector',
      url: `pmtiles://${baseUrl}/roads_swiss_statistics_projection.pmtiles`
    })

    map.addLayer({
      id: 'roads_swiss_statistics_projection-layer',
      type: 'line',
      source: 'roads_swiss_statistics_projection',
      'source-layer': 'roads_swiss_statistics_projection',
      paint: {
        'line-color': [
          'interpolate',
          ['linear'],
          ['get', 'DWV_PW'], // Using DWV as the base metric for traffic intensity
          0,
          '#b0e0e6', // Light color for low traffic
          5000,
          '#4682b4', // Moderate traffic
          10000,
          '#ff4500', // High traffic
          20000,
          '#8b0000' // Very high traffic
        ],
        'line-width': [
          'interpolate',
          ['linear'],
          ['get', 'DTV_PW'], // Adjusting line width based on daily traffic volume
          0,
          0.5, // Thin lines for lower traffic
          5000,
          2,
          10000,
          4,
          20000,
          6
        ],
        'line-opacity': 0.8
      }
    })
    map.addSource('gws_data', {
      type: 'vector',
      url: `pmtiles://${baseUrl}/gws_grid.pmtiles`
    })

    map.addLayer({
      id: 'gws_data-layer',
      type: 'fill',
      source: 'gws_data',
      'source-layer': 'gws_grid_wgs84',
      paint: {
        'fill-opacity': 0.5,
        'fill-color': [
          'interpolate',
          ['linear'],
          ['get', 'GTOT'], // Color gradient based on total buildings with residential use
          0,
          '#e0f7fa', // Light blue for lower values
          10,
          '#4db6ac', // Moderate density of residential buildings
          25,
          '#00796b', // Higher density
          50,
          '#004d40' // Very high density
        ]
      }
    })

    map.addSource('statpop_data', {
      type: 'vector',
      url: `pmtiles://${baseUrl}/statpop_grid.pmtiles`
    })

    map.addLayer({
      id: 'statpop_data-layer',
      type: 'fill',
      source: 'statpop_data',
      'source-layer': 'statpop_grid_wgs84',
      paint: {
        'fill-opacity': 0.5,
        'fill-color': [
          'interpolate',
          ['linear'],
          ['get', 'B22BTOT'], // Color gradient based on total buildings with residential use
          0,
          '#e0f7fa', // Light blue for lower values
          10,
          '#4db6ac', // Moderate density of residential buildings
          25,
          '#00796b', // Higher density
          50,
          '#004d40' // Very high density
        ]
      }
    })

    map.addSource('wrf-data', {
      type: 'image',
      url: urlSource.value,
      coordinates: [
        [5.13211, 47.94587], // Top-left corner
        [11.12701, 47.94587], // Top-right corner
        [11.12701, 45.42068], // Bottom-right corner
        [5.13211, 45.42068] // Bottom-left corner
      ]
    })

    map.addLayer({
      id: 'wrf-layer',
      type: 'raster',
      source: 'wrf-data',
      paint: {
        'raster-opacity': 0.4
      }
    })

    // Add the vector tile source
    map.addSource('buildings', {
      type: 'vector',
      url: `pmtiles://${baseUrl}/buildings_swiss.pmtiles`,
      minzoom: 5
    })

    // Add the vector tile source
    map.addSource('roads', {
      type: 'vector',
      url: `pmtiles://${baseUrl}/roads_swiss.pmtiles`,
      minzoom: 5
    })

    // Add a layer to visualize the data
    map.addLayer({
      id: 'buildings-layer',
      type: 'fill', // or 'line', 'circle', etc., depending on your data
      source: 'buildings',
      'source-layer': 'buildings_swiss', // This should match the layer name inside the MBTiles
      paint: {
        'fill-color': [
          'interpolate',
          ['linear'],
          ['to-number', ['get', 'OBJORIG_YE']], // Converts the OBJORIG_YE property to a number
          1950,
          '#FF0000', // Red for older buildings (e.g., 1900)
          2000,
          '#FFFF00', // Yellow for mid-range buildings (e.g., 2000)
          2020,
          '#00FF00' // Green for newer buildings (e.g., 2020)
        ],
        'fill-opacity': 0.7 // Adjust the opacity to your preference
      }
    })

    map.addLayer({
      id: 'roads-layer',
      type: 'line', // or 'line', 'circle', etc., depending on your data
      source: 'roads',
      'source-layer': 'roads_swiss', // This should match the layer name inside the MBTiles
      paint: {
        'line-color': [
          'interpolate',
          ['linear'],
          ['to-number', ['get', 'OBJORIG_YE']], // Converts the OBJORIG_YE property to a number
          0,
          '#00FFFF', // Cyan for unknown year (e.g., 0)
          1950,
          '#FF0000', // Red for older buildings (e.g., 1900)
          2000,
          '#FFFF00', // Yellow for mid-range buildings (e.g., 2000)
          2020,
          '#00FF00' // Green for newer buildings (e.g., 2020)
        ],
        'line-opacity': 0.7 // Adjust the opacity to your preference
      }
    })

    function testTilesLoaded() {
      if (map?.areTilesLoaded()) {
        loading.value = false
      } else {
        loading.value = true
        setTimeout(testTilesLoaded, 1000)
      }
    }

    function handleDataEvent() {
      if (map?.areTilesLoaded()) {
        loading.value = false
      } else {
        testTilesLoaded()
      }
    }

    map.on('sourcedata', handleDataEvent)

    map.on('sourcedataloading', handleDataEvent)

    map.on('mouseleave', 'trajectories', () => {
      if (map) map.getCanvas().classList.remove('hovered-feature')
    })

    if (props.callbackLoaded) props.callbackLoaded()
  })
  loading.value = false
})

let throttleTimer = new Map<string, boolean>()

const throttle = (callback: () => void, id: string, time: number) => {
  if (throttleTimer.get(id)) {
    // If currently throttled, exit the function
    return
  }

  // Set the throttle flag
  throttleTimer.set(id, true)

  // Clear the throttle flag after the specified time
  setTimeout(() => {
    throttleTimer.set(id, false)
  }, time)
  callback()
}

const setFilter = (
  layerId: string,
  filter?: FilterSpecification | null | undefined,
  options?: StyleSetterOptions | undefined
) => {
  if (hasLoaded.value) {
    throttle(() => map?.setFilter(layerId, filter, options), layerId + '-filter', 100)
  }
}

const setPaintProperty = (
  layerId: string,
  name: string,
  value: any,
  options?: StyleSetterOptions | undefined
) => {
  if (hasLoaded.value)
    throttle(() => map?.setPaintProperty(layerId, name, value, options), layerId + '-paint', 100)
}

const queryFeatures = (filter: any[]) => {
  return map?.querySourceFeatures('trajectories', {
    sourceLayer: 'trajectories',
    filter: filter as FilterSpecification,
    validate: false
  })
}

const queryRenderedFeatures = () => {
  return map?.queryRenderedFeatures()
}

const onZoom = (callback: () => void) => {
  map?.on('zoom', callback)
}

const changeSourceTilesUrl = (sourceId: string, url: string) => {
  const source = map?.getSource(sourceId) as VectorTileSource
  source.setUrl(url)
}

const getSourceTilesUrl = (sourceId: string) => {
  const source = map?.getSource(sourceId) as VectorTileSource
  if (source && source.url) return source.url
  else return ''
}
const setLayerVisibility = (layerId: string, visibility: boolean) => {
  map?.setLayoutProperty(layerId, 'visibility', visibility ? 'visible' : 'none')
}

const getPaintProperty = (layerId: string, name: string) => {
  if (hasLoaded.value) return map?.getPaintProperty(layerId, name)
}

defineExpose({
  getPaintProperty,
  update,
  setFilter,
  queryFeatures,
  queryRenderedFeatures,
  setPaintProperty,
  onZoom,
  changeSourceTilesUrl,
  setLayerVisibility,
  getSourceTilesUrl,
  filterLayers
})

watch(
  () => props.styleSpec,
  (styleSpec) => {
    map?.setStyle(styleSpec)
  },
  { immediate: true }
)

watch(
  () => props.popupLayerIds,
  (popupLayerIds) => {
    popupLayerIds.forEach((layerId) => {
      const popup = new Popup({
        closeButton: false,
        closeOnClick: false
      })
      map?.on('mouseenter', layerId, function () {
        if (map) {
          map.getCanvas().style.cursor = 'pointer'
        }
      })

      map?.on('mouseleave', layerId, function () {
        if (map) {
          map.getCanvas().style.cursor = ''
        }
        popup.remove()
      })
    })
  },
  { immediate: true }
)
watch(
  () => props.filterIds,
  (filterIds) => {
    filterLayers(filterIds)
  },
  { immediate: true }
)

function update(center?: LngLatLike, zoom?: number) {
  if (center !== undefined) {
    map?.setCenter(center)
  }
  if (zoom !== undefined) {
    map?.setZoom(zoom)
  }
}

function filterLayers(filterIds?: string[]) {
  if (filterIds && map !== undefined && map.isStyleLoaded()) {
    map
      .getStyle()
      .layers.filter((layer) => !layer.id.startsWith('gl-draw'))
      .forEach((layer) => {
        map?.setLayoutProperty(
          layer.id,
          'visibility',
          filterIds.includes(layer.id) ? 'visible' : 'none'
        )
      })
  }
}
</script>

<template>
  <v-container class="pa-0 position-relative fill-height" fluid>
    <div ref="container" class="map fill-height">
      <loading-circle :loading="loading" />
    </div>
    <legend-map
      v-if="legendColors"
      :colors="legendColors"
      :is-continuous="continuousColor"
    ></legend-map>
  </v-container>
</template>

<style scoped>
.map {
  height: 100%;
  width: 100%;
  position: relative;
}

.map:deep(.hovered-feature) {
  cursor: pointer !important;
}
</style>
