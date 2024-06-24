<script>
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Bonk" />
</svelte:head>

<section>
	<h3>
		<span class="welcome">
			<p>Welcome to <b class="bonk">Bonk</b>, an open Golf analytics solution.</p>
		</span>
	</h3>
    <div class="links">
        <a href="/courses">View Courses</a>
    </div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	.welcome {
		display: block;
		width: 100%;
		height: 0;
		padding: 0;
        text-align: center;
	}

    .bonk {
        color: green;
    }

    .links {
        position: relative;
        top: 50px;
    }
</style>
