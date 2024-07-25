<script lang="ts">
    import { onMount } from 'svelte';
    import * as api from '../../../../services/api';
    import { page } from '$app/stores';
    import { RoundStage } from '../../RoundStage';
    import type { CourseData } from '../../../../models/CourseData';
    import type { TeeData } from '../../../../models/TeeData';
    import type { RoundData } from '../../../../models/RoundData';
    import type { HoleData } from '../../../../models/HoleData';
    import type { HoleScore } from '../../../../models/HoleScore';
    import type { HoleStatsData } from '../../../../models/HoleStatsData';
    import type { StrokeData } from '../../../../models/StrokeData';
    import type { PuttData } from '../../../../models/PuttData';
    import RoundStart from '../../[course_id]/RoundStart.svelte';
    import HoleEntry from '../../[course_id]/HoleEntry.svelte';
    import Finalize from '../../[course_id]/Finalize.svelte';

    $: params = $page.params;
    $: roundId = Number(params.round_id);

    let entryStage: RoundStage = RoundStage.Start;

    let round: RoundData | undefined = undefined;
    let course: CourseData;
    let tees: TeeData[] = [];
    let holes: HoleData[] = [];

    let holeScores: HoleScore[] = [];

    let roundStats: HoleStatsData[];
    let roundStrokes: StrokeData[];
    let roundPutts: PuttData[];

    onMount(async () => {
        round = (await api.fetchRoundDetails(roundId)) ?? undefined;
        if (round) {
            let roundStats = await api.fetchRoundHoleStats(roundId);
            let roundStrokes = await api.fetchRoundStrokes(roundId);
            let roundPutts = await api.fetchRoundPutts(roundId);
            let courseDetails = await api.fetchCourseDetails(round.courseId ?? -1);
            if (courseDetails) {
                course = courseDetails;
                round.holesCompleted = course.numberOfHoles;
            }
            tees = (await api.fetchTees(course.courseId)) ?? [];
            holes = await api.fetchHoles(course.courseId);

            if (course && course.numberOfHoles && roundStats && roundStrokes && roundPutts) {
                let holeOffset = holes[0].id ?? 0;
                console.log('HOLE OFFSET: ' + holeOffset);
                for (let i = 0; i < course.numberOfHoles; i++) {
                    holeScores = [
                        ...holeScores,
                        {
                            stats: roundStats.filter((s) => s.holeNumber - holeOffset === i)[0] ?? {
                                greenInRegulation: false,
                                greenLightDrive: false,
                            },
                            fullShots: roundStrokes.filter((s) => s.holeNumber - holeOffset === i),
                            putts: roundPutts.filter((s) => s.holeNumber - holeOffset === i),
                        },
                    ];
                }
            }
        }
    });

    async function advanceToFinalizePage() {
        if (round && round.id) {
            roundStats = (await api.getHoleStatsForRound(round.id)) ?? [];
            roundStrokes = (await api.getStrokesForRound(round.id)) ?? [];
            roundPutts = (await api.getPuttsForRound(round.id)) ?? [];
        }

        entryStage = RoundStage.Finalize;
    }
</script>

{#if round}
    {#if entryStage === RoundStage.Start}
        <RoundStart
            continuing={true}
            {course}
            bind:round
            {tees}
            handleAdvance={() => (entryStage = RoundStage.HoleEntry)}
            handleAdvanceToFinal={advanceToFinalizePage}
        />
    {:else if entryStage === RoundStage.HoleEntry}
        <HoleEntry {round} {course} {holes} {holeScores} handleAdvance={advanceToFinalizePage} courseTees={tees} />
    {:else if entryStage === RoundStage.Finalize}
        <Finalize {course} {round} {holes} stats={roundStats} strokes={roundStrokes} putts={roundPutts} />
    {/if}
{/if}
