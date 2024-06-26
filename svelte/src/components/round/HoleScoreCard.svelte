<script lang="ts">
    import type { EventHandler } from "svelte/elements";
    import type { HoleData } from "../../models/HoleData";
    import type { HoleScoreData } from "../../models/HoleScoreData";

    // Props
    export let courseName: string;
    export let maximumNumberOfHoles: number;
    export let hole: HoleData;
    export let holeScore: HoleScoreData;
    export let handleGoToNextHole: EventHandler;
    export let handleGoToPreviousHole: EventHandler;
    export let handleAdvance: EventHandler;
</script>
<div class="card">
    <div class="card-body">
        <h5 class="card-title">
            <span class="card-title-emphasize">Hole {hole.holeNumber}</span> // {courseName}
            <span class="par-badge badge text-bg-success">Par 4</span>
        </h5>
        <div class="score-entry">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col">S</th>
                        <th scope="col">P</th>
                        <th scope="col">GIR</th>
                        <th scope="col">GLD</th>
                        <th scope="col">SCR</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="td-20">
                            <input type="text"
                                bind:value={holeScore.score}
                                class="stats-control form-control"
                                aria-label="strokes">
                        </td>
                        <td class="td-20">
                            <input type="text"
                                bind:value={holeScore.putts}
                                class="stats-control form-control"
                                aria-label="putts">
                        </td>
                        <td class="td-20">
                            <input class="score-checkbox form-check-input" type="checkbox" value="" id="flexCheckDefault">
                        </td>
                        <td class="td-20">
                            <input class="score-checkbox form-check-input" type="checkbox" value="" id="flexCheckDefault">
                        </td>
                        <td class="td-20">
                            <input class="score-checkbox form-check-input" type="checkbox" value="" id="flexCheckDefault">
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="shot-entry">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th style="width: 30px" scope="col">Stroke</th>
                        <th scope="col">Club</th>
                        <th scope="col">Distance (Yards)</th>
                        <th scope="col">To Center</th>
                    </tr>
                </thead>
                <tbody>
                    {#if holeScore.score && holeScore.putts}
                        {#each {length: holeScore.score - holeScore.putts} as _, i}
                            <tr>
                                <td>{i + 1}</td>
                                <td></td>
                                <td></td>
                                <td></td>
                            </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
        </div>
        <div class="putting-entry">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th style="width: 30px" scope="col">Stroke</th>
                        <th scope="col">Putt</th>
                        <th scope="col">Distance (Feet)</th>
                    </tr>
                </thead>
                <tbody>
                    {#if holeScore.score && holeScore.putts}
                        {#each {length: holeScore.putts ?? 0} as _, i}
                        <tr>
                            <td>{holeScore.score - holeScore.putts + i + 1}</td>
                            <td>{i + 1}</td>
                            <td></td>
                        </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
        </div>
        
        <div class="card-buttons">
            
        </div>
        <div class="card-right">
             {#if hole.holeNumber !== 1}
                <a href="/"
                    on:click|preventDefault={handleGoToPreviousHole}
                    class="btn btn-success">
                    <i class="fa-solid fa-arrow-left"></i> Prev Hole
                </a>
            {/if}                
            <a href="/" class="btn btn-secondary"><i class="fas fa-redo"></i> Start over</a>
            {#if hole.holeNumber !== maximumNumberOfHoles}
                <a href="/"
                    on:click|preventDefault={handleGoToNextHole}
                    class="btn btn-success">
                    <i class="fa-solid fa-arrow-right"></i> Next Hole
                </a>
            {:else}
                <a href="/"
                    on:click|preventDefault={handleAdvance}
                    class="btn btn-success">
                    <i class="fa-solid fa-check"></i> Finish Round
                </a>
            {/if}
        </div>
    </div>
</div>
<style>
    .score-checkbox {
        width: 1.75em;
        height: 1.75em;
        display: block;
        margin: auto;
        margin-top: 5px;
    }
    .card-title-emphasize {
        font-size: 18pt;
        font-weight: bold;
    }
    .par-badge {
        float: right;
    }
    .card-right {
        float: right;
    }
    .stats-control {
        border: 0;
    }
    .score-entry {
        width: 300px;
    }
    .shot-entry {
        width: 400px;
    }
    .putting-entry {
        width: 250px;
    }
    td.td-20 {
        width: 20%;
    }
</style>