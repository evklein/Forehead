<script lang="ts">
    import type { CourseData } from "../../models/CourseData";
    import type { RoundData } from "../../models/RoundData";

    export let round: RoundData;
    export let course: CourseData;

    function getRoundTitle(): string {
        return round.nickname ?? course.name;
    }
</script>
<div class="card">
    <div class="card-body">
        <div class="card-title">
            {getRoundTitle()}
        </div>
    </div>
</div>