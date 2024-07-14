<script lang="ts">
    import { onMount } from 'svelte';
    import type { CourseData } from '../../models/CourseData';
    import type { RoundData } from '../../models/RoundData';
    import InProgressRoundCard from './InProgressRoundCard.svelte';
    import * as api from '../../services/api';

    export let rounds: RoundData[] = [];
    export let courses: CourseData[] = [];

    // Flag to indicate if data is loading
    let loading = true;

    onMount(async () => {
        try {
            rounds = (await api.fetchInProgressRounds()) ?? [];

            let uniqueCourseIds = [...new Set(rounds.map((r) => r.courseId))];
            let courseDataPromises = uniqueCourseIds.map((courseId) => api.fetchCourseDetails(courseId ?? -1));

            const fetchedCourses = await Promise.all(courseDataPromises);
            courses = fetchedCourses.filter((course) => course !== undefined) as CourseData[];
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            loading = false;
        }
    });

    function getCourseForRound(round: RoundData): CourseData | undefined {
        let selectedCourse = courses.find((c) => c.courseId === round.courseId);
        return selectedCourse;
    }
</script>

<div class="row align-items-start">
    <div class="col-12">
        <div class="btn-group">
            <a class="btn btn-success" href="/courses">
                <i class="fa fa-plus"></i> Start new round
            </a>
        </div>
    </div>
    <div class="col-12 mt-4">
        <h2>In-Progress Rounds</h2>
        {#if loading}
            <span class="loading">Loading...</span>
        {:else if rounds.length === 0}
            <span class="no-rounds">No in-progress rounds found.</span>
        {:else}
            {#each rounds as round}
                <InProgressRoundCard {round} course={getCourseForRound(round)} />
            {/each}
        {/if}
    </div>
</div>
