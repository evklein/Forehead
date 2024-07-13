<script lang="ts">
    export let imagePath: string;
    export let mode: string;
    export let description: string;
    export let link: string;
    export let badgeText: string | undefined = undefined;
</script>

<div class="col-xs-12 col-lg-4">
    <a href={link}>
        <div class="card">
            <img class="card-img-top" src={imagePath} alt="Course" />
            {#if badgeText}
                <span class="badge text-bg-success">{badgeText}</span>
            {/if}
            <div class="card-body">
                <h5 class="card-title">
                    <span class="card-title-emphasize">{mode}</span>
                </h5>
                <p class="card-text">{description}</p>
            </div>
        </div>
    </a>
</div>

<style>
    .badge {
        position: absolute;
        top: 10px;
        right: 10px;
    }

    a {
        text-decoration: none;
    }

    .card {
        z-index: 1;
        width: 100%;
        margin: 10px 0;
        transition: width 0.2s ease; /* Smooth transition for width change */
    }

    .card:hover {
        width: 105%;
        z-index: 10;
    }
</style>
