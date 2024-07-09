<script lang="ts">
    import { onMount } from 'svelte';
    import type { PracticeShotType } from '../../../models/PracticeShot';
    import type { PracticeStrokeData } from '../../../models/PracticeStrokeData';
    import * as api from '../../../services/api';

    let shotTypes: PracticeShotType[] = [
        {
            name: 'Drive',
            minAllowedDistance: 200,
            maxAllowedDistance: 260,
            showLineOptions: true,
            showDistanceOptions: true,
            showShapeOptions: true,
        },
        {
            name: 'Approach',
            minAllowedDistance: 110,
            maxAllowedDistance: 210,
            showLineOptions: true,
            showDistanceOptions: true,
            showShapeOptions: true,
        },
        {
            name: 'Punch',
            minAllowedDistance: 110,
            maxAllowedDistance: 200,
            showLineOptions: true,
            showDistanceOptions: true,
            showShapeOptions: true,
        },
        {
            name: 'Knockdown',
            minAllowedDistance: 50,
            maxAllowedDistance: 100,
            showLineOptions: true,
            showDistanceOptions: true,
            showShapeOptions: false,
        },
        {
            name: 'Pitch',
            minAllowedDistance: 50,
            maxAllowedDistance: 100,
            showLineOptions: true,
            showDistanceOptions: true,
            showShapeOptions: false,
        },
        {
            name: 'Chip',
            minAllowedDistance: 5,
            maxAllowedDistance: 40,
            showLineOptions: true,
            showDistanceOptions: true,
            showShapeOptions: false,
        },
        {
            name: 'Flop',
            minAllowedDistance: 5,
            maxAllowedDistance: 40,
            showLineOptions: true,
            showDistanceOptions: true,
            showShapeOptions: false,
        },
    ];

    let currentShotType: PracticeShotType;
    let currentShotData: PracticeStrokeData;

    onMount(() => {
        goToNextShot();
    });

    function getYardageForCurrentShot(): number {
        let yardage =
            currentShotType.minAllowedDistance +
            Math.random() *
                (currentShotType.maxAllowedDistance -
                    currentShotType.minAllowedDistance);
        return Number(yardage.toFixed(0));
    }

    function goToNextShot() {
        let randomIndex = Math.floor(Math.random() * shotTypes.length);
        currentShotType = shotTypes[randomIndex];
        clearShotResults();
    }

    function clearShotResults() {
        currentShotData = {
            shotType: currentShotType.name,
            shotDistance: getYardageForCurrentShot(),
            misHit: 'None',
            resultSide: '',
            resultDistance: '',
            resultShapeDirection: '',
            resultShape: '',
        };
    }

    function skipShot() {
        goToNextShot();
    }

    async function saveShot() {
        await api.savePracticeStroke(currentShotData);
        clearShotResults();
    }

    async function saveAndGoToNextShot() {
        await saveShot();
        goToNextShot();
    }
</script>

