<script lang="ts">
    // Props
    export let courseName: string;
    export let numberOfHoles: number;

    interface HoleScore {
        hole: number;
        numberOfStrokes?: number;
        numberOfPutts?: number;
        gir?: boolean;
        gld?: boolean;
        scrambling?: boolean;
        strokes: Stroke[];
    }

    interface Stroke {
        club: string;
        distance: number;
        startCoordinate: Object;
        endCoordinate: Object;
    }

    interface Putt {
        distance: number;
    }

    let holeScores: HoleScore[] = [];
    let currentHole = 1;
    let currentHoleScore: HoleScore = {
        hole: 1,
        strokes: [],
    };

    function goToNextHole() {
        console.log(currentHole);
        currentHole += currentHole !== numberOfHoles ? 1 : 0;
    }

    function goToPreviousHole() {
        currentHole -= currentHole !== 1 ? 1 : 0;
    }

    function finishRound() {

    }
</script>
<div class="card">
    <div class="card-body">
        <h5 class="card-title">
            <span class="card-title-emphasize">Hole {currentHole}</span> // {courseName}
            <span class="par-badge badge text-bg-success">Par 4</span>
        </h5>
        <p class="card-text"><b>310 yards</b></p>
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
                                bind:value={currentHoleScore.numberOfStrokes}
                                class="stats-control form-control"
                                aria-label="strokes">
                        </td>
                        <td class="td-20">
                            <input type="text"
                                bind:value={currentHoleScore.numberOfPutts}
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
                    {#if currentHoleScore.numberOfStrokes && currentHoleScore.numberOfPutts}
                        {#each {length: currentHoleScore.numberOfStrokes - currentHoleScore.numberOfPutts} as _, i}
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
                    {#if currentHoleScore.numberOfStrokes && currentHoleScore.numberOfPutts}
                        {#each {length: currentHoleScore.numberOfPutts ?? 0} as _, i}
                        <tr>
                            <td>{currentHoleScore.numberOfStrokes - currentHoleScore.numberOfPutts + i + 1}</td>
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
             {#if currentHole !== 1}
                <a href="/"
                    on:click|preventDefault={goToPreviousHole}
                    class="btn btn-success">
                    <i class="fa-solid fa-arrow-left"></i> Prev Hole
                </a>
            {/if}                
            <a href="/" class="btn btn-secondary"><i class="fas fa-redo"></i> Start over</a>
            {#if currentHole !== numberOfHoles}
                <a href="/"
                    on:click|preventDefault={goToNextHole}
                    class="btn btn-success">
                    <i class="fa-solid fa-arrow-right"></i> Next Hole
                </a>
            {:else}
                <a href="/"
                    on:click|preventDefault={finishRound}
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