<script lang="ts">
    import type { HoleData } from '../../models/HoleData';
    import type { HoleScore } from '../../models/HoleScore';
    import * as geo from '../../services/geo';
    import * as api from '../../services/api';
    import * as scoreUtils from '../../services/scoreCardUtilities';
    import type { CourseData } from '../../models/CourseData';
    import type { RoundData } from '../../models/RoundData';
    import type { TeeData } from '../../models/TeeData';

    // Props
    export let course: CourseData;
    export let courseTees: TeeData[];
    export let round: RoundData;
    export let hole: HoleData;
    export let holeScore: HoleScore;
    export let handleGoToNextHole: Function;
    export let handleGoToPreviousHole: Function;
    export let handleAdvance: Function;
    export let handleSelectCurrentPosition: Function;
    export let handleSetTargetCoordinate: Function;
    export let selectedPoints: [number, number][];

    $: selectedPoints = selectedPoints;

    let clubs: string[] = ['62°', '56°', '50°', 'P', '9', '8', '7', '6', '5', '4H', '3H', '3W', 'D'].reverse();
    let selectedTeeId: number | undefined = round.playedTeeId;

    function addFullShot(startCoordinates?: [number, number]) {
        let newStrokeNumber = holeScore.fullShots.length;

        holeScore.fullShots = [
            ...holeScore.fullShots,
            {
                penalty: false,
                startCoordinate: startCoordinates,
            },
        ];

        if (newStrokeNumber > 1) {
            holeScore.fullShots[newStrokeNumber - 2].endCoordinate = startCoordinates;
        }
    }

    function addFullShotWithGPS() {
        navigator.geolocation.getCurrentPosition((position) => {
            let lat = position.coords.latitude + Math.random() * 0.001;
            let long = position.coords.longitude + Math.random() * 0.001;
            handleSelectCurrentPosition([lat, long]);
            if (selectedPoints.length > 0) {
                addFullShot([lat, long]);
            }
        });
    }

    function removeStroke(strokeIndex: number) {
        holeScore.fullShots.splice(strokeIndex, 1);
        holeScore.fullShots = holeScore.fullShots; // Trigger re-render

        selectedPoints.splice(strokeIndex, 1);
        selectedPoints = selectedPoints;
    }

    function addPutt() {
        holeScore.putts = [
            ...holeScore.putts,
            {
                distance: 0,
            },
        ];
    }

    function removePutt(puttNumber: number) {
        let puttIndex = puttNumber - 1;
        holeScore.putts.splice(puttIndex, 1);
        holeScore.putts = holeScore.putts;
    }

    function getFormattedCoordinateText(strokeIndex: number): string {
        if (selectedPoints[strokeIndex]) {
            return `[${selectedPoints[strokeIndex][0].toFixed(5)}, ${selectedPoints[strokeIndex][1].toFixed(5)}]`;
        }

        return strokeIndex === 0 ? 'Set Tee Shot Coordinates' : 'Set Coordinates';
    }

    function fullStrokeCellBackgroundStyle(strokeIndex: number): string {
        if (holeScore.fullShots[strokeIndex].penalty) return "red";
        return "blue";
    }

    async function saveAll() {
        if (round.id && hole.id) {
            await api.saveHoleStats(round.id, hole.id, holeScore.stats);
        }

        let nextSelectedPointIndex = 0;
        holeScore.fullShots.forEach(async (stroke, index) => {
            if (round.id && hole.id) {
                stroke.startCoordinate = selectedPoints[nextSelectedPointIndex];
                stroke.endCoordinate = selectedPoints[nextSelectedPointIndex + 1];
                stroke.distance = geo.getDistanceFromLatLonInYards(
                    stroke.startCoordinate[0],
                    stroke.startCoordinate[1],
                    stroke.endCoordinate[0],
                    stroke.endCoordinate[1],
                );
                stroke.strokeNumber = index + 1;
                await api.saveStroke(round.id, hole.id, stroke);
            }
            nextSelectedPointIndex++;
        });

        holeScore.putts.forEach(async (putt, index) => {
            if (round.id && hole.id) {
                (putt.strokeNumber = holeScore.fullShots.length + index + 1),
                    await api.savePutt(round.id, hole.id, putt);
            }
        });
    }

    async function saveAndGoToNext() {
        await saveAll();
        handleGoToNextHole();
    }

    async function saveAndGoToPrevious() {
        await saveAll();
        handleGoToPreviousHole();
    }

    async function advance() {
        await saveAll();
        handleAdvance();
    }
</script>

