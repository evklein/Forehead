<script lang="ts">
    import type { HoleData } from '../../models/HoleData';
    import type { HoleScore } from '../../models/HoleScore';
    import * as geo from '../../services/geo';
    import * as api from '../../services/api';
    import * as scoreUtils from '../../services/scoreCardUtilities';
    import type { CourseData } from '../../models/CourseData';
    import type { RoundData } from '../../models/RoundData';
    import type { TeeData } from '../../models/TeeData';
    import { onMount } from 'svelte';
    import LoadSpinner from '../shared/LoadSpinner.svelte';

    // Props
    export let course: CourseData;
    export let courseTees: TeeData[];
    export let round: RoundData;
    export let hole: HoleData;
    export let holeScore: HoleScore;
    export let handleGoToNextHole: Function;
    export let handleGoToPreviousHole: Function;
    export let handleAdvance: Function;
    export let handleSetTargetCoordinate: Function;
    export let selectedShotCoordinateIndex: number;
    export let selectedShotCoordinateStart: boolean;

    let clubs: string[] = ['62°', '56°', '50°', 'P', '9', '8', '7', '6', '5', '4H', '3H', '3W', 'D'].reverse();
    let selectedTeeId: number | undefined = round.playedTeeId;
    let savingHole: boolean = false;

    function addFullShot(startCoordinates?: [number, number]) {
        let newStrokeNumber = holeScore.fullShots.length;

        holeScore.fullShots = [
            ...holeScore.fullShots,
            {
                penalty: false,
                startCoordinate: startCoordinates,
            },
        ];

        if (newStrokeNumber >= 1) {
            holeScore.fullShots[newStrokeNumber].startCoordinate =
                holeScore.fullShots[newStrokeNumber - 1].endCoordinate;
        }
    }

    async function removeStroke(strokeIndex: number) {
        holeScore.fullShots.splice(strokeIndex, 1);
        holeScore.fullShots = holeScore.fullShots; // Trigger re-render
    }

    function addPutt() {
        holeScore.putts = [
            ...holeScore.putts,
            {
                distance: 0,
            },
        ];
    }

    function handleFocus(event: FocusEvent): void {
        const target = event.target as HTMLInputElement;
        target.select();
    }

    function removePutt(puttIndex: number) {
        holeScore.putts.splice(puttIndex, 1);
        holeScore.putts = holeScore.putts;
    }

    function configureFullShotsForPenalty(targetedStrokeIndex: number) {
        let targetedStroke = holeScore.fullShots[targetedStrokeIndex];
        let prevStroke = holeScore.fullShots[targetedStrokeIndex - 1];
        let nextStroke = holeScore.fullShots[targetedStrokeIndex + 1];

        if (!targetedStroke.penalty) {
            targetedStroke.startCoordinate = undefined;
            targetedStroke.endCoordinate = undefined;

            if (nextStroke) {
                nextStroke.startCoordinate = undefined;
            }
        } else {
            if (prevStroke) {
                targetedStroke.startCoordinate = prevStroke.endCoordinate;
            }

            if (nextStroke) {
                targetedStroke.endCoordinate = nextStroke.startCoordinate;
            }
        }
    }

    function setTargetCoordinate(strokeNumber: number, start: boolean) {
        selectedShotCoordinateIndex = strokeNumber;
        selectedShotCoordinateStart = start;
        handleSetTargetCoordinate(strokeNumber, start);
    }

    $: coordinateButtonClass = (strokeIndex: number) => {
        let previousShot = holeScore.fullShots[strokeIndex - 1];
        if (strokeIndex === 0) return 'btn-warning';
        if (previousShot && previousShot.penalty) {
            return 'btn-danger';
        }
        return 'btn-primary';
    };
    $: coordinateButtonSelectedClass = (strokeIndex: number, start: boolean) => {
        if (strokeIndex === selectedShotCoordinateIndex && start === selectedShotCoordinateStart)
            return 'selected-coordinate';
        return '';
    };
    $: formattedStartCoordinate = (strokeIndex: number) => {
        let shot = holeScore.fullShots[strokeIndex];
        if (!shot.startCoordinate) {
            if (strokeIndex === 0) return 'Set tee-shot-location';
            let previousShot = holeScore.fullShots[strokeIndex - 1];
            if (previousShot && previousShot.penalty) {
                return 'Set drop location';
            }
            return 'Set start location';
        }
        console.log('Formatting!');
        console.log(shot);
        return `[${shot.startCoordinate?.[0].toFixed(5)}, ${shot.startCoordinate?.[1].toFixed(5)}]`;
    };
    $: formattedEndCoordinate = (strokeIndex: number) => {
        let shot = holeScore.fullShots[strokeIndex];
        if (!shot.endCoordinate) {
            return 'Set landing location';
        }
        return `[${shot.endCoordinate?.[0].toFixed(5)}, ${shot.endCoordinate?.[1].toFixed(5)}]`;
    };
    $: getFormattedDistanceToGreen = (strokeIndex: number) => {
        let fullShot = holeScore.fullShots[strokeIndex];
        if (fullShot && fullShot.startCoordinate && hole.centerGreenPoint) {
            return (
                geo
                    .getDistanceFromLatLonInYards(
                        fullShot.startCoordinate[0],
                        fullShot.startCoordinate[1],
                        hole.centerGreenPoint[0],
                        hole.centerGreenPoint[1],
                    )
                    .toFixed(1) + ' yards'
            );
        }
        return '-';
    };

    $: getFormattedDistanceForFullShot = (strokeIndex: number) => {
        let fullShot = holeScore.fullShots[strokeIndex];
        if (fullShot.startCoordinate && fullShot.endCoordinate && hole.centerGreenPoint) {
            return (
                geo
                    .getDistanceFromLatLonInYards(
                        fullShot.startCoordinate[0],
                        fullShot.startCoordinate[1],
                        fullShot.endCoordinate[0],
                        fullShot.endCoordinate[1],
                    )
                    .toFixed(1) + ' yards'
            );
        }
        return '-';
    };

    async function saveAll() {
        savingHole = true;
        if (round.id && hole.id) {
            await api.purgeHoleShots(round.id, hole.id);
            await api.saveHoleStats(round.id, hole.id, holeScore.stats);
        }

        for (let index = 0; index < holeScore.fullShots.length; index++) {
            let stroke = holeScore.fullShots[index];
            if (round.id && hole.id) {
                stroke.distance = geo.getDistanceFromLatLonInYards(
                    stroke.startCoordinate?.[0] ?? 0,
                    stroke.startCoordinate?.[1] ?? 0,
                    stroke.endCoordinate?.[0] ?? 0,
                    stroke.endCoordinate?.[1] ?? 0,
                );
                stroke.strokeNumber = index + 1;
                await api.saveStroke(round.id, hole.id, stroke);
            }
        }

        for (let index = 0; index < holeScore.putts.length; index++) {
            let putt = holeScore.putts[index];
            if (round.id && hole.id) {
                putt.strokeNumber = holeScore.fullShots.length + index + 1;
                await api.savePutt(round.id, hole.id, putt);
            }
        }
        savingHole = false;
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
                <div class="row align-items-start">
                    <span class="col-sm-6 col-lg-3 title-section card-title-emphasize">
                        Hole {hole?.holeNumber}
                    </span>
                    <span class="col-sm-6 col-lg-3 title-section">
                        {course.name}
                    </span>
                    <span class="col-sm-12 col-lg-3 title-section approximate-yardage">
                        <i class="fas fa-arrows-alt-h"></i> &nbsp;{getFormattedDistanceToGreen(0)}
                    </span>
                    <span class="col-sm-12 col-lg-3 title-section tee-select-section">
                        {#if courseTees}
                            <span
                                class="tee-color"
                                style="background: #{courseTees.filter((t) => t.id === selectedTeeId)[0]?.color}"
                            ></span>
                            <select class="tee-select form-select" aria-label="tee-select" bind:value={selectedTeeId}>
                                {#each courseTees as tee}
                                    <option value={tee.id}>
                                        {tee.name}
                                    </option>
                                {/each}
                            </select>
                        {/if}
                    </span>
                </div>
                <!-- <span class="title-section par-badge badge text-bg-success">Par {hole?.par}</span> -->
            </h5>
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
                                <span
                                    class="score"
                                    style={scoreUtils.getScoreElementBorder(
                                        holeScore.fullShots.length + holeScore.putts.length,
                                        hole?.par,
                                    )}
                                >
                                    {holeScore.fullShots.length + holeScore.putts.length}
                                </span>
                            </td>
                            <td>
                                {#if hole?.par === 3}
                                    <span class="disabled-checkbox-placeholder">-</span>
                                {:else}
                                    <input
                                        class="score-checkbox form-check-input"
                                        type="checkbox"
                                        bind:checked={holeScore.stats.greenLightDrive}
                                    />
                                {/if}
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
        </div>
    </div>
    <div class="card mt-2">
        <div class="card-body">
            <div class="card-title">
                <h2>Enter Full Shots</h2>
                <button class="btn btn-primary btn-right" on:click={() => addFullShot()}>Add Full Shot</button>
            </div>
            <div class="shot-entry">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th style="width: 30px" scope="col">Stroke</th>
                            <th scope="col">Club</th>
                            <th scope="col">Start</th>
                            <th scope="col">End</th>
                            <th scope="col">Penalty</th>
                            <th scope="col">Distance (Yards)</th>
                            <th scope="col">To Center</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody>
                        {#if holeScore?.fullShots && holeScore?.putts}
                            {#each { length: holeScore.fullShots.length } as _, strokeIndex}
                                <tr>
                                    <td>{strokeIndex + 1}</td>
                                    <td class={holeScore.fullShots[strokeIndex].penalty ? 'penalty-cell' : ''}>
                                        <select
                                            class="form-select club-select"
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
                                    <td
                                        class="shot-coords {holeScore.fullShots[strokeIndex].penalty
                                            ? 'penalty-cell'
                                            : null}"
                                    >
                                        <button
                                            class="btn btn-small coordinate-button {coordinateButtonClass(
                                                strokeIndex,
                                            )} {coordinateButtonSelectedClass(strokeIndex, true)} coordinate"
                                            on:click={() => setTargetCoordinate(strokeIndex, true)}
                                        >
                                            {formattedStartCoordinate(strokeIndex)}
                                        </button>
                                    </td>
                                    <td
                                        class="shot-coords {holeScore.fullShots[strokeIndex].penalty
                                            ? 'penalty-cell'
                                            : null}"
                                    >
                                        <button
                                            class="btn btn-small coordinate-button btn-primary {coordinateButtonSelectedClass(
                                                strokeIndex,
                                                false,
                                            )} coordinate"
                                            on:click={() => setTargetCoordinate(strokeIndex, false)}
                                        >
                                            {formattedEndCoordinate(strokeIndex)}
                                        </button>
                                    </td>
                                    <td>
                                        <input
                                            class="penalty-checkbox form-check-input"
                                            type="checkbox"
                                            on:change={() => configureFullShotsForPenalty(strokeIndex)}
                                            bind:checked={holeScore.fullShots[strokeIndex].penalty}
                                        />
                                    </td>
                                    <td class={holeScore.fullShots[strokeIndex].penalty ? 'penalty-cell' : ''}>
                                        <span>{getFormattedDistanceForFullShot(strokeIndex)}</span>
                                    </td>
                                    <td class={holeScore.fullShots[strokeIndex].penalty ? 'penalty-cell' : ''}>
                                        <span>{getFormattedDistanceToGreen(strokeIndex)}</span>
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
        </div>
    </div>
    <div class="card mt-2">
        <div class="card-body">
            <slot />
        </div>
    </div>
    <div class="card mt-2">
        <div class="card-body">
            <div class="card-title">
                <h2>Add Putts</h2>
                <button class="btn btn-info btn-right" on:click={addPutt}>Add Putt</button>
            </div>
            <div class="putting-entry">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th scope="col">Stroke</th>
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
                                            on:focus={handleFocus}
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
        </div>
    </div>
    <div class="mt-2">
        {#if hole?.holeNumber !== 1}
            <a href="/" on:click|preventDefault={saveAndGoToPrevious} class="btn btn-success">
                <i class="fa-solid fa-arrow-left"></i> Previous
            </a>
        {/if}
        {#if hole?.holeNumber < round.holesCompleted}
            <button on:click|preventDefault={saveAndGoToNext} class="btn btn-success" disabled={savingHole}>
                {#if savingHole}
                    <LoadSpinner message={'Saving hole'} />
                {:else}
                    <i class="fa-solid fa-arrow-right"></i> Save and go to next
                {/if}
            </button>
        {:else}
            <a href="/" on:click|preventDefault={advance} class="btn btn-success">
                <i class="fa-solid fa-check"></i> Finish Round
            </a>
        {/if}
    </div>
{/if}

<style>
    .coordinate-button {
        font-size: 12px;
    }
    .club-select {
        width: 80px;
    }
    .btn-right {
        margin-left: auto;
    }
    .table {
        margin-bottom: 0;
    }
    td {
        text-align: center;
        vertical-align: middle;
    }
    .tee-color {
        display: block;
        width: 27px;
        height: 25px;
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
    .shot-entry {
        overflow-x: scroll;
    }
    .penalty-cell {
        background: repeating-linear-gradient(-45deg, #ee2222, #ee2222 10px, white 10px, white 20px);
    }
    .penalty-cell > * {
        display: none;
    }

    @media only screen and (max-width: 799px) {
        .tee-color {
            margin-left: 0px;
        }
    }

    .selected-coordinate {
        border: 3px dotted red;
    }
</style>
