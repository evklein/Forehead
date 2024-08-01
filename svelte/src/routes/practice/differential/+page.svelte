<script lang="ts">
    import { onMount } from 'svelte';
    import * as api from '../../../services/api';
    import LoadSpinner from '../../../components/shared/LoadSpinner.svelte';
    import type { DifferentialResults } from '../../../models/DifferentialResults';

    let faceStrikeToeResults: boolean[] = [];
    let faceStrikeHeelResults: boolean[] = [];
    let faceStrikeSweetSpotResults: boolean[] = [];
    let groundStrikeTopResults: boolean[] = [];
    let groundStrikeThinResults: boolean[] = [];
    let groundStrikeFatResults: boolean[] = [];
    let groundStrikeGoodResults: boolean[] = [];
    let directionDrawResults: boolean[] = [];
    let directionFadeReulsts: boolean[] = [];
    let directionStraightResults: boolean[] = [];

    let recentDifferentialResults: DifferentialResults[] = [];
    let numberOfRowsForEachCategory: number = 3;
    let loadingPreviousPracticeSessions: boolean = false;
    let savingNewDrill: boolean = false;

    function resetValues() {
        faceStrikeToeResults = Array(numberOfRowsForEachCategory).fill(false);
        faceStrikeHeelResults = Array(numberOfRowsForEachCategory).fill(false);
        faceStrikeSweetSpotResults = Array(numberOfRowsForEachCategory).fill(false);
        groundStrikeTopResults = Array(numberOfRowsForEachCategory).fill(false);
        groundStrikeThinResults = Array(numberOfRowsForEachCategory).fill(false);
        groundStrikeFatResults = Array(numberOfRowsForEachCategory).fill(false);
        groundStrikeGoodResults = Array(numberOfRowsForEachCategory).fill(false);
        directionDrawResults = Array(numberOfRowsForEachCategory).fill(false);
        directionFadeReulsts = Array(numberOfRowsForEachCategory).fill(false);
        directionStraightResults = Array(numberOfRowsForEachCategory).fill(false);
    }

    onMount(async () => {
        resetValues();
        loadingPreviousPracticeSessions = true;
        await getRecentDifferentialResults();
        loadingPreviousPracticeSessions = false;
    });

    async function getRecentDifferentialResults() {
        recentDifferentialResults = (await api.getRecentDifferentialResults()) ?? [];
    }

    async function saveCalibrationResults() {
        savingNewDrill = true;
        let drillData = JSON.stringify({
            toes: faceStrikeToeResults,
            heels: faceStrikeHeelResults,
            sweetSpots: faceStrikeSweetSpotResults,
            tops: groundStrikeTopResults,
            thins: groundStrikeThinResults,
            fats: groundStrikeFatResults,
            goodStrikes: groundStrikeGoodResults,
            draws: directionDrawResults,
            fades: directionFadeReulsts,
            straight: directionStraightResults,
        });
        await api.saveDrillResults(drillData, 'differential');
        resetValues();
        await getRecentDifferentialResults();
        savingNewDrill = false;
    }
</script>