<h1>Practice</h1>
<div class="row align-items-start">
    <div class="card">
        <div class="card-body">
            {#if currentShotType}
                <div class="card-title">
                    <div class="shot-type">{currentShotType.name}</div>
                    {#key currentShotType}
                        <div class="yardage">
                            {getYardageForCurrentShot()} yards
                        </div>
                    {/key}
                </div>
                <div class="row align-items-start">
                    <div class="selections row align-items-start">
                        <h4 class="selection-section-title">
                            <span class="badge bg-success"> Mis-hit </span>
                        </h4>
                        <div class="btn-group" role="group">
                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="mishit-radio"
                                id="mishit-none-radio"
                                value="None"
                                bind:group={currentShotData.misHit}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="mishit-none-radio">None</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="mishit-radio"
                                id="mishit-top-radio"
                                value="Top"
                                bind:group={currentShotData.misHit}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="mishit-top-radio">Top</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="mishit-radio"
                                id="mishit-fat-radio"
                                value="Fat"
                                bind:group={currentShotData.misHit}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="mishit-fat-radio">Fat</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="mishit-radio"
                                id="mishit-thin-radio"
                                value="Thin"
                                bind:group={currentShotData.misHit}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="mishit-thin-radio">Thin</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="mishit-radio"
                                id="mishit-shank-radio"
                                value="Shank"
                                bind:group={currentShotData.misHit}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="mishit-shank-radio">Shank</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="mishit-radio"
                                id="mishit-whiff-radio"
                                value="Whiff"
                                bind:group={currentShotData.misHit}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="mishit-whiff-radio">Whiff</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="mishit-radio"
                                id="mishit-toe-radio"
                                value="Toe"
                                bind:group={currentShotData.misHit}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="mishit-toe-radio">Toe</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="mishit-radio"
                                id="mishit-sky-radio"
                                value="Sky"
                                bind:group={currentShotData.misHit}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="mishit-sky-radio">Sky</label
                            >
                        </div>
                    </div>
                    <div class="selections row align-items-start">
                        <h4 class="selection-section-title">
                            <span class="badge bg-success"> Landing </span>
                        </h4>
                        <div class="btn-group" role="group">
                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="line-radio"
                                id="left-radio"
                                value="Left"
                                bind:group={currentShotData.resultSide}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="left-radio">Left</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="line-radio"
                                id="straight-radio"
                                value="Straight"
                                bind:group={currentShotData.resultSide}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="straight-radio">Straight</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="line-radio"
                                id="right-radio"
                                value="Right"
                                bind:group={currentShotData.resultSide}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="right-radio">Right</label
                            >
                        </div>
                        <div class="btn-group" role="group">
                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="distance-radio"
                                id="short-radio"
                                value="Short"
                                bind:group={currentShotData.resultDistance}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="short-radio">Short</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="distance-radio"
                                id="on-radio"
                                value="On"
                                bind:group={currentShotData.resultDistance}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="on-radio">On</label
                            >

                            <input
                                type="radio"
                                class="btn-check btn-lg"
                                name="distance-radio"
                                id="long-radio"
                                value="Long"
                                bind:group={currentShotData.resultDistance}
                            />
                            <label
                                class="btn btn-outline-primary"
                                for="long-radio">Long</label
                            >
                        </div>
                    </div>
                    {#if currentShotType.showShapeOptions}
                        <div class="selections row align-items-start">
                            <h4 class="selection-section-title">
                                <span class="badge bg-info"> Shot Shape </span>
                            </h4>
                            <div class="btn-group" role="group">
                                <input
                                    type="radio"
                                    class="btn-check btn-lg"
                                    name="direction-radio"
                                    id="pull-radio"
                                    value="Pull"
                                    bind:group={currentShotData.resultShapeDirection}
                                />
                                <label
                                    class="btn btn-outline-primary"
                                    for="pull-radio">Pull</label
                                >

                                <input
                                    type="radio"
                                    class="btn-check btn-lg"
                                    name="direction-radio"
                                    id="straight-radio-2"
                                    value="Straight"
                                    bind:group={currentShotData.resultShapeDirection}
                                />
                                <label
                                    class="btn btn-outline-primary"
                                    for="straight-radio-2">Straight</label
                                >

                                <input
                                    type="radio"
                                    class="btn-check btn-lg"
                                    name="direction-radio"
                                    id="push-radio"
                                    value="Push"
                                    bind:group={currentShotData.resultShapeDirection}
                                />
                                <label
                                    class="btn btn-outline-primary"
                                    for="push-radio">Push</label
                                >
                            </div>
                            <div class="btn-group" role="group">
                                <input
                                    type="radio"
                                    class="btn-check btn-lg"
                                    name="shape-radio"
                                    id="hook-radio"
                                    value="Hook"
                                    bind:group={currentShotData.resultShape}
                                />
                                <label
                                    class="btn btn-outline-primary"
                                    for="hook-radio">Hook</label
                                >

                                <input
                                    type="radio"
                                    class="btn-check btn-lg"
                                    name="shape-radio"
                                    id="draw-radio"
                                    value="Draw"
                                    bind:group={currentShotData.resultShape}
                                />
                                <label
                                    class="btn btn-outline-primary"
                                    for="draw-radio">Draw</label
                                >

                                <input
                                    type="radio"
                                    class="btn-check btn-lg"
                                    name="shape-radio"
                                    id="straight-radio-3"
                                    value="Straight"
                                    bind:group={currentShotData.resultShape}
                                />
                                <label
                                    class="btn btn-outline-primary"
                                    for="straight-radio-3">Straight</label
                                >

                                <input
                                    type="radio"
                                    class="btn-check btn-lg"
                                    name="shape-radio"
                                    id="fade-radio"
                                    value="Fade"
                                    bind:group={currentShotData.resultShape}
                                />
                                <label
                                    class="btn btn-outline-primary"
                                    for="fade-radio">Fade</label
                                >

                                <input
                                    type="radio"
                                    class="btn-check btn-lg"
                                    name="shape-radio"
                                    id="slice-radio"
                                    value="Slice"
                                    bind:group={currentShotData.resultShape}
                                />
                                <label
                                    class="btn btn-outline-primary"
                                    for="slice-radio">Slice</label
                                >
                            </div>
                        </div>
                    {/if}
                </div>
            {/if}
        </div>
        <div class="lower-buttons">
            <button
                type="button"
                class="btn btn-lg btn-danger"
                on:click={skipShot}>Skip shot</button
            >
            <button
                type="button"
                class="btn btn-lg btn-primary"
                on:click={saveShot}>Save shot</button
            >
            <button
                type="button"
                class="btn btn-lg btn-success"
                on:click={saveAndGoToNextShot}>Save and next shot</button
            >
        </div>
    </div>
</div>

<style>
    .btn-group {
        margin: 10px 0;
    }
    .card-title {
        display: flex;
    }
    .card-title > .shot-type {
        font-size: 20pt;
        font-style: italic;
    }
    .card-title > .yardage {
        margin-left: auto;
        font-size: 18pt;
        font-weight: bold;
    }
    .selections {
        border: 1px solid #ccc;
        border-radius: 5px;
        margin: 20px 0;
        width: 100%;
        display: block;
        padding: 10px;
    }
    .selection-section-title {
        position: relative;
        top: -27px;
        margin-bottom: -27px;
    }

    .lower-buttons {
        float: right;
        margin: 0 0 10px auto;
        display: block;
    }
</style>
