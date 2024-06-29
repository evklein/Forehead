<script lang="ts">
    import { onMount } from 'svelte';
    import { MapMarkerChoice } from './MapMarkerChoice';

    export let focusBounds: [number, number][];
    export let selectedBounds: [number, number][];
    export let highlightSelectedbounds: boolean;
    export let specialPoints: [number, number][] = [];
    export let handleSelectPointOnMap: Function;
    export let markerChoice: MapMarkerChoice = MapMarkerChoice.Default;

    let map: L.Map;

    onMount(async () => {
        await buildMap();
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
                let marker: any;
                switch (markerChoice) {
                    case MapMarkerChoice.Default:
                        marker = L.marker(wrappedCoordinates).addTo(map);
                        marker.bindPopup(`[${wrappedCoordinates.lat}, ${wrappedCoordinates.lng}]`);
                        break;
                    case MapMarkerChoice.ShotTracer:
                        marker = L.circleMarker(wrappedCoordinates, {
                            fillColor: selectedBounds.length > 0 ? 'white' : 'yellow',
                            color: selectedBounds.length > 0 ? 'white' : 'yellow',
                            radius: 8,
                        }).addTo(map);
                        if (selectedBounds.length >= 1) {
                            let lastSelectedBounds = selectedBounds[selectedBounds.length - 1];
                            let line = L.polyline([wrappedCoordinates, lastSelectedBounds], { color: 'white' }).addTo(map);

                        }
                        break;
                }
                // selectedBounds.push([wrappedCoordinates.lat, wrappedCoordinates.lng]);
                // selectedBounds = selectedBounds;

                console.log(selectedBounds.length);
                handleSelectPointOnMap(wrappedCoordinates);
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