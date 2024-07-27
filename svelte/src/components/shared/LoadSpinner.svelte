<script lang="ts">
    export let sizePx: number = 24;
    export let message: string = 'Loading...';
</script>

<span class="loader">
    <i style="font-size: {sizePx}px" class="fas fa-spinner fa-spin"></i>
    <span class="message">&nbsp;&nbsp;{message}</span>
</span>

<style>
    .loader {
        vertical-align: middle;
    }

    .message {
        vertical-align: top;
    }
</style>
