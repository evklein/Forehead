<script lang="ts">
    import type { CourseData } from '../../models/CourseData';
    import type { RoundData } from '../../models/RoundData';

    export let round: RoundData;
    export let course: CourseData | undefined = undefined;
</script>

<div class="card flex-row">
    <img
        class="card-img-left example-card-img-responsive"
        src={course?.imageUrl}
    />
    <div class="card-body">
        <h4 class="card-title h5 h4-sm">
            {round.datePlayed} at <b>{course?.name}</b>
        </h4>
        <a class="btn btn-success" href="/round/continue/{round.id}">
            Continue &nbsp;<i class="fa-solid fa-arrow-right"></i>
        </a>
    </div>
</div>

<style>
    .card {
        margin: 20px;
    }
    img {
        max-width: 200px;
    }
</style>
