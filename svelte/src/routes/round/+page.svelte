<script lang="ts">
    import { onMount } from "svelte";
    import * as api from "../../services/api";
    import RoundStart from "./RoundStart.svelte";
    import { RoundStage } from "./RoundStage";
    import Finalize from "./Finalize.svelte";
    import HoleEntry from "./HoleEntry.svelte";

    let entryStage: RoundStage = RoundStage.Start;
    let currentHole: number = 1;

    let courseName = "Sahm Golf Course";
    let round: RoundData = {
        datePlayed: new Date(),
        holesCompleted: 18,
        mobility: "Walking",
    };
    let tees: TeeData[] = [];

    onMount(async () => {
        // Get tees
        tees = await api.fetchTees(1) ?? [];
        console.log(tees);
    });
</script>
{#if entryStage === RoundStage.Start}
    <RoundStart {courseName} bind:round {tees} />
{:else if entryStage === RoundStage.HoleEntry}
    <HoleEntry />
{:else if entryStage === RoundStage.Finalize}
    <Finalize />
{/if}
<style>
</style>