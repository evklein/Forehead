<script lang="ts">
    export let numberOfSections: number = 6;
    export let numberOfSectionsCompleted: number = 3;
    export let label: string = 'Progress bar';
    export let smooth: boolean = false;
    export let color: string = '#0000ff';
</script>

<div class="progress-bar">
    <span class="label">{label}</span>
    {#each { length: numberOfSections } as _, index}
        {#if smooth}
            <span
                class="progress-bar-unit progress-bar-unit-smooth {index >= numberOfSectionsCompleted
                    ? 'incomplete-unit-smooth'
                    : null}"
                style="background: {index < numberOfSectionsCompleted ? color : 'transparent'}"
            ></span>
        {:else}
            <span
                class="progress-bar-unit {index < numberOfSectionsCompleted ? 'complete-unit' : 'incomplete-unit'}"
                style="background: {index < numberOfSectionsCompleted ? color : 'transparent'}"
            ></span>
        {/if}
    {/each}
</div>

<style>
    .progress-bar {
        display: inline-flex;
        flex-direction: row;
        align-items: center;
        margin: 10px 0;
    }

    .label {
        font-weight: bold;
        margin-right: 10px;
        min-width: 75px;
        max-width: 150px;
    }

    .progress-bar-unit {
        width: 70px;
        height: 18px;
        margin: 2px;
        border-radius: 5px;
    }

    .incomplete-unit {
        border: 1px solid black;
    }

    .incomplete-unit-smooth {
        border-top: 1px solid black;
        border-bottom: 1px solid black;
    }

    .progress-bar-unit-smooth {
        border-radius: 0;
        margin: 0;
        border-top: 1px solid black;
        border-bottom: 1px solid black;
    }

    .progress-bar-unit-smooth:nth-child(2) {
        border-top-left-radius: 5px;
        border-bottom-left-radius: 5px;
        border-left: 1px solid black;
    }

    .progress-bar-unit-smooth:last-child {
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
        border-right: 1px solid black;
    }
</style>
