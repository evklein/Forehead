<script lang="ts">
    import { afterUpdate, onMount } from 'svelte';
    import { MapMarkerChoice } from './MapMarkerChoice';

    export let focusBounds: [number, number][];
    export let selectedBounds: [number, number][];
    export let highlightSelectedbounds: boolean;
    export let specialPoints: [number, number][] = [];
    export let handleSelectPointOnMap: Function | undefined = undefined;
    export let markerChoice: MapMarkerChoice = MapMarkerChoice.Default;

    let map: L.Map;
    let markerLayerGroup: L.LayerGroup;

    onMount(async () => {
        await buildMap();
        await placeMarkers(specialPoints);
    });

    afterUpdate(async () => {
        await placeMarkers(specialPoints);
    });

    async function buildMap() {
        const L = await import('leaflet');
        await import('leaflet/dist/leaflet.css');

        if (!map) {
            map = L.map('map').setView([0, 0], 0);
            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                maxZoom: 20,
            }).addTo(map);

            if (focusBounds.length > 0) {
                map.fitBounds(focusBounds);
                if (highlightSelectedbounds) {
                    L.polygon(focusBounds, { fillColor: 'green', color: 'green' }).addTo(map);
                }
            }

            map.on('click', (e) => {
                let wrappedCoordinates = e.latlng.wrap();
                if (handleSelectPointOnMap) {
                    handleSelectPointOnMap([wrappedCoordinates.lat, wrappedCoordinates.lng]);
                }
            });

            if (specialPoints && Array.isArray(specialPoints)) {
                specialPoints.forEach(point => {
                    if (Array.isArray(point) && point.length === 2) {
                        let [latitude, longitude] = point;
                        L.marker([latitude, longitude]).addTo(map);
                    } else {
                        console.warn('Invalid point format', point);
                    }
                });
            }
        }
        
        return L;
    }

    async function placeMarkers(markerCoordinates: [number, number][]) {
        const L = await import('leaflet');
        await import('leaflet/dist/leaflet.css');

        if (markerLayerGroup == null) {
            markerLayerGroup = L.layerGroup().addTo(map);
        } else {
            markerLayerGroup.clearLayers();
        }

        for (let i = 0; i < markerCoordinates.length; i++) {
            let marker;
            switch (markerChoice) {
                case MapMarkerChoice.Default:
                    marker = L.marker(markerCoordinates[i] as [number, number]).addTo(markerLayerGroup);
                    marker.bindPopup(`[${markerCoordinates[0]}, ${markerCoordinates[1]}]`);
                    break;
                case MapMarkerChoice.ShotTracer:
                    marker = L.circleMarker(markerCoordinates[i] as [number, number], {
                        fillColor: i > 0 ? 'white' : 'yellow',
                        color: i > 0 ? 'white' : 'yellow',
                        radius: 8,
                    }).addTo(map);

                    if (selectedBounds.length > 1 && i >= 1) {
                        let lastSelectedBounds = selectedBounds[i - 1];
                        L.polyline([markerCoordinates[i] as [number, number], lastSelectedBounds], { color: 'white' }).addTo(markerLayerGroup);
                    }
                    break;
            }
        }
    }
</script>
<div id="map-wrapper">
    <div id="map"></div>
</div>
<style>
    #map-wrapper {
        height: 100%;
        width: 100%;
    }
    #map {
        height: 600px; /* Adjust height as needed */
        width: 100%;
        border: 4px solid darkgreen;
        border-radius:5px;
    }
</style>