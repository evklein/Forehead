<script lang="ts">
    import type { RoundData } from '../../../models/RoundData';
    import type { TeeData } from '../../../models/TeeData';
    import * as api from '../../../services/api';
    import type { CourseData } from '../../../models/CourseData';
    import { onMount } from 'svelte';

    export let continuing: boolean = false;
    export let course: CourseData;
    export let round: RoundData;
    export let tees: TeeData[];
    export let handleAdvance: Function;
    export let handleAdvanceToFinal: Function;

    async function advance() {
        round.id;
        if (round.id) {
            await api.updateRound(round);
        } else {
            round.id = await api.saveNewRound(round, course.courseId);
        }
        handleAdvance();
    }

    function advanceToFinalizePage() {
        handleAdvanceToFinal();
    }
</script>

<div class="row align-items-start">
    <div class="card">
        <div class="card-body">
            <h3 class="card-title">
                {continuing ? 'Continue round' : 'New Round'}
                <span class="course-detail"> // {course?.name}</span>
            </h3>
            <div class="row align-items-start mt-4">
                <div class="col-12 col-md-3 mb-3">
                    <div class="input-group">
                        <span class="input-group-text" id="date-addon"><i class="fa fa-calendar"></i></span>
                        <input
                            type="text"
                            class="form-control"
                            aria-describedby="date-addon"
                            placeholder="Date"
                            bind:value={round.datePlayed}
                        />
                    </div>
                </div>
                <div class="col-12 col-md-3 mb-3">
                    <div class="input-group">
                        <span class="input-group-text" id="tee-time-addon"><i class="fa fa-clock"></i></span>
                        <input
                            type="text"
                            class="form-control"
                            aria-describedby="tee-time-addon"
                            bind:value={round.teeTime}
                            placeholder="Tee time"
                        />
                    </div>
                </div>
                <div class="col-12 col-md-3 mb-3">
                    <div class="input-group">
                        <span class="input-group-text" id="finish-addon"
                            ><i class="fa-solid fa-flag-checkered"></i></span
                        >
                        <input
                            type="text"
                            class="form-control"
                            aria-describedby="finish-addon"
                            bind:value={round.finishTime}
                            placeholder="Finish time"
                        />
                    </div>
                </div>
                <div class="col-12 col-md-3 mb-3">
                    <div class="input-group">
                        <span class="input-group-text" id="holes-addon"><i class="fa-regular fa-square-check"></i></span
                        >
                        <input
                            type="text"
                            class="form-control"
                            aria-describedby="holes-addon"
                            bind:value={round.holesCompleted}
                            placeholder="Holes completed"
                        />
                    </div>
                </div>
                <div class="col-12 col-md-3 mb-3">
                    <div class="input-group">
                        <span class="input-group-text" id="tee-addon"><i class="fa-solid fa-golf-ball-tee"></i></span>
                        <select class="form-select" aria-label="Tee select" bind:value={round.playedTeeId}>
                            <option selected>Tee</option>
                            {#each tees as tee}
                                <option value={tee.id}>
                                    {tee.name}
                                </option>
                            {/each}
                        </select>
                    </div>
                </div>
                <div class="col-12 col-md-3 mb-3">
                    <div class="input-group">
                        <span class="input-group-text" id="group-addon"><i class="fa-solid fa-user-group"></i></span>
                        <select class="form-select" aria-label="Group select" bind:value={round.groupMakeup}>
                            <option selected>Group</option>
                            <option value="Single">Single</option>
                            <option value="Randoms">Randoms</option>
                            <option value="Friends">Friends / Family</option>
                            <option value="Mixed">Mixed</option>
                        </select>
                    </div>
                </div>
                <div class="col-12 col-md-3 mb-3">
                    <div class="input-group">
                        <span class="input-group-text" id="mobility-addon"
                            ><i class="fa-solid fa-person-walking"></i></span
                        >
                        <select class="form-select" aria-label="Mobility select" bind:value={round.mobility}>
                            <option selected>Mobility</option>
                            <option value="Walking">Walking</option>
                            <option value="Pushing">Pushing</option>
                            <option value="Carting">Carting</option>
                        </select>
                    </div>
                </div>
                <div class="col-12 mb-3">
                    <div class="form-check">
                        <input
                            class="form-check-input"
                            type="checkbox"
                            id="flexCheckDefault"
                            bind:value={round.roundCountsTowardHci}
                        />
                        <label class="form-check-label" for="flexCheckDefault">
                            Round counts toward Handicap Index
                        </label>
                    </div>
                </div>
                <div class="col-12 mb-3">
                    <div class="input-group">
                        <span class="input-group-text" id="notes-addon"><i class="fa-solid fa-list"></i></span>
                        <textarea
                            bind:value={round.notes}
                            class="form-control"
                            placeholder="Notes"
                            aria-describedby="notes-addon"
                            rows="4"
                        ></textarea>
                    </div>
                </div>
                <div class="col-12 text-center">
                    <button class="btn btn-success" on:click={advance}>
                        <i class="fa-solid fa-arrow-right"></i>
                        {continuing ? 'Continue ' : 'Start '} Round
                    </button>
                    {#if continuing}
                        <button class="btn btn-warning" on:click={advanceToFinalizePage}>
                            <i class="fa-solid fa-table"></i> View Scorecard
                        </button>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .course-detail {
        font-size: 14pt;
    }
</style>
