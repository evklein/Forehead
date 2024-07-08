<script lang="ts">
    export let imagePath: string;
    export let mode: string;
    export let description: string;
    export let link: string;
    export let badgeText: string | undefined = undefined;
</script>
<div class="col-4">
    <div class="card">
        <img class="card-img-top" src={imagePath} alt="Course">
        {#if badgeText}
            <span class="badge text-bg-success">{badgeText}</span>
        {/if}
        <div class="card-body">
            <h5 class="card-title">
                <span class="card-title-emphasize">{mode}</span>
            </h5>
            <p class="card-text">{description}</p>
            <a href={link} class="btn btn-success">Play <i class="fa-solid fa-play"></i></a>
        </div>
    </div>
</div>
<style>
    .badge {
        position: absolute;
        top: 10px;
        right: 10px;
    }
</style>