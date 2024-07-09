<script lang="ts">
    import type { EventHandler } from 'svelte/elements';
    import type { CourseData } from '../../../models/CourseData';
    import type { TeeData } from '../../../models/TeeData';

    export let course: CourseData;
    export let saveCourse: EventHandler;
    export let tees: TeeData[];
</script>

<div class="card">
    <div class="card-body">
        <h5 class="card-title">
            {course.name}
        </h5>
        <div class="row align-items-start mb-2">
            <div class="col-12 tee-box">
                {#each tees as tee}
                    <span
                        class="tee"
                        style="background: #{tee.color}"
                        title={tee.name}
                    ></span>
                {/each}
            </div>
        </div>
        <div class="row align-items-start">
            <div class="col-6">
                <div class="input-group mb-3 col-6">
                    <span class="input-group-text" id="par-addon"
                        ><i class="fa-solid fa-golf-ball-tee"></i></span
                    >
                    <input
                        type="number"
                        bind:value={course.par}
                        class="form-control"
                        aria-describedby="par-addon"
                        placeholder="Par"
                    />
                </div>
            </div>
            <div class="col-6">
                <div class="input-group mb-3">
                    <span class="input-group-text" id="number-of-holes-addon"
                        ><i class="fa-solid fa-flag"></i></span
                    >
                    <input
                        type="text"
                        class="form-control"
                        placeholder="Number of Holes"
                        aria-describedby="number-of-holes-addon"
                        bind:value={course.numberOfHoles}
                    />
                </div>
            </div>
        </div>
        <div class="input-group mb-3 col-6">
            <span class="input-group-text" id="address-addon"
                ><i class="fa-solid fa-location-dot"></i></span
            >
            <input
                type="text"
                bind:value={course.address}
                class="form-control"
                aria-describedby="address-addon"
                placeholder="Address"
            />
        </div>

        <div class="input-group mb-3">
            <span class="input-group-text" id="designer-addon"
                ><i class="fa-solid fa-signature"></i></span
            >
            <input
                type="text"
                class="form-control"
                placeholder="Designer"
                aria-describedby="designer-addon"
                bind:value={course.designer}
            />
        </div>
        <div class="input-group mb-3">
            <span class="input-group-text" id="bounds-addon"
                ><i class="fa-solid fa-map-pin"></i></span
            >
            <textarea
                class="form-control"
                placeholder="Bound Points"
                aria-describedby="bounds-addon"
                rows="9"
                value={JSON.stringify(course.boundPoints)}
            />
        </div>
        <div class="card-buttons">
            <a
                href="/"
                on:click|preventDefault={saveCourse}
                class="btn btn-success"
            >
                <i class="fa-solid fa-check"></i> Save Course
            </a>
        </div>
    </div>
</div>

<style>
    textarea {
        max-height: 400px;
    }
    .tee-box {
        display: flex;
        align-items: center;
        flex-direction: row;
    }
    .tee {
        margin: 2px;
        display: block;
        width: 20px;
        height: 20px;
        border: 2px solid black;
        border-radius: 40px;
    }
</style>
