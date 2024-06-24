<script>
    import HoleScoreCard from "../../components/round/HoleScoreCard.svelte";
    import Map from "../../components/shared/Map.svelte";

    let courseName = "Sahm Golf Course";
    let numberOfHoles = 18;
</script>

<div class="row align-items-start">
    <div class="col-4">
        <!-- <Map /> -->
    </div>
    <div class="col-8">
        <HoleScoreCard {courseName} {numberOfHoles} />
    </div>
</div>

