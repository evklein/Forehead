import * as apiHelpers from "./apiHelpers";
import type { CourseData } from "../models/CourseData";
import type { HoleData } from "../models/HoleData";
import type { TeeData } from "../models/TeeData";
import type { PuttData } from "../models/PuttData";
import type { StrokeData } from "../models/StrokeData";
import type { HoleStatsData } from "../models/HoleStatsData";
import type { RoundData } from "../models/RoundData";

const BONK_API_URL = import.meta.env.VITE_BONK_API_URL ?? "http://localhost:8000";

export async function fetchAllCourses(): Promise<CourseData[] | null> {
    console.log('AHHHh');
    console.log(BONK_API_URL);
    const endpoint = `/course/all`;
    try {
        const rawData: any = await apiHelpers.get(BONK_API_URL, endpoint);
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

export async function fetchCourseDetails(id: number): Promise<CourseData | null> {
    const endpoint = `/course/${id}/details/`;
    try {
        const rawData: any = await apiHelpers.get(BONK_API_URL, endpoint);
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
        }
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
        await apiHelpers.post(BONK_API_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function fetchHoles(courseId: number): Promise<HoleData[]> {
    const endpoint = `/course/${courseId}/holes/`;
    try {
        const rawData: any = await apiHelpers.get(BONK_API_URL, endpoint);
        let holes: HoleData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextHoleData = rawData[i];
            holes.push({
                holeNumber: nextHoleData['fields']['hole_number'],
                nickname: nextHoleData['fields']['nickname'],
                par: nextHoleData['fields']['par'],
                boundPoints: nextHoleData['fields']['bound_points'] ?? [],
                centerGreenPoint: JSON.parse(nextHoleData['fields']['center_green_point']),
                id: nextHoleData['pk']
            });
        }
        return holes;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return [];
    }
}

export async function fetchHoleDetails(courseId: number, holeNumber: number): Promise<HoleData> {
    const endpoint = `/course/${courseId}/hole/${holeNumber}`;
    try {
        const rawData: any = await apiHelpers.get(BONK_API_URL, endpoint);
        const hole: HoleData = {
            holeNumber: rawData['fields']['hole_number'],
            nickname: rawData['fields']['nickname'],
            par: rawData['fields']['par'],
            boundPoints: rawData['fields']['bound_points'] ?? [],
            centerGreenPoint: JSON.parse(rawData['fields']['center_green_point']),
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
        center_green_point: hole.centerGreenPoint
    });
    try {
        await apiHelpers.post(BONK_API_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function fetchTees(courseId: number) {
    const endpoint = `/course/${courseId}/tees/`;
    try {
        const rawData: any = await apiHelpers.get(BONK_API_URL, endpoint);
        
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

export async function saveRound(roundData: RoundData, courseId: number, teeId: number): Promise<number> {
    const endpoint = `/round/new/?course_id=${courseId}&tee_id=${teeId}`;
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
        let response = await apiHelpers.post(BONK_API_URL, endpoint, requestBody);
        return response['round_id'];
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
        return -1;
    }
}

export async function saveHoleStats(roundId: number, holeId: number, stats: HoleStatsData) {
    const endpoint = `/round/${roundId}/hole/${holeId}/new/`;
    console.log("saving");
    let requestBody: string = JSON.stringify({
        gir: stats.greenInRegulation,
        gld: stats.greenLightDrive,
        scrambling: stats.scrambling,
    });
    console.log(requestBody)
    try {
        await apiHelpers.post(BONK_API_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function saveStroke(roundId: number, holeId: number, stroke: StrokeData) {
    const endpoint = `/round/${roundId}/hole/${holeId}/strokes/new/`;
    let requestBody: string = JSON.stringify({
        stroke_number: stroke.strokeNumber,
        club: stroke.club,
        penalty: stroke.penalty,
        start_coordinate: stroke.startCoordinate,
        end_coordinate: stroke.endCoordinate,
    });
    try {
        await apiHelpers.post(BONK_API_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function savePutt(roundId: number, holeId: number, putt: PuttData) {
    const endpoint = `/round/${roundId}/hole/${holeId}/putts/new/`;
    let requestBody: string = JSON.stringify({
        distance: 10,
        stroke_number: 1,
    });
    try {
        await apiHelpers.post(BONK_API_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function getHoleStatsForRound(roundId: number) {
    const endpoint = `/round/${roundId}/stats/`;
    try {
        const rawData: any = await apiHelpers.get(BONK_API_URL, endpoint);
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
        const rawData: any = await apiHelpers.get(BONK_API_URL, endpoint);
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
                holeNumber: nextStroke['fields']['hole']
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
        const rawData: any = await apiHelpers.get(BONK_API_URL, endpoint);
        let putts: PuttData[] = [];
        for (let i = 0; i < rawData.length; i++) {
            let nextPutt = rawData[i];
            putts.push({
                strokeNumber: nextPutt['fields']['stroke_number'],
                distance: nextPutt['fields']['distance'],
                holeNumber: nextPutt['fields']['hole']
            });
        }
        return putts;
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}