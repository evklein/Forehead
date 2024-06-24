<script lang="ts">
    import { onMount } from 'svelte';
    import type { CourseData } from '../../models/CourseData';
    import CourseCard from '../../components/course/CourseCard.svelte';

    let courses: CourseData[] = [];

    onMount(async () => {
        await fetchAllCourses();
    });

    async function fetchAllCourses() {
		const res = await fetch(`http://127.0.0.1:8000/course/all`)
            .then(response => response.json())
            .then(data => {
                data.forEach((rawCourseData: any) => {
                    courses = [...courses, {
                        courseId: rawCourseData['pk'],
                        public: rawCourseData['fields']['public'],
                        par: rawCourseData['fields']['par'],
                        address: rawCourseData['fields']['address'],
                        name: rawCourseData['fields']['name'],
                        designer: rawCourseData['fields']['designer'],
                        imageUrl: rawCourseData['fields']['image_url'],
                    }];
                });
            });
    }
</script>
<div class="row align-items-start">
    {#each courses as course}
        <CourseCard {course} />
    {/each}
</div>
<style></style>