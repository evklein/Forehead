<script>
    import Header from '../components/shared/Header.svelte';
    import './styles.css';
</script>

<svelte:head>
    <meta name="apple-mobile-web-app-capable" content="yes" />
</svelte:head>

<div class="app">
    <Header />

    <main>
        <slot />
    </main>
</div>

<style>
    .app {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    main {
        flex: 1;
        display: flex;
        flex-direction: column;
        padding: 1rem;
        width: 100%;
        max-width: 95rem;
        margin: 0 auto;
        box-sizing: border-box;
    }
</style>
