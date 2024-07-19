<script lang="ts">
    import { onMount } from 'svelte';
    import Map from '../../../../components/shared/Map.svelte';
    import { page } from '$app/stores';
    import type { CourseData } from '../../../../models/CourseData';
    import * as api from '../../../../services/api';
    import type { HoleData } from '../../../../models/HoleData';
    import HoleFormCard from './HoleFormCard.svelte';
    import { goto } from '$app/navigation';

    $: params = $page.params;
    $: courseId = Number(params.course_id);
    $: markers = hole.boundPoints.map((point) => {
        return {
            coordinates: point,
        };
    });

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
        holeNumber: 1,
        par: 0,
        boundPoints: [],
    };
    let initialBoundPointCount: number = 0;
    let mapCanBeLoaded: boolean = false;

    onMount(async () => {
        let holeDetails = await api.fetchHoleDetails(courseId, 1);
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

    function selectPoints(coordinates: [number, number]) {
        console.log('Setting point');
        hole.boundPoints = [...hole.boundPoints, coordinates];
    }

    async function goToNextHole() {
        let holeDetails = await api.fetchHoleDetails(courseId, hole.holeNumber + 1);
        if (holeDetails) {
            hole = holeDetails;
            initialBoundPointCount = hole.boundPoints.length;
        }
    }

    async function goToPreviousHole() {
        let holeDetails = await api.fetchHoleDetails(courseId, hole.holeNumber - 1);
        if (holeDetails) {
            hole = holeDetails;
            initialBoundPointCount = hole.boundPoints.length;
        }
    }
</script>

<div class="row align-items-start">
    <div class="col-7">
        {#if mapCanBeLoaded}
            {#if initialBoundPointCount === 0}
                <Map
                    bind:focusBounds={course.boundPoints}
                    {markers}
                    handleSelectPointOnMap={selectPoints}
                    highlightSelectedbounds={false}
                />
            {:else}
                <Map bind:focusBounds={hole.boundPoints} {markers} highlightSelectedbounds={true} />
            {/if}
        {/if}
    </div>
    <div class="col-5">
        <HoleFormCard
            {courseId}
            holeNumber={hole.holeNumber}
            courseName={course.name}
            bind:hole
            saveHole={async () => await api.saveHole(courseId, hole)}
            handleGoToNextHole={goToNextHole}
            handleGoToPreviousHole={goToPreviousHole}
        />
    </div>
</div>
