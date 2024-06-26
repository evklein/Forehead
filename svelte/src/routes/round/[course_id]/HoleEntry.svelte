<script lang="ts">
    import type { EventHandler } from "svelte/elements";
    import HoleScoreCard from "../../../components/round/HoleScoreCard.svelte";
    import type { HoleData } from "../../../models/HoleData";
    import type { HoleScoreData } from "../../../models/HoleScoreData";
    import { onMount } from "svelte";

    export let holes: HoleData[];
    export let holeScores: HoleScoreData[] = [];
    export let handleAdvance: EventHandler;
    export let courseName: string;
    export let maximumNumberOfHoles: number;
    
    let currentHoleNumber: number = 1;

    onMount(() => {
        console.log('In hole entry.');
        console.log(courseName);
        console.log(holeScores);
    });
</script>
<div class="row align-items-start">
    <div class="col-6">
        <!-- <Map /> -->
    </div>
    <div class="col-6">
        <HoleScoreCard {courseName}
            bind:hole={holes[currentHoleNumber]}
            {maximumNumberOfHoles}
            bind:holeScore={holeScores[currentHoleNumber]}
            handleGoToNextHole={() => currentHoleNumber++}
            handleGoToPreviousHole={() => currentHoleNumber--}
            {handleAdvance}
        />
    </div>
</div>