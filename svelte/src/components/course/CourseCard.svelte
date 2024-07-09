<script lang="ts">
    import type { CourseData } from '../../models/CourseData';

    export let course: CourseData;
</script>

<div class="col-4">
    <div class="card">
        <img class="card-img-top" src={course.imageUrl} alt="Course" />
        <span
            class="public-badge badge text-bg-{course.public
                ? 'success'
                : 'danger'}">{course.public ? `Public` : `Private`}</span
        >
        <span class="par-badge badge text-bg-success">Par {course.par}</span>
        <div class="card-body">
            <h5 class="card-title">
                <span class="card-title-emphasize">{course.name}</span>
            </h5>
            <p class="card-text">{course.address}</p>
            <a href={`/courses/${course.courseId}`} class="btn btn-primary"
                >Edit Details <i class="fa-solid fa-pencil"></i></a
            >
            <a href="/round/{course.courseId}" class="btn btn-success"
                >Start Round <i class="fa-solid fa-arrow-right"></i></a
            >
        </div>
    </div>
</div>

<style>
    .badge {
        position: absolute;
        top: 10px;
    }
    .public-badge {
        left: 10px;
    }
    .par-badge {
        right: 10px;
    }
</style>
