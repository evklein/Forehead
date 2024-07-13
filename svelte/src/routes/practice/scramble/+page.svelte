<script lang="ts">
    import { onMount } from 'svelte';
    import type { ScrambleGameData } from '../../../models/ScrambleGameData';
    import * as api from '../../../services/api';
    import type { ScrambleRoundData } from '../../../models/ScrambleRoundData';

    let scrambleGameData: ScrambleGameData = {
        holeChips: Array(18).fill(0),
        holePutts: Array(18).fill(0),
        holeYardages: Array(18).fill(0),
    };
    let recentRoundData: ScrambleRoundData[] = [];

    $: holeScores = scrambleGameData.holeChips.map((_, i) => getHoleScore(i));
    $: holeBorders = holeScores.map((score) => getBorderForHoleScore(score));
    $: totalChips = scrambleGameData.holeChips.reduce((total, nextValue) => total + Number(nextValue), 0);
    $: totalPutts = scrambleGameData.holePutts.reduce((total, nextValue) => total + Number(nextValue), 0);
    $: totalYards = scrambleGameData.holeYardages.reduce((total, nextValue) => total + Number(nextValue), 0);
    $: totalScore = totalChips + totalPutts;

    onMount(async () => {
        await getRecentRounds();

        let minYardage = 5;
        let maxYardage = 30;
        let newHoleYardages = [...scrambleGameData.holeYardages]; // Copy existing holeYardages

        for (let i = 0; i < 18; i += 3) {
            let nextYardage = Math.floor(Math.random() * (maxYardage - minYardage + 1)) + minYardage;
            newHoleYardages[i] = nextYardage;
            newHoleYardages[i + 1] = nextYardage;
            newHoleYardages[i + 2] = nextYardage;
        }

        scrambleGameData = {
            ...scrambleGameData,
            holeYardages: newHoleYardages,
        };
    });

    function getHoleScore(holeNumber: number): number {
        return (
            (Number(scrambleGameData.holeChips[holeNumber]) ?? 0) +
            (Number(scrambleGameData.holePutts[holeNumber]) ?? 0)
        );
    }

    function getBorderForHoleScore(score: number): string {
        if (score === 1) return 'border: 1px solid white; border-radius: 20px;';
        if (score === 2 || score === 0) return '';
        if (score === 3) return 'border: 1px solid white;';
        return 'border: 3px double white';
    }

    function handleFocus(event: FocusEvent): void {
        const target = event.target as HTMLInputElement;
        target.select();
    }

    async function getRecentRounds() {
        recentRoundData = (await api.getRecentUpDownRounds()) ?? [];
    }

    async function saveScrambleRound() {
        await api.savePracticeGame(scrambleGameData);
        await getRecentRounds();
    }
</script>

<div class="row align-items-start">
    <div class="col-12">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">Up & Down</h2>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th scope="col"></th>
                            {#each { length: 18 } as _, i}
                                <th scope="col">{i + 1}</th>
                            {/each}
                            <th scope="col">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Score</td>
                            {#each { length: 18 } as _, i}
                                <td>
                                    <span class="score-number" style={holeBorders[i]}>
                                        {holeScores[i]}
                                    </span>
                                </td>
                            {/each}
                            <td>
                                <b>
                                    {totalScore}
                                </b>
                            </td>
                        </tr>
                        <tr>
                            <td>In</td>
                            {#each { length: 18 } as _, i}
                                <td>
                                    <input
                                        class="form-control-sm"
                                        type="text"
                                        on:focus={handleFocus}
                                        bind:value={scrambleGameData.holeYardages[i]}
                                    />
                                </td>
                            {/each}
                            <td>
                                {totalYards}
                            </td>
                        </tr>
                        <tr>
                            <td>Chips</td>
                            {#each { length: 18 } as _, i}
                                <td>
                                    <input
                                        class="form-control-sm"
                                        type="text"
                                        on:focus={handleFocus}
                                        bind:value={scrambleGameData.holeChips[i]}
                                    />
                                </td>
                            {/each}
                            <td>{totalChips}</td>
                        </tr>
                        <tr>
                            <td>Putts</td>
                            {#each { length: 18 } as _, i}
                                <td>
                                    <input
                                        class="form-control-sm"
                                        type="text"
                                        on:focus={handleFocus}
                                        bind:value={scrambleGameData.holePutts[i]}
                                    />
                                </td>
                            {/each}
                            <td>{totalPutts}</td>
                        </tr>
                    </tbody>
                </table>
                <div class="lower-buttons btn-group">
                    <button type="button" class="btn btn-lg btn-success" on:click={saveScrambleRound}>
                        <i class="fa-solid fa-floppy-disk"></i> &nbsp;Save game
                    </button>
                    <button type="button" class="btn btn-lg btn-secondary"> Restart </button>
                </div>
            </div>
        </div>
    </div>
    <div class="col-12">
        <div class="card mt-3">
            <div class="card-body">
                <h4 class="card-title"><i class="fa-solid fa-star"></i> &nbsp;Recent Scores</h4>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Total</th>
                            <th>Score</th>
                            <th>Yards</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each recentRoundData as round}
                            <tr>
                                <td>{round.date.toLocaleDateString()}</td>
                                <td>{round.total}</td>
                                <td>{round.total > 36 ? '+' : ''}{round.total - 36}</td>
                                <td>{round.yards} yards</td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<style>
    .table {
        overflow-x: scroll;
    }
    .score-number {
        padding: 0px 5px;
    }
    .form-control-sm {
        border: none;
    }
    table {
        width: 100%;
        display: block;
    }
    td > input {
        width: 30px;
    }
</style>
