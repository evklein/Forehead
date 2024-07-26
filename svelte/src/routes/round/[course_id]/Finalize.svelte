<script lang="ts">
    import type { CourseData } from '../../../models/CourseData';
    import type { HoleData } from '../../../models/HoleData';
    import type { HoleStatsData } from '../../../models/HoleStatsData';
    import type { RoundData } from '../../../models/RoundData';
    import type { StrokeData } from '../../../models/StrokeData';
    import * as scoreCardUtils from '../../../services/scoreCardUtilities';

    export let course: CourseData;
    export let round: RoundData;
    export let holes: HoleData[];
    export let stats: HoleStatsData[];
    export let strokes: StrokeData[];
    export let putts: StrokeData[];

    $: getCumulativeStrokeForHole = (holeNumber: number) => {
        console.log(strokes);
        let holeOffset = holes[0].id ?? 0;
        return (
            strokes?.filter((s) => s.holeNumber - holeOffset === holeNumber - 1).length +
            getCumultativePuttsForHole(holeNumber)
        );
    };

    function getCumultativePuttsForHole(holeNumber: number): number {
        let holeOffset = holes[0].id ?? 0;
        return putts?.filter((p) => p.holeNumber - holeOffset === holeNumber - 1).length;
    }

    function getStatsForHole(holeNumber: number): HoleStatsData | undefined {
        let holeOffset = holes[0].id ?? 0;
        return stats?.find((s) => s.holeNumber - holeOffset === holeNumber - 1);
    }

    function getFinalScore() {
        return holes.reduce((total, nextHole) => total + getCumulativeStrokeForHole(nextHole.holeNumber), 0);
    }

    function getTotalGir() {
        let totalGir = holes.reduce(
            (total, nextHole) => total + (getStatsForHole(nextHole.holeNumber)?.greenInRegulation ? 1 : 0),
            0,
        );
        return totalGir;
    }

    function getTotalGld() {
        let totalGld = holes.reduce(
            (total, nextHole) => total + (getStatsForHole(nextHole.holeNumber)?.greenLightDrive ? 1 : 0),
            0,
        );
        let numberOfParThrees = holes.reduce((total, nextHole) => total + (nextHole.par === 3 ? 1 : 0), 0);
        return `${totalGld}/${round.holesCompleted - numberOfParThrees}`;
    }

    function getTotalScrambling() {
        let totalGir = getTotalGir();
        let totalScrambling = holes.reduce(
            (total, nextHole) => total + (getStatsForHole(nextHole.holeNumber)?.scrambling ? 1 : 0),
            0,
        );
        return `${totalScrambling}/${round.holesCompleted - totalGir}`;
    }

    function getTotalPutts() {
        return holes.reduce((total, nextHole) => total + getCumultativePuttsForHole(nextHole.holeNumber), 0);
    }
</script>

<div class="row align-items-start">
    <div class="col-12">
        <div class="card">
            <div class="card-body">
                {#if round && round.holesCompleted}
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th scope="col"></th>
                                {#each holes as hole}
                                    <th scope="col">{hole.holeNumber}</th>
                                {/each}
                                <th scope="col">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Score</td>
                                {#each holes as hole}
                                    <td>
                                        <span
                                            class="score-number"
                                            style={scoreCardUtils.getScoreElementBorder(
                                                getCumulativeStrokeForHole(hole.holeNumber),
                                                hole.par,
                                            )}
                                        >
                                            {getCumulativeStrokeForHole(hole.holeNumber)}
                                        </span>
                                    </td>
                                {/each}
                                <td>
                                    <b>
                                        {getFinalScore()}
                                    </b>
                                </td>
                            </tr>
                            <tr>
                                <td>Putts</td>
                                {#each holes as hole}
                                    <td>{getCumultativePuttsForHole(hole.holeNumber)}</td>
                                {/each}
                                <td>
                                    <b>
                                        {getTotalPutts()}
                                    </b>
                                </td>
                            </tr>
                            <tr>
                                <td>GIR</td>
                                {#each holes as hole}
                                    <td>
                                        <input
                                            type="checkbox"
                                            class="form-check-input"
                                            checked={getStatsForHole(hole.holeNumber)?.greenInRegulation}
                                            disabled
                                        />
                                    </td>
                                {/each}
                                <td>
                                    <b>{getTotalGir()}/{round.holesCompleted}</b>
                                </td>
                            </tr>
                            <tr>
                                <td>GLD</td>
                                {#each holes as hole}
                                    <td>
                                        {#if hole.par > 3}
                                            <input
                                                type="checkbox"
                                                class="form-check-input"
                                                checked={getStatsForHole(hole.holeNumber)?.greenLightDrive}
                                                disabled
                                            />
                                        {:else}
                                            <span>-</span>
                                        {/if}
                                    </td>{/each}
                                <td>
                                    <b>{getTotalGld()}</b>
                                </td>
                            </tr>
                            <tr>
                                <td>SCR</td>
                                {#each holes as hole}
                                    {#if !getStatsForHole(hole.holeNumber)?.greenInRegulation}
                                        <td>
                                            <input
                                                type="checkbox"
                                                class="form-check-input"
                                                checked={getStatsForHole(hole.holeNumber)?.scrambling}
                                                disabled
                                            />
                                        </td>
                                    {:else}
                                        <td><span>-</span></td>
                                    {/if}
                                {/each}
                                <td>
                                    <b>{getTotalScrambling()}</b>
                                </td>
                            </tr>
                            <tr>
                                <td>Par</td>
                                {#each holes as hole}
                                    <td>{hole.par}</td>
                                {/each}
                                <td>
                                    <b>
                                        {course.par}
                                    </b>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    .score-number {
        padding: 0 5px;
    }

    td {
        text-align: center;
    }
</style>
