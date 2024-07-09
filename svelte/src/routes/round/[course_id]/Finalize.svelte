<script lang="ts">
    import type { CourseData } from '../../../models/CourseData';
    import type { HoleData } from '../../../models/HoleData';
    import type { HoleStatsData } from '../../../models/HoleStatsData';
    import type { RoundData } from '../../../models/RoundData';
    import type { StrokeData } from '../../../models/StrokeData';

    export let course: CourseData;
    export let round: RoundData;
    export let holes: HoleData[];
    export let stats: HoleStatsData[];
    export let strokes: StrokeData[];
    export let putts: StrokeData[];

    function getCumulativeStrokeForHole(holeNumber: number): number {
        console.log(strokes);
        return (
            strokes.filter((s) => s.holeNumber === holeNumber).length +
            getCumultativePuttsForHole(holeNumber)
        );
    }

    function getCumultativePuttsForHole(holeNumber: number): number {
        return putts.filter((p) => p.holeNumber === holeNumber).length;
    }

    function getStatsForHole(holeNumber: number): HoleStatsData | undefined {
        return stats.find((s) => s.holeNumber === holeNumber);
    }

    function getBorderForHoleScore(hole: HoleData): string {
        let score = getCumulativeStrokeForHole(hole.holeNumber);
        let par = hole.par;

        if (score <= par - 2)
            return 'border: 3px double white; border-radius: 20px;';
        if (score === par - 1)
            return 'border: 2px solid white; border-radius: 20px;';
        if (score === par) return '';
        if (score === par + 1) return 'border: 1px solid white';
        return 'border: 3px double white';
    }

    function getFinalScore() {
        return holes.reduce(
            (total, nextHole) =>
                total + getCumulativeStrokeForHole(nextHole.holeNumber),
            0,
        );
    }

    function getTotalGir() {
        let totalGir = holes.reduce(
            (total, nextHole) =>
                total +
                (getStatsForHole(nextHole.holeNumber)?.greenInRegulation
                    ? 1
                    : 0),
            0,
        );
        return totalGir;
    }

    function getTotalGld() {
        let totalGld = holes.reduce(
            (total, nextHole) =>
                total +
                (getStatsForHole(nextHole.holeNumber)?.greenLightDrive ? 1 : 0),
            0,
        );
        let numberOfParThrees = holes.reduce(
            (total, nextHole) => total + (nextHole.par === 3 ? 1 : 0),
            0,
        );
        return `${totalGld}/${round.holesCompleted - numberOfParThrees}`;
    }

    function getTotalScrambling() {
        let totalGir = getTotalGir();
        let totalScrambling = holes.reduce(
            (total, nextHole) =>
                total +
                (getStatsForHole(nextHole.holeNumber)?.scrambling ? 1 : 0),
            0,
        );
        return `${totalScrambling}/${round.holesCompleted - totalGir}`;
    }

    function getTotalPutts() {
        return holes.reduce(
            (total, nextHole) =>
                total + getCumultativePuttsForHole(nextHole.holeNumber),
            0,
        );
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
                                            style={getBorderForHoleScore(hole)}
                                        >
                                            {getCumulativeStrokeForHole(
                                                hole.holeNumber,
                                            )}
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
                                    <td
                                        >{getCumultativePuttsForHole(
                                            hole.holeNumber,
                                        )}</td
                                    >
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
                                            checked={getStatsForHole(
                                                hole.holeNumber,
                                            )?.greenInRegulation}
                                            disabled
                                        />
                                    </td>
                                {/each}
                                <td>
                                    <b>{getTotalGir()}/{round.holesCompleted}</b
                                    >
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
                                                checked={getStatsForHole(
                                                    hole.holeNumber,
                                                )?.greenLightDrive}
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
                                                checked={getStatsForHole(
                                                    hole.holeNumber,
                                                )?.scrambling}
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
