<script lang="ts">
    import { afterUpdate, onMount } from 'svelte';
    import { MapMarkerChoice } from './MapMarkerChoice';
    import type { MapMarker } from '../../models/MapMarker';

    export let focusBounds: [number, number][];
    export let highlightSelectedbounds: boolean;
    export let markers: MapMarker[] = [];
    export let handleSelectPointOnMap: Function | undefined = undefined;
    export let markerChoice: MapMarkerChoice = MapMarkerChoice.Default;
    export let showAdditionalControls: boolean = false;

    let map: L.Map;
    let markerLayerGroup: L.LayerGroup;

    onMount(async () => {
        await buildMap();
        await placeMarkers(markers);
    });

    afterUpdate(async () => {
        await placeMarkers(markers);
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
                    L.polygon(focusBounds, {
                        fillColor: 'green',
                        color: 'green',
                    }).addTo(map);
                }
            }

            map.on('click', (e) => {
                let wrappedCoordinates = e.latlng.wrap();
                if (handleSelectPointOnMap) {
                    handleSelectPointOnMap([wrappedCoordinates.lat, wrappedCoordinates.lng]);
                }
            });
        }

        return L;
    }

    async function placeMarkers(markers: MapMarker[]) {
        const L = await import('leaflet');
        await import('leaflet/dist/leaflet.css');

        if (markerLayerGroup == null) {
            markerLayerGroup = L.layerGroup().addTo(map);
        }
        markerLayerGroup.clearLayers();

        for (let i = 0; i < markers.length; i++) {
            let marker = markers[i];
            let leafletMarker;
            switch (markerChoice) {
                case MapMarkerChoice.Default:
                    leafletMarker = L.marker(marker.coordinates).addTo(markerLayerGroup);
                    leafletMarker.bindPopup(`[${marker.coordinates[0]}, ${marker.coordinates[1]}]`);
                    break;
                case MapMarkerChoice.ShotTracer:
                    let markerColor = 'white';
                    if (i === 0) markerColor = 'yellow';
                    if (marker.drop) markerColor = 'red';

                    leafletMarker = L.circleMarker(marker.coordinates, {
                        fillColor: markerColor,
                        color: markerColor,
                        radius: 8,
                    }).addTo(markerLayerGroup);

                    if (markers.length > 1 && i >= 1) {
                        let lastMarker = markers[i - 1];
                        if (!marker.drop) {
                            L.polyline([marker.coordinates, lastMarker.coordinates], {
                                color: 'white',
                            }).addTo(markerLayerGroup);
                        }
                    }
                    break;
            }
        }
    }

    function clickUseCurrentLocation() {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                let lat = position.coords.latitude;
                let long = position.coords.longitude;
                if (handleSelectPointOnMap) {
                    handleSelectPointOnMap([lat, long]);
                }
                console.log('Accuracy: ' + position.coords.accuracy);
            },
            (error) => {
                console.error('Error obtaining location:', error);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0,
            },
        );
    }
</script>

<div id="map-wrapper">
    {#if showAdditionalControls}
        <div id="map-controls-panel">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">
                        <i class="fa-solid fa-sliders"></i>&nbsp; Map Controls
                    </h5>
                    <div class="btn-group">
                        <button class="btn btn-success" on:click={clickUseCurrentLocation}>
                            <i class="fa-solid fa-location-dot"></i>&nbsp; Use Current Location
                        </button>
                    </div>
                </div>
            </div>
        </div>
    {/if}
    <div id="map"></div>
</div>

<style>
    #map-wrapper {
        height: 100%;
        width: 100%;
    }
    #map-controls-panel {
        margin: 10px 0;
    }
    #map {
        height: 600px; /* Adjust height as needed */
        width: 100%;
        border: 4px solid darkgreen;
        border-radius: 5px;
    }
</style>
