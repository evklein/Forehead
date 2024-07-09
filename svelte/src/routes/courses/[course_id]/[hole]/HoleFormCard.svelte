<script lang="ts">
    import type { EventHandler } from 'svelte/elements';
    import type { HoleData } from '../../../../models/HoleData';

    export let courseId: number;
    export let holeNumber: number;
    export let courseName: string;
    export let hole: HoleData;
    export let saveHole: EventHandler;
</script>

<div class="card">
    <div class="card-body">
        <h5 class="card-title">
            {courseName}
            <div class="input-group hole-number">
                <span class="input-group-text" id="hole-addon"
                    ><i class="fa-solid fa-hashtag"></i></span
                >
                <input
                    type="text"
                    value={holeNumber}
                    disabled
                    class="form-control"
                    aria-describedby="hole-addon"
                    placeholder="Hole"
                />
            </div>
            <div class="next-and-prev">
                <div
                    class="btn-group mr-2"
                    role="group"
                    aria-label="First group"
                >
                    {#if holeNumber !== 1}
                        <a
                            href="/courses/{courseId}/{holeNumber - 1}"
                            rel="external"
                            class="btn btn-secondary"
                            ><i class="fa-solid fa-arrow-left"></i></a
                        >
                    {/if}
                    {#if holeNumber !== 18}
                        <a
                            href="/courses/{courseId}/{holeNumber + 1}"
                            rel="external"
                            class="btn btn-secondary"
                            ><i class="fa-solid fa-arrow-right"></i></a
                        >
                    {:else}
                        <a href="/courses/{courseId}" class="btn btn-success"
                            >Back to course page</a
                        >
                    {/if}
                </div>
            </div>
        </h5>
        <div class="input-group mb-3">
            <span class="input-group-text" id="name-addon"
                ><i class="fa fa-tag"></i></span
            >
            <input
                type="text"
                bind:value={hole.nickname}
                class="form-control"
                aria-describedby="name-addon"
                placeholder="Nickname"
            />
        </div>
        <div class="input-group mb-3">
            <span class="input-group-text" id="par-addon"
                ><i class="fa-solid fa-golf-ball-tee"></i></span
            >
            <input
                type="number"
                bind:value={hole.par}
                class="form-control"
                aria-describedby="par-addon"
                placeholder="Par"
            />
        </div>
        <div class="input-group mb-3">
            <span class="input-group-text" id="bounds-addon"
                ><i class="fa-solid fa-map-pin"></i></span
            >
            <textarea
                rows="9"
                class="form-control"
                placeholder="Bound Points"
                aria-describedby="bounds-addon"
                value={JSON.stringify(hole.boundPoints)}
            />
        </div>
        <div class="input-group mb-3">
            <span class="input-group-text" id="green-center-addon"
                ><i class="fas fa-location"></i></span
            >
            <input
                type="text"
                class="form-control"
                placeholder="Green Center Location"
                aria-describedby="green-center-addon"
                bind:value={hole.centerGreenPoint}
            />
        </div>
        <div class="card-buttons">
            <a
                href="/"
                on:click|preventDefault={saveHole}
                class="btn btn-success"
            >
                <i class="fa-solid fa-check"></i> Save Hole
            </a>
        </div>
    </div>
</div>

<style>
    .card-title {
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .hole-number {
        width: 90px;
        margin-left: 10px;
    }

    .next-and-prev {
        margin-left: auto;
    }
</style>
