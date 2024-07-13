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

    export let round: RoundData;
    export let course: CourseData;
    export let courseTees: TeeData[];
    export let holes: HoleData[];
    export let holeScores: HoleScore[] = [];
    export let handleAdvance: EventHandler;

    let selectedStrokeCoordinateIndex: number = -1;
    let selectedStrokeCoordinateStart: boolean = true;
    let currentHoleIndex: number = 0;
    let currentHole: HoleData;
    let currentHoleScore: HoleScore;

    $: selectedPointsForMap = currentHoleScore?.fullShots
        .map((fullShot) => [fullShot.startCoordinate, fullShot.endCoordinate])
        .flat() as [number, number][];

    onMount(() => {
        currentHole = holes[currentHoleIndex];
        currentHoleScore = holeScores[currentHoleIndex];
    });

    function incrementCurrentHoleNumber() {
        currentHoleIndex++;
        currentHole = holes[currentHoleIndex];
        currentHoleScore = holeScores[currentHoleIndex];
    }

    function decrementCurrentHoleNumber() {
        currentHoleIndex--;
        currentHole = holes[currentHoleIndex];
        currentHoleScore = holeScores[currentHoleIndex];
    }

    function selectPointOnMap(coordinates: [number, number]) {
        if (selectedStrokeCoordinateIndex !== -1) {
            console.log('Placing coordinates: ' + coordinates);
            if (selectedStrokeCoordinateStart) {
                console.log('Setting start coordinates for stroke ' + selectedStrokeCoordinateIndex);
                currentHoleScore.fullShots[selectedStrokeCoordinateIndex].startCoordinate = coordinates;
            } else {
                console.log('Setting end coordinates for stroke ' + selectedStrokeCoordinateIndex);
                currentHoleScore.fullShots[selectedStrokeCoordinateIndex].endCoordinate = coordinates;
            }
        }

        selectedStrokeCoordinateIndex = -1;
        selectedStrokeCoordinateStart = true;
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
        selectedStrokeCoordinateIndex = strokeIndex;
        selectedStrokeCoordinateStart = start;
    }
</script>

<div class="row align-items-start">
    <div class="col-12">
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
        />
        {#if currentHole}
            <!-- <InputDirector>
                {#key (currentHoleScore.numberOfStrokes, currentHoleScore.numberOfPutts, selectedPoints)}
                    {@html getCurrentInstructions()}
                {/key}
            </InputDirector> -->
        {/if}
    </div>
    <div class="col-12">
        {#if currentHole}
            {#key currentHoleIndex}
                <Map
                    focusBounds={currentHole.boundPoints}
                    specialPoints={selectedPointsForMap}
                    highlightSelectedbounds={true}
                    handleSelectPointOnMap={selectPointOnMap}
                    markerChoice={MapMarkerChoice.ShotTracer}
                    showAdditionalControls={true}
                />
            {/key}
        {/if}
    </div>
</div>
