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

    function getCumulativeScoreForHoles(start: number, end: number) {
        return holes
            .slice(start, end)
            .reduce((total, nextHole) => total + getCumulativeStrokeForHole(nextHole.holeNumber), 0);
    }

    function getCumulativePuttsForHoles(start: number, end: number) {
        return holes
            .slice(start, end)
            .reduce((total, nextHole) => total + getCumultativePuttsForHole(nextHole.holeNumber), 0);
    }

    function getCumulativeGIRForHoles(start: number, end: number) {
        return holes
            .slice(start, end)
            .reduce((total, nextHole) => total + (getStatsForHole(nextHole.holeNumber)?.greenInRegulation ? 1 : 0), 0);
    }

    function getCumulativeGLDForHoles(start: number, end: number) {
        let numberOfParThrees = holes
            .slice(start, end)
            .reduce((total, nextHole) => total + (nextHole.par === 3 ? 1 : 0), 0);
        let numberOfGLD = holes
            .slice(start, end)
            .reduce((total, nextHole) => total + (getStatsForHole(nextHole.holeNumber)?.greenLightDrive ? 1 : 0), 0);
        return `${numberOfGLD}/${end - start - numberOfParThrees}`;
    }

    function getCumulativeScramblingForHoles(start: number, end: number) {
        let numberOfMissedGreens = end - start - getCumulativeGIRForHoles(start, end);
        let scrambles = holes
            .slice(start, end)
            .reduce((total, nextHole) => total + (getStatsForHole(nextHole.holeNumber)?.scrambling ? 1 : 0), 0);
        return `${scrambles}/${numberOfMissedGreens}`;
    }

    function getCumulativeParForHoles(start: number, end: number) {
        return holes.slice(start, end).reduce((total, nextHole) => total + nextHole.par, 0);
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
                                {#each holes as hole, index}
                                    <th scope="col">{hole.holeNumber}</th>
                                    {#if index === 8}
                                        <th scope="col">Front</th>
                                    {/if}
                                {/each}
                                <th scope="col">Back</th>
                                <th scope="col">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Score</td>
                                {#each holes as hole, index}
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
                                    {#if index === 8}
                                        <td>{getCumulativeScoreForHoles(0, 9)}</td>
                                    {/if}
                                {/each}
                                <td>{getCumulativeScoreForHoles(9, 18)}</td>
                                <td>
                                    <b>
                                        {getCumulativeScoreForHoles(0, 18)}
                                    </b>
                                </td>
                            </tr>
                            <tr>
                                <td>Putts</td>
                                {#each holes as hole, index}
                                    <td>{getCumultativePuttsForHole(hole.holeNumber)}</td>
                                    {#if index === 8}
                                        <td>{getCumulativePuttsForHoles(0, 9)}</td>
                                    {/if}
                                {/each}
                                <td>{getCumulativePuttsForHoles(9, 18)}</td>
                                <td>
                                    <b>
                                        {getCumulativePuttsForHoles(0, 18)}
                                    </b>
                                </td>
                            </tr>
                            <tr>
                                <td>GIR</td>
                                {#each holes as hole, index}
                                    <td>
                                        <input
                                            type="checkbox"
                                            class="form-check-input"
                                            checked={getStatsForHole(hole.holeNumber)?.greenInRegulation}
                                            disabled
                                        />
                                    </td>
                                    {#if index === 8}
                                        <td>{getCumulativeGIRForHoles(0, 9)}/9</td>
                                    {/if}
                                {/each}
                                <td>{getCumulativeGIRForHoles(9, 18)}/9</td>
                                <td>
                                    <b>{getCumulativeGIRForHoles(0, 18)}/{round.holesCompleted}</b>
                                </td>
                            </tr>
                            <tr>
                                <td>GLD</td>
                                {#each holes as hole, index}
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
                                    </td>
                                    {#if index === 8}
                                        <td>{getCumulativeGLDForHoles(0, 9)}</td>
                                    {/if}
                                {/each}
                                <td>{getCumulativeGLDForHoles(9, 18)}</td>
                                <td>
                                    <b>{getCumulativeGLDForHoles(0, 18)}</b>
                                </td>
                            </tr>
                            <tr>
                                <td>SCR</td>
                                {#each holes as hole, index}
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
                                    {#if index === 8}
                                        <td>{getCumulativeScramblingForHoles(0, 9)}</td>
                                    {/if}
                                {/each}
                                <td>{getCumulativeScramblingForHoles(9, 18)}</td>
                                <td>
                                    <b>{getCumulativeScramblingForHoles(0, 18)}</b>
                                </td>
                            </tr>
                            <tr>
                                <td>Par</td>
                                {#each holes as hole, index}
                                    <td>{hole.par}</td>
                                    {#if index === 8}
                                        <td>{getCumulativeParForHoles(0, 9)}</td>
                                    {/if}
                                {/each}
                                <td>{getCumulativeParForHoles(9, 18)}</td>
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
