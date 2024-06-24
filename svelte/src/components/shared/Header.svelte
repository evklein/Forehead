<header>
    <div id="header">
            <a class="brand-link" href="/">
                <h1 id="brand">
                    <i class="brand-icon fa-solid fa-golf-ball-tee"></i> Bonk
                </h1>
            </a>
        <div class="header-links">
            <a href="/round">Enter Round</a>
            <a href="/courses">Courses</a>
        </div>
    </div>
</header>

<style>
    #header {
        padding: 10px;
        background: #21c24c;
        margin-bottom: 10px;
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    #brand {
        margin-left: 5%;
    }
    #brand > .brand-icon {
        margin-right: 5px;
    }
    a.brand-link {
        text-decoration: none;
    }
    h1 {
        margin: 0;
        color: white;
        font-size: 28px;
        transition: 0.3s;
        display: flex;
        align-items: center;
    }
    h1:hover {
        color: darkgreen;
        font-weight: bold;
        cursor: pointer;
    }
    .header-links {
        display: flex;
        margin-left: auto;
        width: 200px;
        justify-content: space-around;
    }
    .header-links > a {
        color: white;
        text-decoration: none;
        font-size: 12pt;
        transition: 0.3s;
    }
    .header-links> a:hover {
        font-weight: bold;
        color: darkgreen;
    }
</style>
