<script lang="ts">
    import { onMount } from 'svelte';
    import type { CourseData } from '../../models/CourseData';
    import CourseCard from '../../components/course/CourseCard.svelte';
    import * as api from '../../services/api';

    let courses: CourseData[] = [];

    onMount(async () => {
        courses = (await api.fetchAllCourses()) ?? [];
    });
</script>

<div class="row align-items-start">
    {#each courses as course}
        <CourseCard {course} />
    {/each}
</div>

<style></style>
