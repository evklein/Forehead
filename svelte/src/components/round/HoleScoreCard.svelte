<script lang="ts">
    import type { EventHandler } from "svelte/elements";
    import type { HoleData } from "../../models/HoleData";
    import type { HoleScore } from "../../models/HoleScore";
    import * as geo from "../../services/geo";
    import * as api from "../../services/api";

    // Props
    export let courseName: string;
    export let maximumNumberOfHoles: number;
    export let hole: HoleData;
    export let holeScore: HoleScore;
    export let handleGoToNextHole: Function;
    export let handleGoToPreviousHole: Function;
    export let handleAdvance: EventHandler;
    export let selectedPoints: [number, number][];

    let clubs: string[] = ['62°', '56°', '50°', 'P', '9', '8', '7', '6', '5', '4H', '3H', '3W', 'D'].reverse();

    function createStrokesAndPutts(event: any) {
        holeScore.strokes = [];
        holeScore.putts = [];

        if (holeScore.numberOfStrokes && holeScore.numberOfPutts) {
            for (let i = 0; i < holeScore.numberOfStrokes; i++) {
                holeScore.strokes.push({
                    strokeNumber: i + 1,                
                });
            }
    
            for (let i = 0; i < holeScore.numberOfPutts; i++) {
                holeScore.putts.push({
                    strokeNumber: i + holeScore.numberOfStrokes + 1,
                });
            }
        }
    }

    async function saveAll() {
        // Save Hole Stats
        
        // Save strokes

        // Save putts
        for (let i = 0; i < holeScore.putts.length; i++) {
            let nextPutt = holeScore.putts[i];
            await api.savePutt(2, 1, nextPutt);
        }
    }

    async function saveAndGoToNext() {
        console.log('Saving!');
        await saveAll();
        handleGoToPreviousHole();
    }

    async function saveAndGoToPrevious() {
        await saveAll();
        handleGoToNextHole();
    }
</script>
{#if holeScore}
<div class="card">
    <div class="card-body">
        <h5 class="card-title">
            <span class="card-title-emphasize">Hole {hole?.holeNumber}</span> // {courseName}
            <span class="par-badge badge text-bg-success">Par {hole?.par}</span>
        </h5>
        <p class="approximate-yardage">
            <i class="fas fa-arrows-alt-h"></i>
            {#if selectedPoints.length > 0 && hole.centerGreenPoint}
                {geo.getDistanceFromLatLonInYards(selectedPoints[0][0], selectedPoints[0][1], hole.centerGreenPoint[0], hole.centerGreenPoint[1]).toFixed(0)} yards
            {:else}
                -
            {/if}
        </p>
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
                                class="stats-control form-control"
                                bind:value={holeScore.numberOfStrokes}
                                aria-label="strokes">
                        </td>
                        <td class="td-20">
                            <input type="text"
                                class="stats-control form-control"
                                bind:value={holeScore.numberOfPutts}
                                on:change|preventDefault={createStrokesAndPutts}
                                aria-label="putts">
                        </td>
                        <td class="td-20">
                            <input class="score-checkbox form-check-input" type="checkbox" value="" id="flexCheckDefault">
                        </td>
                        <td class="td-20">
                            <input class="score-checkbox form-check-input" type="checkbox" value="" id="flexCheckDefault">
                        </td>
                        <td class="td-20">
                            {#if holeScore.stats && holeScore.stats.greenInRegulation}
                                <input class="score-checkbox form-check-input"
                                        type="checkbox" value="" id="flexCheckDefault">
                            {:else}
                                <span class="disabled-checkbox-placeholder">-</span>
                            {/if}
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
                        <th scope="col">Penalty</th>
                    </tr>
                </thead>
                <tbody>
                    {#if holeScore?.strokes && holeScore?.putts}
                        {#each {length: holeScore.strokes.length - holeScore.putts.length} as _, strokeNumber}
                            <tr>
                                <td>{strokeNumber + 1}</td>
                                <td>
                                    <select
                                        class="form-select"
                                        id="floatingSelect"
                                        aria-label="club-select"
                                    >
                                        <option selected>Club</option>
                                        {#each clubs as club}
                                            <option>
                                                {club}
                                            </option>
                                        {/each}
                                    </select>
                                </td>
                                <td>
                                    {#if selectedPoints && selectedPoints.length >= strokeNumber + 2}
                                        {geo.getDistanceFromLatLonInYards(
                                            selectedPoints[strokeNumber][0],
                                            selectedPoints[strokeNumber][1],
                                            selectedPoints[strokeNumber + 1][0],
                                            selectedPoints[strokeNumber + 1][1]
                                        ).toFixed(1)}
                                    {/if}
                                </td>
                                <td>
                                    {#if selectedPoints && selectedPoints.length >= strokeNumber + 2 && hole && hole.centerGreenPoint}
                                        {geo.getDistanceFromLatLonInYards(
                                            hole.centerGreenPoint[0],
                                            hole.centerGreenPoint[1],
                                            selectedPoints[strokeNumber + 1][0],
                                            selectedPoints[strokeNumber + 1][1]
                                        ).toFixed(1)}
                                    {/if}
                                </td>
                                <td>
                                    <input class="penalty-checkbox form-check-input"
                                            type="checkbox" value="" id="flexCheckDefault">
                                    </td>
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
                    {#if holeScore?.strokes && holeScore?.putts}
                        {#each {length: holeScore.putts.length ?? 0} as _, i}
                        <tr>
                            <td>{holeScore.strokes.length - holeScore.putts.length + i + 1}</td>
                            <td>{i + 1}</td>
                            <td>
                                <input class="form-control" type="text" placeholder="" />
                            </td>
                        </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
        </div>
        <div class="card-buttons">
            <a href="/" class="btn btn-secondary"><i class="fas fa-redo"></i> Start over</a>

        <div class="card-right">
             {#if hole?.holeNumber !== 1}
                <a href="/"
                    on:click|preventDefault={saveAndGoToPrevious}
                    class="btn btn-success">
                    <i class="fa-solid fa-arrow-left"></i> Previous
                </a>
            {/if}                
            {#if hole?.holeNumber !== maximumNumberOfHoles}
                <a href="/"
                    on:click|preventDefault={saveAndGoToNext}
                    class="btn btn-success">
                    <i class="fa-solid fa-arrow-right"></i> Save and go to next
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
</div>
{/if}
<style>
    .approximate-yardage {
        font-size: 12pt;
    }
    .score-checkbox {
        width: 1.75em;
        height: 1.75em;
        display: block;
        margin: auto;
        margin-top: 5px;
    }
    .penalty-checkbox {
        width: 1.75em;
        height: 1.75em;
        display: block;
        margin: auto;
        margin-top: 5px;
    }
    .penalty-checkbox:checked {
        background-color: darkred !important;
        border-color: darkred !important;
    }
    .penalty-checkbox:focus {
        border-color: rgba(139, 0, 0, .25);
        box-shadow: 0 0 0 .25rem rgba(139, 0, 0,.25)
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
    .disabled-checkbox-placeholder {
        text-align: center;
        font-size: 18pt;
        color: #555;
        display: block;
        margin: auto;
    }
</style>