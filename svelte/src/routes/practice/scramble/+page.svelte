<script lang="ts">
    import { onMount } from "svelte";
    import type { ScrambleGameData } from "../../../models/ScrambleGameData";
    import * as api from "../../../services/api";

    let scrambleGameData: ScrambleGameData = {
        holeChips: Array(18).fill(0),
        holePutts: Array(18).fill(0),
        holeYardages: Array(18).fill(0)
    };

    $: holeScores = scrambleGameData.holeChips.map((_, i) => getHoleScore(i));
    $: holeBorders = holeScores.map((score) => getBorderForHoleScore(score));
    $: totalChips = scrambleGameData.holeChips.reduce((total, nextValue) => total + Number(nextValue), 0);
    $: totalPutts = scrambleGameData.holePutts.reduce((total, nextValue) => total + Number(nextValue), 0);
    $: totalYards = scrambleGameData.holeYardages.reduce((total, nextValue) => total + nextValue, 0);
    $: totalScore = totalChips + totalPutts;
    $: gameSavedStatus = "Game not saved";

    onMount(() => {
        console.log(scrambleGameData);
        let minYardage = 5;
        let maxYardage = 30;
        let newHoleYardages = [...scrambleGameData.holeYardages]; // Copy existing holeYardages

        for (let i = 0; i < 18; i += 3) {
            let nextMiddleYardage = Math.floor(Math.random() * (maxYardage - minYardage + 1)) + minYardage;
            newHoleYardages[i] = nextMiddleYardage - 1;
            newHoleYardages[i + 1] = nextMiddleYardage;
            newHoleYardages[i + 2] = nextMiddleYardage + 1;
        }
        
        scrambleGameData = { ...scrambleGameData, holeYardages: newHoleYardages };
    });

    function getHoleScore(holeNumber: number): number {
        return (Number(scrambleGameData.holeChips[holeNumber]) ?? 0) + (Number(scrambleGameData.holePutts[holeNumber]) ?? 0);
    }

    function getBorderForHoleScore(score: number): string {
        if (score === 1) return "border: 1px solid white; border-radius: 20px;";
        if (score === 2 || score === 0) return "";
        if (score === 3) return "border: 1px solid white;";
        return "border: 3px double white";
    }

    async function saveScrambleRound() {
        await api.savePracticeGame(scrambleGameData);
        gameSavedStatus = "Game Saved!";
    }
</script>

<div class="row align-items-start">
    <div class="col-12">
        <div class="card">
            <div class="card-body">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th scope="col"></th>
                            {#each {length: 18} as _, i}
                                <th scope="col">{i + 1}</th>
                            {/each}
                            <th scope="col">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Score</td>
                            {#each {length: 18} as _, i}
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
                            {#each {length: 18} as _, i}
                                <td>
                                    {scrambleGameData.holeYardages[i]}
                                </td>
                            {/each}
                            <td>
                                {totalYards}
                            </td>
                        </tr>
                        <tr>
                            <td>Chips</td>
                            {#each {length: 18} as _, i}
                                <td>
                                    <input class="form-control-sm" type="text" bind:value={scrambleGameData.holeChips[i]} />
                                </td>
                            {/each}
                            <td>{totalChips}</td>
                        </tr>
                        <tr>
                            <td>Putts</td>
                            {#each {length: 18} as _, i}
                                <td>
                                    <input class="form-control-sm" type="text" bind:value={scrambleGameData.holePutts[i]} />
                                </td>
                            {/each}
                            <td>{totalPutts}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="lower-buttons">
                <button type="button" class="btn btn-lg btn-primary" on:click={saveScrambleRound}>Save game</button>
                {gameSavedStatus}
            </div>
        </div>
    </div>
</div>

<style>
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
    .lower-buttons {
        display: flex;
        flex-direction: column;
        width: 300px;
        padding:0 20px;
    }
</style>
