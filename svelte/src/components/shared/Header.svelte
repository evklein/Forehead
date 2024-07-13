<header>
    <div id="header">
        <a class="brand-link" href="/">
            <h1 id="brand">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="45"
                    height="45"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="lucide lucide-land-plot"
                    ><path d="m12 8 6-3-6-3v10" /><path
                        d="m8 11.99-5.5 3.14a1 1 0 0 0 0 1.74l8.5 4.86a2 2 0 0 0 2 0l8.5-4.86a1 1 0 0 0 0-1.74L16 12"
                    /><path d="m6.49 12.85 11.02 6.3" /><path d="M17.51 12.85 6.5 19.15" /></svg
                >
                &nbsp;<b>Fore</b>head
            </h1>
        </a>
        <div class="header-links">
            <a href="/practice">Practice</a>
            <a href="/rounds">Play</a>
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
    .header-links > a:hover {
        font-weight: bold;
        color: darkgreen;
    }
</style>