<div class="row align-items-start">
    <div class="col-12 col-md-12">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">Differential Practice</h2>
                <div class="sub-table">
                    <div class="table-section-label">
                        <span>Face Strike</span>
                    </div>
                    <table class=" table table-bordered">
                        <thead>
                            <tr>
                                <th scope="col" class="table-col-third">Toe</th>
                                <th scope="col" class="table-col-third">Heel</th>
                                <th scope="col" class="table-col-third">Sweet Spot</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each { length: numberOfRowsForEachCategory } as _, index}
                                <tr>
                                    <td
                                        class=" {index === numberOfRowsForEachCategory - 1 ? 'last-cell-in-row' : null}"
                                    >
                                        <input
                                            class="score form-check-input"
                                            type="checkbox"
                                            bind:checked={faceStrikeToeResults[index]}
                                        />
                                    </td>
                                    <td
                                        class=" {index === numberOfRowsForEachCategory - 1 ? 'last-cell-in-row' : null}"
                                    >
                                        <input
                                            class="score form-check-input"
                                            type="checkbox"
                                            bind:checked={faceStrikeHeelResults[index]}
                                        />
                                    </td>
                                    <td
                                        class=" {index === numberOfRowsForEachCategory - 1 ? 'last-cell-in-row' : null}"
                                    >
                                        <input
                                            class="score form-check-input"
                                            type="checkbox"
                                            bind:checked={faceStrikeSweetSpotResults[index]}
                                        />
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
                <div class="sub-table">
                    <div class="table-section-label">
                        <span>Ground Strike</span>
                    </div>
                    <table class=" table table-bordered">
                        <thead>
                            <tr>
                                <th scope="col" class="table-col-fourth">Top</th>
                                <th scope="col" class="table-col-fourth">Thin</th>
                                <th scope="col" class="table-col-fourth">Fat</th>
                                <th scope="col" class="table-col-fourth">Good</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each { length: numberOfRowsForEachCategory } as _, index}
                                <tr>
                                    <td
                                        class=" {index === numberOfRowsForEachCategory - 1 ? 'last-cell-in-row' : null}"
                                    >
                                        <input
                                            class="score form-check-input"
                                            type="checkbox"
                                            bind:checked={groundStrikeTopResults[index]}
                                        />
                                    </td>
                                    <td
                                        class="table-col-fourth {index === numberOfRowsForEachCategory - 1
                                            ? 'last-cell-in-row'
                                            : null}"
                                    >
                                        <input
                                            class="score form-check-input"
                                            type="checkbox"
                                            bind:checked={groundStrikeThinResults[index]}
                                        />
                                    </td>
                                    <td
                                        class="table-col-fourth {index === numberOfRowsForEachCategory - 1
                                            ? 'last-cell-in-row'
                                            : null}"
                                    >
                                        <input
                                            class="score form-check-input"
                                            type="checkbox"
                                            bind:checked={groundStrikeFatResults[index]}
                                        />
                                    </td>
                                    <td
                                        class="table-col-fourth {index === numberOfRowsForEachCategory - 1
                                            ? 'last-cell-in-row'
                                            : null}"
                                    >
                                        <input
                                            class="score form-check-input"
                                            type="checkbox"
                                            bind:checked={groundStrikeGoodResults[index]}
                                        />
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
                <div class="sub-table">
                    <div class="table-section-label">
                        <span>Direction</span>
                    </div>
                    <table class=" table table-bordered">
                        <thead>
                            <tr>
                                <th scope="col" class="table-col-third">Draw</th>
                                <th scope="col" class="table-col-third">Fade</th>
                                <th scope="col" class="table-col-third">Straight</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each { length: numberOfRowsForEachCategory } as _, index}
                                <tr>
                                    <td
                                        class=" {index === numberOfRowsForEachCategory - 1 ? 'last-cell-in-row' : null}"
                                    >
                                        <input
                                            class="score form-check-input"
                                            type="checkbox"
                                            bind:checked={directionDrawResults[index]}
                                        />
                                    </td>
                                    <td
                                        class=" {index === numberOfRowsForEachCategory - 1 ? 'last-cell-in-row' : null}"
                                    >
                                        <input
                                            class="score form-check-input"
                                            type="checkbox"
                                            bind:checked={directionFadeReulsts[index]}
                                        />
                                    </td>
                                    <td
                                        class=" {index === numberOfRowsForEachCategory - 1 ? 'last-cell-in-row' : null}"
                                    >
                                        <input
                                            class="score form-check-input"
                                            type="checkbox"
                                            bind:checked={directionStraightResults[index]}
                                        />
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="lower-buttons btn-group">
                <button
                    type="button"
                    class="btn btn-lg btn-success"
                    on:click={saveCalibrationResults}
                    disabled={savingNewDrill}
                >
                    {#if savingNewDrill}
                        <LoadSpinner message={'Saving drill results'} />
                    {:else}
                        <i class="fa-solid fa-floppy-disk"></i> &nbsp;Save Results
                    {/if}
                </button>
                <button type="button" class="btn btn-lg btn-secondary" on:click={resetValues}> Restart </button>
            </div>
        </div>
        <div class="card mt-3">
            <div class="card-body">
                <h4 class="card-title">Previous Sessions</h4>
                {#if loadingPreviousPracticeSessions}
                    <LoadSpinner sizePx={28} message={'Loading previous sessions...'} />
                {:else}
                    <table class="results-table table table-bordered">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Toes</th>
                                <th>Heels</th>
                                <th>Sweet Spots</th>
                                <th>Tops</th>
                                <th>Thins</th>
                                <th>Fats</th>
                                <th>Good Strikes</th>
                                <th>Draws</th>
                                <th>Fades</th>
                                <th>Straights</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each recentDifferentialResults as recentDifferentialResult}
                                <tr>
                                    <td>{recentDifferentialResult.date.toLocaleDateString()}</td>
                                    <td>{recentDifferentialResult.numberOfToes}/3</td>
                                    <td>{recentDifferentialResult.numberOfHeels}/3</td>
                                    <td>{recentDifferentialResult.numberOfSweetSpots}/3</td>
                                    <td>{recentDifferentialResult.numberOfTops}/3</td>
                                    <td>{recentDifferentialResult.numberOfThins}/3</td>
                                    <td>{recentDifferentialResult.numberOfFats}/3</td>
                                    <td>{recentDifferentialResult.numberOfGoodStrikes}/3</td>
                                    <td>{recentDifferentialResult.numberOfDraws}/3</td>
                                    <td>{recentDifferentialResult.numberOfFades}/3</td>
                                    <td>{recentDifferentialResult.numberOfStraights}/3</td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    table {
        width: 100%;
        display: block;
    }
    .lower-buttons {
        padding: 12px;
    }
    .table {
        margin-bottom: 0;
    }
    .sub-table {
        display: flex;
        flex-direction: row;
    }
    .table-section-label {
        border: 1px solid rgb(222, 226, 230);
        border-right: none;
        padding: 12px;
        font-size: 18px;
        width: 140px;
        display: flex;
        align-items: center;
    }
    th {
        text-align: center;
    }
    td {
        text-align: center;
    }
    .table-col-third {
        width: 120px;
    }
    .table-col-fourth {
        width: 90px;
    }
    .last-cell-in-row {
        background: repeating-linear-gradient(-45deg, #a8eb8f, #a8eb8f 10px, #f4f7f2 10px, #f4f7f2 20px);
    }
    .results-table {
        overflow-x: scroll;
    }
</style>
