<script lang="ts">
    import type { EventHandler } from 'svelte/elements';
    import HoleScoreCard from '../../../components/round/HoleScoreCard.svelte';
    import type { HoleData } from '../../../models/HoleData';
    import { onMount } from 'svelte';
    import type { HoleScore } from '../../../models/HoleScore';
    import Map from '../../../components/shared/Map.svelte';
    import { MapMarkerChoice } from '../../../components/shared/MapMarkerChoice';
    import type { CourseData } from '../../../models/CourseData';
    import type { RoundData } from '../../../models/RoundData';
    import type { TeeData } from '../../../models/TeeData';
    import type { MapMarker } from '../../../models/MapMarker';

    export let round: RoundData;
    export let course: CourseData;
    export let courseTees: TeeData[];
    export let holes: HoleData[];
    export let holeScores: HoleScore[] = [];
    export let handleAdvance: EventHandler;

    let selectedShotCoordinateIndex: number = -1;
    let selectedShotCoordinateStart: boolean = true;
    let currentHoleIndex: number = 0;
    let currentHole: HoleData;
    let currentHoleScore: HoleScore;

    $: selectedPointsForMap = (() => {
        let mapMarkers: MapMarker[] = [];
        if (currentHoleScore && currentHoleScore.fullShots) {
            for (let i = 0; i < currentHoleScore.fullShots.length; i++) {
                let startCoordinate = currentHoleScore.fullShots[i].startCoordinate;
                let endCoordinate = currentHoleScore.fullShots[i].endCoordinate;

                if (startCoordinate) {
                    let startMarkerForShot = {
                        coordinates: startCoordinate,
                        drop: i > 0 ? currentHoleScore.fullShots[i - 1].penalty : false,
                    };
                    mapMarkers = [...mapMarkers, startMarkerForShot];
                }

                if (endCoordinate) {
                    let endMarkerForShot = {
                        coordinates: endCoordinate,
                        drop: false,
                    };
                    mapMarkers = [...mapMarkers, endMarkerForShot];
                }
            }
        }
        return mapMarkers;
    })();

    onMount(() => {
        currentHole = holes[currentHoleIndex];
        currentHoleScore = holeScores[currentHoleIndex];
        resetSelectedShotIndex();
    });

    function incrementCurrentHoleNumber() {
        currentHoleIndex++;
        currentHole = holes[currentHoleIndex];
        currentHoleScore = holeScores[currentHoleIndex];
        resetSelectedShotIndex();
    }

    function decrementCurrentHoleNumber() {
        currentHoleIndex--;
        currentHole = holes[currentHoleIndex];
        currentHoleScore = holeScores[currentHoleIndex];
        resetSelectedShotIndex();
    }

    function resetSelectedShotIndex() {
        selectedShotCoordinateIndex = 0;
        selectedShotCoordinateStart = true;
    }

    function selectPointOnMap(coordinates: [number, number]) {
        if (selectedShotCoordinateIndex !== -1) {
            console.log('Setting coordinates for ' + selectedShotCoordinateIndex + '.' + selectedShotCoordinateStart);
            if (selectedShotCoordinateStart) {
                currentHoleScore.fullShots[selectedShotCoordinateIndex].startCoordinate = coordinates;

                let previousShot = currentHoleScore.fullShots[selectedShotCoordinateIndex - 1];
                if (previousShot && !previousShot.penalty) {
                    previousShot.endCoordinate = coordinates;
                }
            } else {
                currentHoleScore.fullShots[selectedShotCoordinateIndex].endCoordinate = coordinates;

                let nextShot = currentHoleScore.fullShots[selectedShotCoordinateIndex + 1];
                if (nextShot && !nextShot.penalty) {
                    nextShot.startCoordinate = coordinates;
                }
            }
        }

        if (selectedShotCoordinateIndex === 0 && selectedShotCoordinateStart) {
            if (selectedShotCoordinateStart) selectedShotCoordinateStart = false;
        } else {
            selectedShotCoordinateIndex++;
        }
    }

    function getCurrentInstructions(): string {
        // if (
        //     currentHoleScore.numberOfStrokes &&
        //     currentHoleScore.numberOfPutts
        // ) {
        //     let numberOfPointToBeMarked =
        //         currentHoleScore.numberOfStrokes -
        //         currentHoleScore.numberOfPutts;
        //     if (selectedPoints.length === 0) {
        //         return `
        //             Mark any <span style="color: darkred; font-weight: bold;"">penalty shots</span> first on score card<br />
        //             Place <span style="color: gold; font-weight: bold;">tee shot</span> location
        //         `;
        //     } else if (selectedPoints.length < numberOfPointToBeMarked + 1) {
        //         return `Place <b>${numberOfPointToBeMarked}</b> shots.`;
        //     } else {
        //         return `Fill in <span style="color: green; font-weight: bold;">putts table</span>`;
        //     }
        // }
        // return 'Fill out scorecard';
        return ``;
    }

    function setTargetCoordinate(strokeIndex: number, start: boolean) {
        selectedShotCoordinateIndex = strokeIndex;
        selectedShotCoordinateStart = start;
    }
</script>

<div class="row align-items-start">
    <!-- <div class="map-col col-12 col-md-5">
        {#if currentHole}
            {#key currentHoleIndex}
                <Map
                    focusBounds={currentHole.boundPoints}
                    markers={selectedPointsForMap}
                    highlightSelectedbounds={true}
                    handleSelectPointOnMap={selectPointOnMap}
                    markerChoice={MapMarkerChoice.ShotTracer}
                    showAdditionalControls={true}
                />
            {/key}
        {/if}
    </div> -->
    <div class="card-col col-12 col-md-7">
        <HoleScoreCard
            {round}
            {course}
            bind:hole={currentHole}
            bind:holeScore={currentHoleScore}
            handleGoToNextHole={incrementCurrentHoleNumber}
            handleGoToPreviousHole={decrementCurrentHoleNumber}
            {handleAdvance}
            handleSetTargetCoordinate={setTargetCoordinate}
            {courseTees}
            {selectedShotCoordinateIndex}
            {selectedShotCoordinateStart}
        >
            <div class="m-1">
                {#if currentHole}
                    {#key currentHoleIndex}
                        <Map
                            focusBounds={currentHole.boundPoints}
                            markers={selectedPointsForMap}
                            highlightSelectedbounds={true}
                            handleSelectPointOnMap={selectPointOnMap}
                            markerChoice={MapMarkerChoice.ShotTracer}
                            showAdditionalControls={true}
                        />
                    {/key}
                {/if}
            </div>
        </HoleScoreCard>
        {#if currentHole}
            <!-- <InputDirector>
                {#key (currentHoleScore.numberOfStrokes, currentHoleScore.numberOfPutts, selectedPoints)}
                    {@html getCurrentInstructions()}
                {/key}
            </InputDirector> -->
        {/if}
    </div>
</div>

<style>
    @media only screen and (max-width: 799px) {
        .map-col {
            order: 1;
        }

        .card-col {
            order: 0;
        }
    }
</style>
