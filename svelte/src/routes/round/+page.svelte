<script>
    import HoleScoreCard from "../../components/round/HoleScoreCard.svelte";
    import Map from "../../components/shared/Map.svelte";

    let courseName = "Sahm Golf Course";
    let numberOfHoles = 18;
</script>

<div class="row align-items-start">
    <div class="card">
        <div class="card-body">
            <h3 class="card-title">
                New Round
                <span class="course-detail"> // {courseName}</span>
                <span class="date-detail">
                    <div class="input-group mb-3 col-6">
                        <span class="input-group-text" id="date-addon"><i class="fa fa-calendar"></i></span>
                        <input type="text"
                            class="form-control"
                            aria-describedby="date-addon"
                            placeholder="Date">
                    </div>
                </span>
            </h3>
            <div class="row align-items-start mt-5">
                <div class="col-3">
                     <div class="input-group mb-3">
                        <span class="input-group-text" id="tee-time-addon"><i class="fa fa-clock"></i></span>
                        <input type="text"
                            class="form-control"
                            aria-describedby="tee-time-addon"
                            placeholder="Tee time">
                    </div>
                </div>
                <div class="col-3">
                     <div class="input-group mb-3">
                        <span class="input-group-text" id="finish-addon"><i class="fa-solid fa-flag-checkered"></i></span>
                        <input type="text"
                            class="form-control"
                            aria-describedby="finish-addon"
                            placeholder="Finish time">
                    </div>
                </div>
                <div class="col-3">
                     <div class="input-group mb-3">
                        <span class="input-group-text" id="holes-addon"><i class="fa-regular fa-square-check"></i></span>
                        <input type="text"
                            class="form-control"
                            aria-describedby="holes-addon"
                            placeholder="Holes completed">
                    </div>
                </div>
                <div class="col-3">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="group-addon"><i class="fa-solid fa-golf-ball-tee"></i></span>
                        <select class="form-select" id="floatingSelect" aria-label="Floating label select example">
                            <option selected>Tee</option>
                            <option value="1">Single</option>
                            <option value="2">Randoms</option>
                            <option value="3">Friends</option>
                        </select>
                    </div>
                </div>
                <div class="col-3">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="group-addon"><i class="fa-solid fa-user-group"></i></span>
                        <select class="form-select" id="floatingSelect" aria-label="Floating label select example">
                            <option selected>Group</option>
                            <option value="1">Single</option>
                            <option value="2">Randoms</option>
                            <option value="3">Friends</option>
                        </select>
                    </div>
                </div>
                <div class="col-3">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="group-addon"><i class="fa-solid fa-person-walking"></i></span>
                        <select class="form-select" id="floatingSelect" aria-label="Floating label select example">
                            <option selected>Mobility</option>
                            <option value="1">Single</option>
                            <option value="2">Randoms</option>
                            <option value="3">Friends / Family</option>
                        </select>
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                    <label class="form-check-label" for="flexCheckDefault">
                        Round counts toward Handicap Index
                    </label>
                    </div>
                </div>
                <div class="col-11">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="bounds-addon"><i class="fa-solid fa-list"></i></span>
                        <textarea
                            class="form-control"
                            placeholder="Notes"
                            aria-describedby="bounds-addon"
                            rows="4"
                        />
                    </div>
                </div>
                <div class="card-buttons">
                    <button
                        class="btn btn-success">
                        <i class="fa-solid fa-check"></i> Save Course
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>
<style>
    .course-detail {
        font-size: 14pt;
    }
    .date-detail {
        float: right;
    }
</style>

