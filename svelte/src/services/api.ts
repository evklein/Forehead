import * as apiHelpers from './apiHelpers';
import type { CourseData } from '../models/CourseData';
import type { HoleData } from '../models/HoleData';
import type { TeeData } from '../models/TeeData';
import type { PuttData } from '../models/PuttData';
import type { StrokeData } from '../models/StrokeData';
import type { HoleStatsData } from '../models/HoleStatsData';
import type { RoundData } from '../models/RoundData';
import type { PracticeStrokeData } from '../models/PracticeStrokeData';
import type { ScrambleGameData } from '../models/ScrambleGameData';
import type { ScrambleRoundData } from '../models/ScrambleRoundData';

const FOREHEAD_API_URL =
    import.meta.env.VITE_BONK_API_URL ?? 'http://localhost:8000';

export async function fetchAllCourses(): Promise<CourseData[] | null> {
    console.log('AHHHh');
    console.log(FOREHEAD_API_URL);
    const endpoint = `/course/all/`;
    try {
        const rawData: any = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        let courses: CourseData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextCourse = rawData[i];
            courses.push({
                courseId: nextCourse['pk'],
                name: nextCourse['fields']['name'],
                address: nextCourse['fields']['address'],
                par: nextCourse['fields']['par'],
                designer: nextCourse['fields']['designer'],
                boundPoints: nextCourse['fields']['bound_points'] ?? [],
                numberOfHoles: nextCourse['fields']['num_holes'],
                imageUrl: nextCourse['fields']['image_url'],
                public: nextCourse['fields']['public'],
            });
        }
        return courses;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return null;
    }
}

export async function fetchCourseDetails(
    id: number,
): Promise<CourseData | null> {
    const endpoint = `/course/${id}/details/`;
    try {
        const rawData: any = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        const course: CourseData = {
            courseId: rawData['pk'],
            name: rawData['fields']['name'],
            address: rawData['fields']['address'],
            par: rawData['fields']['par'],
            designer: rawData['fields']['designer'],
            boundPoints: rawData['fields']['bound_points'] ?? [],
            numberOfHoles: rawData['fields']['num_holes'],
            imageUrl: rawData['fields']['image_url'],
            public: rawData['fields']['public'],
        };
        return course;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return null;
    }
}

