<script lang="ts">
    import { onMount } from 'svelte';
    import * as api from '../../../services/api';

    let numberOfShots: number = 20;

    let groundStrikeOptions = ['Good', 'Thin', 'Fat'];
    let faceStrikeOptions = ['Sweet spot', 'Heel', 'Toe'];
    let directionOptions = ['Within Target Area', 'Left', 'Right'];
    let groundStrikeValues = Array(numberOfShots).fill('');
    let faceStrikeValues = Array(numberOfShots).fill('');
    let directionValues = Array(numberOfShots).fill('');

    onMount(async () => {});

    async function saveCalibrationResults() {
        let drillData = JSON.stringify({
            groundStrikeValues: groundStrikeValues,
            faceStrikeValues: faceStrikeValues,
            directionValues: directionValues,
        });
        await api.saveDrillResults(drillData, 'swing_calibration');
    }

    function resetValues() {
        groundStrikeValues = Array(numberOfShots).fill('');
        faceStrikeValues = Array(numberOfShots).fill('');
        directionValues = Array(numberOfShots).fill('');
    }
</script>

<div class="row align-items-start">
    <div class="col-12 col-md-8">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">Swing Calibration</h2>
                <table class="score-table table table-bordered">
                    <thead>
                        <tr>
                            <th scope="col"></th>
                            {#each { length: numberOfShots } as _, i}
                                <th scope="col">{i + 1}</th>
                            {/each}
                            <th scope="col">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Strike with Ground</td>
                            {#each { length: numberOfShots } as _, i}
                                <td>
                                    <select class="form-select" bind:value={groundStrikeValues[i]}>
                                        {#each groundStrikeOptions as groundStrikeOption}
                                            <option value={groundStrikeOption}>{groundStrikeOption}</option>
                                        {/each}
                                    </select>
                                </td>
                            {/each}
                            <td>
                                <span class="row-score"
                                    >{groundStrikeValues.filter((gs) => gs === groundStrikeOptions[0]).length} / {numberOfShots}</span
                                >
                            </td>
                        </tr>
                        <tr>
                            <td>Strike with Face</td>
                            {#each { length: numberOfShots } as _, i}
                                <td>
                                    <select class="form-select" bind:value={faceStrikeValues[i]}>
                                        {#each faceStrikeOptions as faceStrikeOption}
                                            <option value={faceStrikeOption}>{faceStrikeOption}</option>
                                        {/each}
                                    </select>
                                </td>
                            {/each}
                            <td
                                ><span class="row-score"
                                    >{faceStrikeValues.filter((fs) => fs === faceStrikeOptions[0]).length} / {numberOfShots}</span
                                >
                            </td>
                        </tr>
                        <tr>
                            <td>Direction</td>
                            {#each { length: numberOfShots } as _, i}
                                <td>
                                    <select class="form-select" bind:value={directionValues[i]}>
                                        {#each directionOptions as directionOption}
                                            <option value={directionOption}>{directionOption}</option>
                                        {/each}
                                    </select>
                                </td>
                            {/each}
                            <td
                                ><span class="row-score"
                                    >{directionValues.filter((d) => d === directionOptions[0]).length} / {numberOfShots}</span
                                ></td
                            >
                        </tr>
                    </tbody>
                </table>
                <div class="lower-buttons btn-group">
                    <button type="button" class="btn btn-lg btn-success" on:click={saveCalibrationResults}>
                        <i class="fa-solid fa-floppy-disk"></i> &nbsp;Save Results
                    </button>
                    <button type="button" class="btn btn-lg btn-secondary" on:click={resetValues}> Restart </button>
                </div>
            </div>
        </div>
    </div>
    <div class="col-12 col-md-4">
        <div class="card">
            <div class="card-body">
                <h4 class="card-title">Boundaries <b>(28 - 18 HCI)</b></h4>
                <ul>
                    <li>
                        <span
                            ><b>Ground Strike:</b> Divot must start <b>2 inches in front and 3 inches behind</b> the ball.</span
                        >
                    </li>
                    <li>
                        <span
                            ><b>Face Strike:</b> The strike with the face must at least be in the
                            <b>grooved area of the face.</b></span
                        >
                    </li>
                    <li>
                        <b>Direction:</b> Must finish within the following target ranges.
                        <table class="table table-bordered">
                            <thead>
                                <tr>
                                    <th scope="col">Club</th>
                                    <th scope="col">Target</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Sand Wedge</td>
                                    <td>5 yards</td>
                                </tr>
                                <tr>
                                    <td>Gap Wedge</td>
                                    <td>10 yards</td>
                                </tr>
                                <tr>
                                    <td>P Wedge</td>
                                    <td>15 Yards</td>
                                </tr>
                                <tr>
                                    <td>9 Iron</td>
                                    <td>20 yards</td>
                                </tr>
                                <tr>
                                    <td>8 Iron</td>
                                    <td>25 yards</td>
                                </tr>
                                <tr>
                                    <td>7 Iron</td>
                                    <td>30 yards</td>
                                </tr>
                                <tr>
                                    <td>6 Iron</td>
                                    <td>35 yards</td>
                                </tr>
                                <tr>
                                    <td>4 Hybrid</td>
                                    <td>40 yards</td>
                                </tr>
                                <tr>
                                    <td>4 Hybrid</td>
                                    <td>45 yards</td>
                                </tr>
                                <tr>
                                    <td>3 Hybrid</td>
                                    <td>50 yards</td>
                                </tr>
                                <tr>
                                    <td>Driver</td>
                                    <td>50 yards</td>
                                </tr>
                            </tbody>
                        </table>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>

<style>
    .score-table {
        overflow-x: scroll;
    }
    th:first-child,
    td:first-child {
        position: sticky;
        left: 0px;
    }
    th:last-child,
    td:last-child {
        position: sticky;
        right: 0px;
        width: 100px;
    }
    select {
        width: 150px;
    }
    table {
        width: 100%;
        display: block;
    }
    .row-score {
        width: 100px;
    }
</style>
