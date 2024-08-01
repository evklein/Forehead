<script>
    import ProgressBar from '../../components/shared/ProgressBar.svelte';
</script>

<div class="row align-items-start">
    <h2>Skills Dashboard</h2>
    <div class="col-12 col-md-5">
        <div class="card">
            <div class="card-body">
                <h4 class="card-title">Calibration Levels</h4>
                <ProgressBar label="Full Shots" color={'#d15b17'} />
                <ProgressBar label="Chipping" color={'#1c9c36'} />
                <ProgressBar label="Putting" color={'#1ea1e3'} />
            </div>
        </div>
    </div>
    <div class="col-12 col-md-5">
        <div class="card">
            <div class="card-body">
                <h4 class="card-title">Recent Differentials</h4>
            </div>
        </div>
    </div>
    <div class="col-12 col-md-6 mt-3">
        <div class="card">
            <div class="card-body">
                <h4 class="card-title">Change in Handicap</h4>
            </div>
        </div>
    </div>
    <div class="col-12 col-md-6 mt-3">
        <div class="card">
            <div class="card-body">
                <h4 class="card-title">Goals</h4>
            </div>
        </div>
    </div>
</div>
