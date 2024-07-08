<script lang="ts">
    import type { CourseData } from "../../models/CourseData";
    import type { RoundData } from "../../models/RoundData";
    import InProgressRoundCard from "./InProgressRoundCard.svelte";

    export let rounds: RoundData[] = [];
    export let course: CourseData;
</script>
<div class="row align-items-start">
    <div class="col-12">
        <div class="btn-group">
            <a class="btn btn-success" href="/courses">
                <i class="fa fa-plus"></i> Start new round
            </a>
        </div>
    </div>
    <div class="col-12 mt-4">
        <h2>In-Progress Rounds</h2>
        {#if rounds.length === 0}
            <span class="no-rounds">No in-progress rounds found.</span>
        {/if}
        {#each rounds as round}
            <InProgressRoundCard
                {round}
                {course}
            />
        {/each}
    </div>
</div>