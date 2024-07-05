<script lang="ts">
    import { onMount } from "svelte";
    import Map from "../../../../components/shared/Map.svelte";
    import { page } from '$app/stores';
    import type { CourseData } from "../../../../models/CourseData";
    import * as api from "../../../../services/api";
    import type { HoleData } from "../../../../models/HoleData";
    import HoleFormCard from "./HoleFormCard.svelte";

    $: params = $page.params;
    $: courseId = Number(params.course_id);
    $: holeNumber = Number(params.hole);

    let course: CourseData = {
        courseId: -1,
        name: '',
        numberOfHoles: 0,
        par: 0,
        public: false,
        designer: '',
        address: '',
        imageUrl: '',
        boundPoints: [],
    };
    let hole: HoleData = {
        holeNumber: holeNumber,
        par: 0,
        boundPoints: [],
    };
    let initialBoundPointCount: number = 0;
    let mapCanBeLoaded: boolean = false;

    onMount(async () => {
        let holeDetails = await api.fetchHoleDetails(courseId, holeNumber);
        if (holeDetails) {
            hole = holeDetails;
            initialBoundPointCount = hole.boundPoints.length;
        }

        let courseDetails = await api.fetchCourseDetails(courseId);
        if (courseDetails) {
            course = courseDetails;
        }

        mapCanBeLoaded = true;
    });
</script>
<div class="row align-items-start">
    <div class="col-7">
    {#if mapCanBeLoaded}
        {#if initialBoundPointCount === 0}
            <Map bind:focusBounds={course.boundPoints} bind:selectedBounds={hole.boundPoints} highlightSelectedbounds={false} />
        {:else}
            <Map bind:focusBounds={hole.boundPoints} bind:selectedBounds={hole.boundPoints} highlightSelectedbounds={true} specialPoints={hole.centerGreenPoint ? [hole.centerGreenPoint] : []} />
        {/if}
    {/if}
    </div>
    <div class="col-5">
        <HoleFormCard {courseId} {holeNumber} courseName={course.name} bind:hole saveHole={async() => await api.saveHole(courseId, hole)} />
    </div>
</div>
