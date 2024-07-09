<script lang="ts">
    import type { RoundData } from '../../../models/RoundData';
    import type { TeeData } from '../../../models/TeeData';
    import * as api from '../../../services/api';
    import type { CourseData } from '../../../models/CourseData';

    export let course: CourseData;
    export let round: RoundData;
    export let tees: TeeData[];
    export let handleAdvance: Function;

    let selectedTee: TeeData;

    async function advance() {
        console.log('SAVING: ' + course.name + ' ' + selectedTee.name);
        console.log(round);
        round.id = await api.saveRound(round, course.courseId, selectedTee.id);
        handleAdvance();
    }
</script>

<div class="row align-items-start">
    <div class="card">
        <div class="card-body">
            <h3 class="card-title">
                New Round
                <span class="course-detail"> // {course?.name}</span>
                <span class="date-detail">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="date-addon"
                            ><i class="fa fa-calendar"></i></span
                        >
                        <input
                            type="text"
                            class="form-control"
                            aria-describedby="date-addon"
                            placeholder="Date"
                            bind:value={round.datePlayed}
                        />
                    </div>
                </span>
            </h3>
            <div class="row align-items-start mt-5">
                <div class="col-3">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="tee-time-addon"
                            ><i class="fa fa-clock"></i></span
                        >
                        <input
                            type="text"
                            class="form-control"
                            aria-describedby="tee-time-addon"
                            bind:value={round.teeTime}
                            placeholder="Tee time"
                        />
                    </div>
                </div>
                <div class="col-3">
                    <div class="input-group mb-3">
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
                <div class="col-3">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="holes-addon"
                            ><i class="fa-regular fa-square-check"></i></span
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
                <div class="col-3">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="group-addon"
                            ><i class="fa-solid fa-golf-ball-tee"></i></span
                        >
                        <select
                            class="form-select"
                            id="floatingSelect"
                            aria-label="Floating label select example"
                            bind:value={selectedTee}
                        >
                            <option selected>Tee</option>
                            {#each tees as tee}
                                <option value={tee}>
                                    {tee.name}
                                </option>
                            {/each}
                        </select>
                    </div>
                </div>
                <div class="col-3">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="group-addon"
                            ><i class="fa-solid fa-user-group"></i></span
                        >
                        <select
                            class="form-select"
                            id="floatingSelect"
                            aria-label="Floating label select example"
                            bind:value={round.groupMakeup}
                        >
                            <option selected>Group</option>
                            <option value="Single">Single</option>
                            <option value="Randoms">Randoms</option>
                            <option value="Friends">Friends / Family</option>
                        </select>
                    </div>
                </div>
                <div class="col-3">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="group-addon"
                            ><i class="fa-solid fa-person-walking"></i></span
                        >
                        <select
                            class="form-select"
                            id="floatingSelect"
                            aria-label="Floating label select example"
                            bind:value={round.mobility}
                        >
                            <option selected>Mobility</option>
                            <option value="Walking">Walking</option>
                            <option value="Pushing">Pushing</option>
                            <option value="Carting">Carting</option>
                        </select>
                    </div>
                </div>
                <div class="col-6">
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
                <div class="col-11">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="bounds-addon"
                            ><i class="fa-solid fa-list"></i></span
                        >
                        <textarea
                            bind:value={round.notes}
                            class="form-control"
                            placeholder="Notes"
                            aria-describedby="bounds-addon"
                            rows="4"
                        />
                    </div>
                </div>
                <div class="card-buttons">
                    <button class="btn btn-success" on:click={advance}>
                        <i class="fa-solid fa-arrow-right"></i> Start Round
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .course-detail {
        font-size: 14pt;
    }
    .date-detail {
        float: right;
    }
</style>
