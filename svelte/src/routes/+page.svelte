<script>
</script>

<svelte:head>
    <title>Forehead</title>
    <meta name="description" content="Forehead" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
</svelte:head>

<div>
    <div class="row align-items-start">
        <h3>
            <span class="welcome">
                <p>
                    Welcome to <b class="forehead">Forehead</b>, an open Golf analytics solution.
                </p>
            </span>
        </h3>
    </div>
    <div class="row align-items-start">
        <div class="col-xs-12 col-lg-4">
            <a href="/rounds">
                <div class="card">
                    <img
                        class="card-img-top"
                        src="https://www.thebreakfastball.com/wp-content/uploads/2017/09/2017-93-Crooked-Stick-GC-hole-6.jpg"
                        alt="Course"
                    />
                    <div class="card-body">
                        <h5 class="card-title">Play</h5>
                        <p class="card-text">Play a round of golf. Record the data for analytics.</p>
                    </div>
                </div>
            </a>
        </div>
        <div class="col-xs-12 col-lg-4">
            <a href="/practice">
                <div class="card">
                    <img
                        class="card-img-top"
                        src="https://media.istockphoto.com/id/489515598/photo/female-golfer-practicing-on-a-driving-range.jpg?s=612x612&w=0&k=20&c=uAtg7QQhw_DfNvrO9updTuJcVsmy0c6sfRpKRWKKX80="
                        alt="Course"
                    />
                    <div class="card-body">
                        <h5 class="card-title">Practice</h5>
                        <p class="card-text">Practice different parts of the game.</p>
                    </div>
                </div>
            </a>
        </div>
    </div>
</div>

<style>
    section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        flex: 0.6;
    }

    .forehead {
        color: green;
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
