<script lang="ts">
    import { onMount } from "svelte";
    import * as api from "../../../services/api";
    import RoundStart from "./RoundStart.svelte";
    import { RoundStage } from "../RoundStage";
    import Finalize from "./Finalize.svelte";
    import HoleEntry from "./HoleEntry.svelte";
    import type { HoleData } from "../../../models/HoleData";
    import type { RoundData } from "../../../models/RoundData";
    import type { TeeData } from "../../../models/TeeData";
    import { page } from "$app/stores";
    import type { CourseData } from "../../../models/CourseData";
    import type { HoleScore } from "../../../models/HoleScore";
    import type { HoleStatsData } from "../../../models/HoleStatsData";
    import type { PuttData } from "../../../models/PuttData";
    import type { StrokeData } from "../../../models/StrokeData";

    $: params = $page.params;
    $: courseId = Number(params.course_id);

    let entryStage: RoundStage = RoundStage.Start;

    let course: CourseData;
    let tees: TeeData[] = [];
    let holes: HoleData[] = [];

    let round: RoundData = {
        datePlayed: new Date(),
        mobility: "Walking",
        roundCountsTowardHci: false,
        holesCompleted: 0,
    };

    let holeScores: HoleScore[];

    let roundStats: HoleStatsData[];
    let roundStrokes: StrokeData[];
    let roundPutts: PuttData[];

    onMount(async () => {
        let courseDetails = await api.fetchCourseDetails(courseId);
        if (courseDetails) {
            course = courseDetails;
            round.holesCompleted = course.numberOfHoles;
        }
        tees = await api.fetchTees(course.courseId) ?? [];
        holes = await api.fetchHoles(course.courseId);

        if (course && course.numberOfHoles) {
            holeScores = Array.from({ length: course.numberOfHoles }, (_, index) => {
                return {
                    numberOfStrokes: 0,
                    numberOfPutts: 0,
                    stats: {
                        greenInRegulation: false,
                        greenLightDrive: false,
                    },
                    strokes: [],
                    putts: []
                }
            });
        }
    });

    async function advanceToFinalizePage() {
        if (round.id) {
            roundStats = await api.getHoleStatsForRound(round.id) ?? [];
            roundStrokes = await api.getStrokesForRound(round.id) ?? [];
            roundPutts = await api.getPuttsForRound(round.id) ?? [];
        }

        entryStage = RoundStage.Finalize;
    }
</script>
{#if entryStage === RoundStage.Start}
    <RoundStart
        {course}
        bind:round
        {tees} 
        handleAdvance={() => entryStage = RoundStage.HoleEntry} />
{:else if entryStage === RoundStage.HoleEntry}
    <HoleEntry
        {round}
        {course}
        {holes}
        {holeScores}
        handleAdvance={advanceToFinalizePage} />
{:else if entryStage === RoundStage.Finalize}
    <Finalize
        {course}
        {round}
        {holes}
        stats={roundStats}
        strokes={roundStrokes}
        putts={roundPutts}
    />
{/if}
<style>
</style>