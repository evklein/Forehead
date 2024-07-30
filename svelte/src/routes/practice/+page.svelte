<script lang="ts">
    import PracticeModeCard from '../../components/practice/PracticeModeCard.svelte';
</script>

<div class="row align-items-start">
    <h2>Practice</h2>
    <PracticeModeCard
        mode="Range Record"
        description="Hit range balls and collect shot data."
        imagePath="https://cdn.shipsticks.com/blog/wp-content/uploads/2022/02/DRIVING_RANGE_FIXED.jpg"
        link="/practice/range"
    />
    <PracticeModeCard
        mode="Up & Down"
        description="18 holes - chipping and putting only."
        imagePath="https://media.istockphoto.com/id/472810042/photo/golfer-chipping.jpg?s=612x612&w=0&k=20&c=laQx0K1DEtrP4Dj9jxENLarfmTCpxRe3opoz5AJsB7o="
        link="/practice/scramble"
        badgeText="Game"
    />
    <PracticeModeCard
        mode="Swing Calibration"
        description="Test swing for weaknesses."
        imagePath="https://media.istockphoto.com/id/1289137258/photo/asian-chinese-mature-man-golf-couch-teaching-young-male-student-to-play-golf-at-driving-range.jpg?s=612x612&w=0&k=20&c=upfK8gdl0rzw_a-xLlGDM2TwgVR5Ke3LbmniwDJFunQ="
        link="/practice/calibration"
        badgeText="Calibration"
    />
    <PracticeModeCard
        mode="Chipping Calibration"
        description="Test short game"
        imagePath="https://t3.ftcdn.net/jpg/00/34/76/76/360_F_34767677_Dqf96hfvrHnk0guiMRHbfBxhAYBqD0VG.jpg"
        link="/practice/chipping-calibration"
        badgeText="Calibration"
    />
    <PracticeModeCard
        mode="Putting Calibration"
        description="Test putting"
        imagePath="https://media.istockphoto.com/id/882323218/photo/this-is-going-to-be-in.jpg?s=612x612&w=0&k=20&c=vX4pi2tVwE3unRMc443FlJmzI4wT4KlIzXAh0HXZQuU="
        link="/practice/putting-calibration"
        badgeText="Calibration"
    />
</div>
