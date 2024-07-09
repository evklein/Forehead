<script lang="ts">
    import PracticeModeCard from '../../components/practice/PracticeModeCard.svelte';
</script>

<div class="row align-items-start">
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
</div>
