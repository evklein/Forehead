<script lang="ts">
    import { onMount } from "svelte";
    import * as api from "../../../services/api";
    import RoundStart from "./RoundStart.svelte";
    import { RoundStage } from "../RoundStage";
    import Finalize from "./Finalize.svelte";
    import HoleEntry from "./HoleEntry.svelte";
    import type { HoleData } from "../../../models/HoleData";
    import type { HoleScoreData } from "../../../models/HoleScoreData";
    import type { RoundData } from "../../../models/RoundData";
    import type { TeeData } from "../../../models/TeeData";
    import type { StrokeData } from "../../../models/StrokeData";
    import type { PuttData } from "../../../models/PuttData";
    import { page } from "$app/stores";
    import type { CourseData } from "../../../models/CourseData";

    $: params = $page.params;
    $: courseId = Number(params.course_id);

    let entryStage: RoundStage = RoundStage.Start;

    let course: CourseData;
    let tees: TeeData[] = [];
    let holes: HoleData[] = [];

    let round: RoundData = {
        datePlayed: new Date(),
        mobility: "Walking",
    };
    let holeScores: HoleScoreData[] = [];
    let strokes: StrokeData[] = [];
    let putts: PuttData[] = [];

    onMount(async () => {
        // Get tees
        let courseDetails = await api.fetchCourseDetails(courseId);
        if (courseDetails) {
            course = courseDetails;
            round.holesCompleted = course.numberOfHoles;
        }
        tees = await api.fetchTees(1) ?? [];
        holes = await api.fetchHoles(1);

        if (course && course.numberOfHoles) {
            holeScores = Array.from({ length: course.numberOfHoles }, (_, index) => {
                return {
                    score: 0,
                    putts: 0,
                    greenInRegulation: false,
                    greenLightDrive: false,
                    scrambling: false,
                    roundId: 0,
                    holeId: 0,
                }
            }
            );
        }
        console.log('All data retrieved');
        console.log(course);
        console.log(tees);
        console.log(holes);
    });
</script>
{#if entryStage === RoundStage.Start}
    <RoundStart
        courseName={course?.name}
        bind:round {tees} 
        handleAdvance={() => entryStage = RoundStage.HoleEntry} />
{:else if entryStage === RoundStage.HoleEntry}
    <HoleEntry courseName={course.name}
        maximumNumberOfHoles={course.numberOfHoles}
        {holes}
        {holeScores}
        handleAdvance={() => entryStage = RoundStage.Finalize} />
{:else if entryStage === RoundStage.Finalize}
    <Finalize />
{/if}
<style>
</style>