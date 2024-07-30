<script lang="ts">
    import { onMount } from 'svelte';
    import * as api from '../../../services/api';
    import type { PuttingCalibrationResultsData } from '../../../models/CalibrationResultsData';
    import LoadSpinner from '../../../components/shared/LoadSpinner.svelte';

    let numberOfShots: number = 20;

    let distanceControlOptions = ['Good', 'Short', 'Long'];
    let holeSideOptions = ['High', 'Low', 'Holed'];

    let distanceControlValues: string[] = [];
    let holeSideValues: string[] = [];
    let recentCalibrationResults: PuttingCalibrationResultsData[] = [];
    let loadingPreviousTests: boolean = false;
    let savingNewTest: boolean = false;

    function resetValues() {
        distanceControlValues = Array(numberOfShots).fill('');
        holeSideValues = Array(numberOfShots).fill('');
    }

    onMount(async () => {
        resetValues();
        loadingPreviousTests = true;
        await getRecentCalibrationResults();
        loadingPreviousTests = false;
    });

    async function getRecentCalibrationResults() {
        recentCalibrationResults = (await api.getRecentPuttingCalibrationResults()) ?? [];
    }

    async function saveCalibrationResults() {
        savingNewTest = true;
        let drillData = JSON.stringify({
            distanceControlValues: distanceControlValues,
            holeSideValues: holeSideValues,
        });
        await api.saveDrillResults(drillData, 'putting_calibration');
        resetValues();
        await getRecentCalibrationResults();
        savingNewTest = false;
    }
</script>

<div class="row align-items-start">
    <div class="col-12 col-md-8">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">Putting Calibration</h2>
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
                            <td>Distance Control</td>
                            {#each { length: numberOfShots } as _, i}
                                <td>
                                    <select class="form-select" bind:value={distanceControlValues[i]}>
                                        {#each distanceControlOptions as distanceControlOption}
                                            <option value={distanceControlOption}>{distanceControlOption}</option>
                                        {/each}
                                    </select>
                                </td>
                            {/each}
                            <td>
                                <span class="row-score"
                                    >{distanceControlValues.filter((dc) => dc === distanceControlOptions[0]).length} / {numberOfShots}</span
                                >
                            </td>
                        </tr>
                        <tr>
                            <td>Hole Side</td>
                            {#each { length: numberOfShots } as _, i}
                                <td>
                                    <select
                                        class="form-select"
                                        bind:value={holeSideValues[i]}
                                        disabled={distanceControlValues[i] !== 'Good'}
                                    >
                                        {#each holeSideOptions as holeSideOption}
                                            <option value={holeSideOption}>{holeSideOption}</option>
                                        {/each}
                                    </select>
                                </td>
                            {/each}
                            <td> </td>
                        </tr>
                    </tbody>
                </table>
                <div class="lower-buttons btn-group">
                    <button
                        type="button"
                        class="btn btn-lg btn-success"
                        on:click={saveCalibrationResults}
                        disabled={savingNewTest}
                    >
                        {#if savingNewTest}
                            <LoadSpinner message={'Saving calibration'} />
                        {:else}
                            <i class="fa-solid fa-floppy-disk"></i> &nbsp;Save Results
                        {/if}
                    </button>
                    <button type="button" class="btn btn-lg btn-secondary" on:click={resetValues}> Restart </button>
                </div>
            </div>
        </div>
        <div class="card mt-3">
            <div class="card-body">
                <h4 class="card-title">Previous Tests</h4>
                {#if loadingPreviousTests}
                    <LoadSpinner sizePx={28} message={'Loading calibrations...'} />
                {:else}
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Distance Control</th>
                                <th>Number Holed</th>
                                <th>High</th>
                                <th>Low</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each recentCalibrationResults as recentCalibrationResult}
                                <tr>
                                    <td>{recentCalibrationResult.date.toLocaleDateString()}</td>
                                    <td>{recentCalibrationResult.distanceControlSuccesses}/20</td>
                                    <td>{recentCalibrationResult.numberHoled}/20</td>
                                    <td
                                        >{recentCalibrationResult.holeSideHigh}/{recentCalibrationResult.distanceControlSuccesses}</td
                                    >
                                    <td
                                        >{recentCalibrationResult.holeSideLow}/{recentCalibrationResult.distanceControlSuccesses}</td
                                    >
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                {/if}
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
