<script lang="ts">
    import type { EventHandler } from "svelte/elements";
    import HoleScoreCard from "../../../components/round/HoleScoreCard.svelte";
    import type { HoleData } from "../../../models/HoleData";
    import { onMount } from "svelte";
    import type { HoleScore } from "../../../models/HoleScore";
    import Map from "../../../components/shared/Map.svelte";

    export let courseName: string;
    export let maximumNumberOfHoles: number;
    export let holes: HoleData[];
    export let holeScores: HoleScore[] = [];
    export let handleAdvance: EventHandler;
    
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

    function selectPointOnMap(position: any) {
        selectedPoints.push([position.lat, position.lng]);
        selectedPoints = selectedPoints;
    }
</script>
<div class="row align-items-start">
    <div class="col-6">
        {#if currentHole}
            {#key currentHoleIndex}
                <Map focusBounds={currentHole.boundPoints}
                    bind:selectedBounds={currentHole.boundPoints}
                    highlightSelectedbounds={true}
                    handleSelectPointOnMap={selectPointOnMap}
                />
            {/key}
        {/if}
    </div>
    <div class="col-6">
        <HoleScoreCard {courseName}
            bind:hole={currentHole}
            {maximumNumberOfHoles}
            bind:holeScore={currentHoleScore}
            handleGoToNextHole={incrementCurrentHoleNumber}
            handleGoToPreviousHole={decrementCurrentHoleNumber}
            {handleAdvance}
            {selectedPoints}
        />
    </div>
</div>