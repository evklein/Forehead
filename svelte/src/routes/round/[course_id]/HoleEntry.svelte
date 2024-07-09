<script lang="ts">
    import type { EventHandler } from "svelte/elements";
    import HoleScoreCard from "../../../components/round/HoleScoreCard.svelte";
    import type { HoleData } from "../../../models/HoleData";
    import { onMount } from "svelte";
    import type { HoleScore } from "../../../models/HoleScore";
    import Map from "../../../components/shared/Map.svelte";
    import InputDirector from "../../../components/round/InputDirector.svelte";
    import { MapMarkerChoice } from "../../../components/shared/MapMarkerChoice";
    import type { CourseData } from "../../../models/CourseData";
    import type { RoundData } from "../../../models/RoundData";

    export let round: RoundData;
    export let course: CourseData;
    export let holes: HoleData[];
    export let holeScores: HoleScore[] = [];
    export let handleAdvance: EventHandler;
    
    let selectedStrokeIndex: number | undefined = undefined;
    let currentHoleIndex: number = 0;
    let currentHole: HoleData;
    let currentHoleScore: HoleScore;
    let selectedPoints: [number, number][] = [];

    onMount(() => {
        currentHole = holes[currentHoleIndex];
        currentHoleScore = holeScores[currentHoleIndex];
    });

    function incrementCurrentHoleNumber() {
        currentHoleIndex++;
        currentHole = holes[currentHoleIndex];
        currentHoleScore = holeScores[currentHoleIndex];
        selectedPoints = [];
    }

    function decrementCurrentHoleNumber() {
        currentHoleIndex--;
        currentHole = holes[currentHoleIndex];
        currentHoleScore = holeScores[currentHoleIndex];
        selectedPoints = [];
    }

    function selectPointOnMap(coordinates: [number, number]) {
        if (selectedStrokeIndex == undefined) {
            selectedPoints = [...selectedPoints, coordinates];
        } else {
            selectedPoints[selectedStrokeIndex] = coordinates;
        }

        selectedStrokeIndex = undefined;
    }

    function getCurrentInstructions(): string {
        if (currentHoleScore.numberOfStrokes && currentHoleScore.numberOfPutts) {
            let numberOfPointToBeMarked = currentHoleScore.numberOfStrokes - currentHoleScore.numberOfPutts;
            if (selectedPoints.length === 0) {
                return `
                    Mark any <span style="color: darkred; font-weight: bold;"">penalty shots</span> first on score card<br />
                    Place <span style="color: gold; font-weight: bold;">tee shot</span> location
                `;
            } else if (selectedPoints.length < numberOfPointToBeMarked + 1) {
                return `Place <b>${numberOfPointToBeMarked}</b> shots.`;
            } else {
                return `Fill in <span style="color: green; font-weight: bold;">putts table</span>`;
            }
        }

        return "Fill out scorecard";
    }

    function setTargetCoordinate(strokeNumber: number) {
        selectedStrokeIndex = strokeNumber;
    }
</script>
<div class="row align-items-start">
    <div class="col-6">
        {#if currentHole}
            {#key currentHoleIndex}
                <Map focusBounds={currentHole.boundPoints}
                    bind:selectedBounds={selectedPoints}
                    specialPoints={selectedPoints}
                    highlightSelectedbounds={true}
                    handleSelectPointOnMap={selectPointOnMap}
                    markerChoice={MapMarkerChoice.ShotTracer}
                />
                <InputDirector>
                    {#key currentHoleScore.numberOfStrokes, currentHoleScore.numberOfPutts, selectedPoints}
                        {@html getCurrentInstructions()}
                    {/key}
                </InputDirector>
            {/key}
        {/if}
    </div>
    <div class="col-6">
        <HoleScoreCard {round} {course}
            bind:hole={currentHole}
            bind:holeScore={currentHoleScore}
            handleGoToNextHole={incrementCurrentHoleNumber}
            handleGoToPreviousHole={decrementCurrentHoleNumber}
            {handleAdvance}
            {selectedPoints}
            handleSelectCurrentPosition={selectPointOnMap}
            handleSetTargetCoordinate={setTargetCoordinate}
        />
    </div>
</div>