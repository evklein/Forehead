<script lang="ts">
    import { onMount } from "svelte";
    import Map from "../../../components/shared/Map.svelte";
    import { page } from '$app/stores';
    import type { CourseData } from "../../../models/CourseData";
    import CourseFormCard from "./CourseFormCard.svelte";
    import * as api from "../../../services/api";
    import type { HoleData } from "../../../models/HoleData";

    $: params = $page.params;
    $: id = Number(params.course_id);

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
    }
    let currentlySelectedHoleNumber: number = 1;
    let selectedHole: HoleData = {
        holeNumber: -1,
        par: 0,
        boundPoints: [],
    };
    let tees: TeeData[] = [];

    onMount(async () => {
        let courseDetails = await api.fetchCourseDetails(id);
        if (courseDetails) {
            course = courseDetails;
        }

        let teeDetails = await api.fetchTees(id);
        if (teeDetails) {
            tees = teeDetails;
            tees.sort((a, b) => a.yardage - b.yardage);
        }
        
        await fetchCurrentlySelectedHoleDetails();
    });

    async function selectNextHole() {
        if (currentlySelectedHoleNumber < course.numberOfHoles) {
            currentlySelectedHoleNumber++
            await fetchCurrentlySelectedHoleDetails();
        };
    }

    async function selectPreviousHole() {
        if (currentlySelectedHoleNumber > 0) { 
            currentlySelectedHoleNumber--;
            await fetchCurrentlySelectedHoleDetails();
        }
    }

    async function fetchCurrentlySelectedHoleDetails() {
        let nextHoleDetails = await api.fetchHoleDetails(id, currentlySelectedHoleNumber);
        if (nextHoleDetails) {
            selectedHole = nextHoleDetails;
        }
    }
</script>
<div class="row align-items-start">
    <div class="col-8">
        <div class="map-wrapper">
            <Map focusBounds={course.boundPoints} bind:selectedBounds={course.boundPoints} highlightSelectedbounds={true} />
        </div>
    </div>
    <div class="col-4">
        <CourseFormCard bind:course saveCourse={async () => await api.saveCourse(id, course)} {tees} />
        <div class="card">
            <div class="card-body">
                <h5 class="hole-card-title card-title">
                    Hole {currentlySelectedHoleNumber}
                    <span class="par-badge badge text-bg-success ml-2">Par {selectedHole.par}</span>
                    <div class="next-and-prev">
                        <div class="btn-group mr-2" role="group" aria-label="First group">
                            {#if currentlySelectedHoleNumber > 1}
                                <btn rel="external" class="btn btn-secondary" on:click={selectPreviousHole}><i class="fa-solid fa-arrow-left"></i></btn>
                            {/if}
                            {#if currentlySelectedHoleNumber < course.numberOfHoles}
                                <btn class="btn btn-secondary" on:click={selectNextHole}><i class="fa-solid fa-arrow-right"></i></btn>
                            {/if}
                        </div>
                    </div>
                </h5>
                <div class="card-buttons">
                    <a href="/courses/{id}/{currentlySelectedHoleNumber}"
                        class="btn btn-primary">
                        <i class="fa-solid fa-edit"></i> Edit Hole
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
<style>
    .map-wrapper {
        margin: 10px;
    }

    .hole-card-title {
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    .next-and-prev {
        margin-left: auto;
    }
    .par-badge {
        margin-left: 10px;
        font-size: 10pt;
    }
</style>