export async function saveCourse(id: number, course: CourseData) {
    const endpoint = `/course/${id}/save/`;
    let requestBody: string = JSON.stringify({
        name: course.name,
        address: course.address,
        par: course.par,
        designer: course.designer,
        public: course.public,
        bound_points: course.boundPoints,
        image_url: course.imageUrl,
        num_holes: course.numberOfHoles,
    });

    try {
        await apiHelpers.post(FOREHEAD_API_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function fetchHoles(courseId: number): Promise<HoleData[]> {
    const endpoint = `/course/${courseId}/holes/`;
    try {
        const rawData: any = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        let holes: HoleData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextHoleData = rawData[i];
            holes.push({
                holeNumber: nextHoleData['fields']['hole_number'],
                nickname: nextHoleData['fields']['nickname'],
                par: nextHoleData['fields']['par'],
                boundPoints: nextHoleData['fields']['bound_points'] ?? [],
                centerGreenPoint: JSON.parse(
                    nextHoleData['fields']['center_green_point'],
                ),
                id: nextHoleData['pk'],
            });
        }
        return holes;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return [];
    }
}

export async function fetchHoleDetails(
    courseId: number,
    holeNumber: number,
): Promise<HoleData> {
    const endpoint = `/course/${courseId}/hole/${holeNumber}`;
    try {
        const rawData: any = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        const hole: HoleData = {
            holeNumber: rawData['fields']['hole_number'],
            nickname: rawData['fields']['nickname'],
            par: rawData['fields']['par'],
            boundPoints: rawData['fields']['bound_points'] ?? [],
            centerGreenPoint: JSON.parse(
                rawData['fields']['center_green_point'],
            ),
        };
        return hole;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return {
            holeNumber,
            par: 4,
            boundPoints: [],
        };
    }
}

export async function saveHole(courseId: number, hole: HoleData) {
    const endpoint = `/course/${courseId}/hole/${hole.holeNumber}/save/`;
    let requestBody: string = JSON.stringify({
        hole_number: hole.holeNumber,
        nickname: hole.nickname,
        par: hole.par,
        bound_points: hole.boundPoints,
        center_green_point: hole.centerGreenPoint,
    });
    try {
        await apiHelpers.post(FOREHEAD_API_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function fetchTees(courseId: number) {
    const endpoint = `/course/${courseId}/tees/`;
    try {
        const rawData: any = await apiHelpers.get(FOREHEAD_API_URL, endpoint);

        let tees: TeeData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextObject = rawData[i];
            tees.push({
                id: nextObject['pk'],
                color: nextObject['fields']['color'],
                name: nextObject['fields']['name'],
                yardage: nextObject['fields']['yardage'],
                slope: nextObject['fields']['slope'],
                rating: nextObject['fields']['rating'],
            });
        }
        return tees;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function fetchInProgressRounds() {
    const endpoint = `/round/in-progress/`;
    let rounds: RoundData[] = [];
    try {
        const rawData: any = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        for (let i = 0; i < rawData.length; i++) {
            let nextObject = rawData[i];
            rounds.push({
                id: nextObject['pk'],
                datePlayed: nextObject['fields']['date_played'],
                holesCompleted: nextObject['fields']['holes_completed'],
                courseId: nextObject['fields']['course'],
            });
        }
        return rounds;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function saveNewRound(
    roundData: RoundData,
    courseId: number,
): Promise<number> {
    const endpoint = `/round/new/?course_id=${courseId}&tee_id=${roundData.playedTeeId}`;
    let requestBody: string = JSON.stringify({
        nickname: roundData.nickname,
        date_played: roundData.datePlayed?.toISOString().split('T')[0],
        tee_time: roundData.teeTime,
        finish_time: roundData.finishTime,
        holes_completed: roundData.holesCompleted,
        group_makeup: roundData.groupMakeup,
        mobility: roundData.mobility,
        round_counts_toward_hci: roundData.roundCountsTowardHci,
        notes: roundData.notes,
    });
    try {
        let response = await apiHelpers.post(
            FOREHEAD_API_URL,
            endpoint,
            requestBody,
        );
        return response['round_id'];
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return -1;
    }
}

export async function updateRound(
    roundData: RoundData,
): Promise<number> {
    const endpoint = `/round/${roundData.id}/update/`;
    let requestBody: string = JSON.stringify({
        nickname: roundData.nickname,
        date_played: roundData.datePlayed?.toISOString().split('T')[0],
        tee_time: roundData.teeTime,
        finish_time: roundData.finishTime,
        holes_completed: roundData.holesCompleted,
        group_makeup: roundData.groupMakeup,
        mobility: roundData.mobility,
        round_counts_toward_hci: roundData.roundCountsTowardHci,
        notes: roundData.notes,
    });
    try {
        let response = await apiHelpers.post(
            FOREHEAD_API_URL,
            endpoint,
            requestBody,
        );
        return response['round_id'];
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return -1;
    }
}

export async function saveHoleStats(
    roundId: number,
    holeId: number,
    stats: HoleStatsData,
) {
    const endpoint = `/round/${roundId}/hole/${holeId}/new/`;
    let requestBody: string = JSON.stringify({
        gir: stats.greenInRegulation,
        gld: stats.greenLightDrive,
        scrambling: stats.scrambling,
    });
    console.log(requestBody);
    try {
        await apiHelpers.post(FOREHEAD_API_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function saveStroke(
    roundId: number,
    holeId: number,
    stroke: StrokeData,
) {
    const endpoint = `/round/${roundId}/hole/${holeId}/strokes/new/`;
    let requestBody: string = JSON.stringify({
        stroke_number: stroke.strokeNumber,
        club: stroke.club,
        penalty: stroke.penalty,
        start_coordinate: stroke.startCoordinate,
        end_coordinate: stroke.endCoordinate,
    });
    try {
        await apiHelpers.post(FOREHEAD_API_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function savePutt(
    roundId: number,
    holeId: number,
    putt: PuttData,
) {
    const endpoint = `/round/${roundId}/hole/${holeId}/putts/new/`;
    let requestBody: string = JSON.stringify({
        stroke_number: putt.strokeNumber,
        distance: putt.distance,
    });
    try {
        await apiHelpers.post(FOREHEAD_API_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function getHoleStatsForRound(roundId: number) {
    const endpoint = `/round/${roundId}/stats/`;
    try {
        const rawData: any = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        let stats: HoleStatsData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextStatData = rawData[i];
            stats.push({
                holeNumber: nextStatData['fields']['hole'],
                greenInRegulation: nextStatData['fields']['gir'],
                greenLightDrive: nextStatData['fields']['gld'],
                scrambling: nextStatData['fields']['scrambling'],
            });
        }
        return stats;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function getStrokesForRound(roundId: number) {
    const endpoint = `/round/${roundId}/strokes/`;
    try {
        const rawData: any = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        let strokes: StrokeData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextStroke = rawData[i];
            strokes.push({
                strokeNumber: nextStroke['fields']['stroke_number'],
                club: nextStroke['fields']['club'],
                distance: nextStroke['fields']['distance'],
                startCoordinate: nextStroke['fields']['start_coordinate'],
                endCoordinate: nextStroke['fields']['end_coordinate'],
                penalty: nextStroke['fields']['penalty'],
                holeNumber: nextStroke['fields']['hole'],
            });
        }
        return strokes;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function getPuttsForRound(roundId: number) {
    const endpoint = `/round/${roundId}/putts/`;
    try {
        const rawData: any = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        let putts: PuttData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextPutt = rawData[i];
            putts.push({
                strokeNumber: nextPutt['fields']['stroke_number'],
                distance: nextPutt['fields']['distance'],
                holeNumber: nextPutt['fields']['hole'],
            });
        }
        return putts;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function savePracticeStroke(practiceStroke: PracticeStrokeData) {
    const endpoint = `/practice/stroke/`;
    let requestBody: string = JSON.stringify({
        shot_type: practiceStroke.shotType,
        mis_hit: practiceStroke.misHit,
        shot_distance: practiceStroke.shotDistance,
        result_side: practiceStroke.resultSide,
        result_distance: practiceStroke.resultDistance,
        result_shape_direction: practiceStroke.resultShapeDirection,
        result_shape: practiceStroke.resultShape,
    });
    try {
        let response = await apiHelpers.post(
            FOREHEAD_API_URL,
            endpoint,
            requestBody,
        );
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return -1;
    }
}

export async function savePracticeGame(practiceGame: ScrambleGameData) {
    const endpoint = `/practice/game/`;
    let requestBody: string = JSON.stringify({
        game_type: 'scramble',
        game_data: JSON.stringify(practiceGame),
    });
    try {
        let response = await apiHelpers.post(
            FOREHEAD_API_URL,
            endpoint,
            requestBody,
        );
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return -1;
    }
}

export async function fetchRoundDetails(roundId: number): Promise<RoundData | null> {
    const endpoint = `/round/${roundId}/`;
    try {
        const rawData = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        let roundData = {
            datePlayed: new Date(rawData['fields']['date_played']),
            groupMakeup: rawData['fields']['group_makeup'],
            holesCompleted: rawData['fields']['holes_completed'],
            mobility: rawData['fields']['mobility'],
            teeTime: rawData['fields']['tee_time'],
            finishTime: rawData['fields']['finish_time'],
            nickname: rawData['fields']['nickname'],
            playedTeeId: rawData['fields']['played_tee'],
            roundCountsTowardHci: rawData['fields']['round_counts_toward_hci'],
            courseId: rawData['fields']['course'],
            notes: rawData['fields']['notes'],
            id: rawData['pk']
        } as RoundData;
        return roundData;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return null;
    }
}

export async function fetchRoundHoleStats(roundId: number): Promise<HoleStatsData[] | null> {
    const endpoint = `/round/${roundId}/stats/`;
    try {
        const rawData = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        let stats: HoleStatsData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextSetOfStats = rawData[i];
            stats.push({
                greenLightDrive: nextSetOfStats['fields']['gld'],
                greenInRegulation: nextSetOfStats['fields']['gir'],
                scrambling: nextSetOfStats['fields']['scrambling'],
                holeNumber: nextSetOfStats['fields']['hole'],
                roundId: nextSetOfStats['fields']['rnd'],
            });
        }
        
        return stats;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return null;
    }
}

export async function fetchRoundStrokes(roundId: number): Promise<StrokeData[] | null> {
    const endpoint = `/round/${roundId}/strokes/`;
    try {
        const rawData = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        let fullShots: StrokeData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextFullShot = rawData[i];
            fullShots.push({
                strokeNumber: nextFullShot['fields']['stroke_number'],
                holeNumber: nextFullShot['fields']['hole'],
                penalty: nextFullShot['fields']['penalty'],
                roundId: nextFullShot['fields']['rnd'],
                startCoordinate: nextFullShot['fields']['start_coordinate'],
                endCoordinate: nextFullShot['fields']['end_coordinate'],
                club: nextFullShot['fields']['club']
            })
        }
        return fullShots;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return null;
    }
}

export async function fetchRoundPutts(roundId: number): Promise<PuttData[] | null> {
    const endpoint = `/round/${roundId}/putts/`;
    try {
        const rawData = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        let putts: PuttData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextPutt = rawData[i];
            putts.push({
                strokeNumber: nextPutt['fields']['stroke_number'],
                distance: nextPutt['fields']['distance'],
                holeNumber: nextPutt['fields']['hole'],
                roundId: nextPutt['fields']['rnd']
            })
        }
        return putts;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return null;
    }
}

export async function getRecentUpDownRounds(): Promise<ScrambleRoundData[] | null> {
    const endpoint = `/practice/scramble/recent/`;
    try {
        const rawData = await apiHelpers.get(FOREHEAD_API_URL, endpoint);
        let roundData: ScrambleRoundData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            console.log('Getting round data for ' + i);
            let nextRound = rawData[i];
            console.log(nextRound);
            roundData.push({
                date: new Date(nextRound['date']),
                total: nextRound['totalShots'],
                yards: nextRound['totalYards']
            });
        }
        console.log(roundData);
        return roundData;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return null;
    }
}