{#if holeScore}
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                <span class="title-section card-title-emphasize">Hole {hole?.holeNumber}</span>
                <span class="title-section">// {course.name}</span>
                <span class="title-section approximate-yardage">
                    // <i class="fas fa-arrows-alt-h"></i>
                    {#if selectedPoints.length > 0 && hole.centerGreenPoint}
                        {geo
                            .getDistanceFromLatLonInYards(
                                selectedPoints[0][0],
                                selectedPoints[0][1],
                                hole.centerGreenPoint[0],
                                hole.centerGreenPoint[1],
                            )
                            .toFixed(0)} yards
                    {:else}
                        -
                    {/if}
                </span>
                <span class="title-section tee-select-section">
                    // {#if courseTees}
                        <span class="tee-color" style="background: #{courseTees.filter(t => t.id === selectedTeeId)[0]?.color}"></span>
                        <select
                            class="tee-select form-select"
                            aria-label="tee-select"
                            bind:value={selectedTeeId}
                        >
                            {#each courseTees as tee}
                                <option value={tee.id}>
                                    {tee.name}
                                </option>
                            {/each}
                        </select>
                    {/if}
                </span>
                <span class="title-section par-badge badge text-bg-success">Par {hole?.par}</span>
            </h5>
            <div class="btn btn-group">
                <button class="btn btn-primary" on:click={() => addFullShot()}>Add FullShot</button>
                <button class="btn btn-info" on:click={addPutt}>Add Putt</button>
            </div>
            <div class="score-entry">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th scope="col">Full Shots</th>
                            <th scope="col">Putts</th>
                            <th scope="col">Score</th>
                            <th scope="col">GLD</th>
                            <th scope="col">GIR</th>
                            <th scope="col">SCR</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <input
                                    type="text"
                                    class="stats-control form-control"
                                    bind:value={holeScore.fullShots.length}
                                    disabled
                                    aria-label="strokes"
                                />
                            </td>
                            <td>
                                <input
                                    type="text"
                                    class="stats-control form-control"
                                    bind:value={holeScore.putts.length}
                                    disabled
                                    aria-label="putts"
                                />
                            </td>
                            <td>
                                <span class="score" style={scoreUtils.getScoreElementBorder(holeScore.fullShots.length + holeScore.putts.length, hole?.par)}>
                                    {holeScore.fullShots.length + holeScore.putts.length}
                                </span>
                            </td>
                            <td>
                                <input
                                    class="score-checkbox form-check-input"
                                    type="checkbox"
                                    bind:checked={holeScore.stats.greenLightDrive}
                                />
                            </td>
                            <td>
                                <input
                                    class="score-checkbox form-check-input"
                                    type="checkbox"
                                    bind:checked={holeScore.stats.greenInRegulation}
                                />
                            </td>
                            <td>
                                {#if holeScore.stats && holeScore.stats.greenInRegulation}
                                    <span class="disabled-checkbox-placeholder">-</span>
                                {:else}
                                    <input
                                        class="score-checkbox form-check-input"
                                        type="checkbox"
                                        bind:checked={holeScore.stats.scrambling}
                                    />
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
                            <th scope="col">Start</th>
                            <th scope="col">End</th>
                            <th scope="col">Penalty</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody>
                        {#if holeScore?.fullShots && holeScore?.putts}
                            {#each { length: holeScore.fullShots.length } as _, strokeIndex}
                                <tr>
                                    <td>{strokeIndex + 1}</td>
                                    <td class={holeScore.fullShots[strokeIndex].penalty ? "penalty-cell" : ""}>
                                        <select
                                            class="form-select"
                                            id="floatingSelect"
                                            aria-label="club-select"
                                            bind:value={holeScore.fullShots[strokeIndex].club}
                                        >
                                            <option selected>Club</option>
                                            {#each clubs as club}
                                                <option value={club}>
                                                    {club}
                                                </option>
                                            {/each}
                                        </select>
                                    </td>
                                    <td class={holeScore.fullShots[strokeIndex].penalty ? "penalty-cell" : ""}>
                                        {#if selectedPoints && selectedPoints.length >= strokeIndex + 2}
                                            <span>
                                                {geo.getDistanceFromLatLonInYards(
                                                    selectedPoints[strokeIndex][0],
                                                    selectedPoints[strokeIndex][1],
                                                    selectedPoints[strokeIndex + 1][0],
                                                    selectedPoints[strokeIndex + 1][1],
                                                ).toFixed(1)}
                                            </span>
                                        {/if}
                                    </td>
                                    <td class={holeScore.fullShots[strokeIndex].penalty ? "penalty-cell" : ""}>
                                        {#if selectedPoints && selectedPoints.length >= strokeIndex + 2 && hole && hole.centerGreenPoint}
                                            <span>
                                                {geo.getDistanceFromLatLonInYards(
                                                    hole.centerGreenPoint[0],
                                                    hole.centerGreenPoint[1],
                                                    selectedPoints[strokeIndex + 1][0],
                                                    selectedPoints[strokeIndex + 1][1],
                                                ).toFixed(1)}
                                            </span>
                                        {/if}
                                    </td>
                                    <td class="shot-coords {holeScore.fullShots[strokeIndex].penalty ? "penalty-cell" : null}">
                                        {#key selectedPoints}
                                            <button
                                                class="btn btn-small {strokeIndex === 0 ? "btn-warning" : "btn-primary"} coordinate"
                                                on:click={() => handleSetTargetCoordinate(strokeIndex)}
                                            >
                                                {getFormattedCoordinateText(strokeIndex)}
                                            </button>
                                        {/key}
                                    </td>
                                    <td class="shot-coords {holeScore.fullShots[strokeIndex].penalty ? "penalty-cell" : null}">
                                        {#key selectedPoints}
                                            <button
                                                class="btn btn-small btn-primary coordinate"
                                                on:click={() => handleSetTargetCoordinate(strokeIndex + 1)}
                                            >
                                                {getFormattedCoordinateText(strokeIndex + 1)}
                                            </button>
                                        {/key}
                                    </td>
                                    <td>
                                        <input
                                            class="penalty-checkbox form-check-input"
                                            type="checkbox"
                                            bind:checked={holeScore.fullShots[strokeIndex].penalty}
                                        />
                                    </td>
                                    <td>
                                        <button class="btn btn-danger" on:click={() => removeStroke(strokeIndex)}>
                                            <i class="fa-solid fa-trash"></i>
                                        </button>
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
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody>
                        {#if holeScore?.fullShots && holeScore?.putts}
                            {#each { length: holeScore.putts.length ?? 0 } as _, puttIndex}
                                <tr>
                                    <td>{holeScore.fullShots.length + puttIndex + 1}</td>
                                    <td>{puttIndex + 1}</td>
                                    <td>
                                        <input
                                            class="form-control"
                                            type="text"
                                            bind:value={holeScore.putts[puttIndex].distance}
                                        />
                                    </td>
                                    <td>
                                        <button class="btn btn-small btn-danger" on:click={() => removePutt(puttIndex)}>
                                            <i class="fa-solid fa-trash"></i>
                                        </button>
                                    </td>
                                </tr>
                            {/each}
                        {/if}
                    </tbody>
                </table>
            </div>
            <div class="card-buttons">
                <div class="card-right">
                    {#if hole?.holeNumber !== 1}
                        <a href="/" on:click|preventDefault={saveAndGoToPrevious} class="btn btn-success">
                            <i class="fa-solid fa-arrow-left"></i> Previous
                        </a>
                    {/if}
                    {#if hole?.holeNumber < round.holesCompleted}
                        <a href="/" on:click|preventDefault={saveAndGoToNext} class="btn btn-success">
                            <i class="fa-solid fa-arrow-right"></i> Save and go to next
                        </a>
                    {:else}
                        <a href="/" on:click|preventDefault={advance} class="btn btn-success">
                            <i class="fa-solid fa-check"></i> Finish Round
                        </a>
                    {/if}
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    td {
        text-align: center;
        vertical-align: middle;
    }
    .tee-color {
        display: block;
        width: 35px;
        height: 24px;
        border: 2px solid black;
        border-radius: 20px;
        margin: 0 10px 0 15px;
    }
    .score {
        padding: 3px 8px;
    }
    .score-checkbox {
        width: 1.75em;
        height: 1.75em;
        display: block;
        margin: auto;
        margin-top: 5px;
    }
    .score-entry {
        display: flex;
        flex-direction: row;
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
        border-color: rgba(139, 0, 0, 0.25);
        box-shadow: 0 0 0 0.25rem rgba(139, 0, 0, 0.25);
    }
    .card-title {
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    .title-section {
        margin: 0 5px;
    }
    .card-title-emphasize {
        font-size: 18pt;
        font-weight: bold;
    }
    .tee-select-section {
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    .par-badge {
        margin: 0 0 0 auto;
    }
    .card-right {
        float: right;
    }
    .stats-control {
        border: 0;
    }
    .shot-coords {
        font-size: 9pt;
    }
    .putting-entry {
        width: 250px;
    }
    .disabled-checkbox-placeholder {
        text-align: center;
        font-size: 18pt;
        color: #555;
        display: block;
        margin: auto;
    }

    .penalty-cell {
        background: repeating-linear-gradient(
            -45deg,
            #ee2222,
            #ee2222 10px,
            white 10px,
            white 20px
        );
    }
    .penalty-cell > * {
        display: none;  
    }
</style>
