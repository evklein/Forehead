import * as apiHelpers from "./apiHelpers";
import type { CourseData } from "../models/CourseData";
import type { HoleData } from "../models/HoleData";

const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchAllCourses(): Promise<CourseData[] | null> {
    const endpoint = `/course/all`;
    try {
        const rawData: any = await apiHelpers.get(API_BASE_URL, endpoint);
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
        const rawData: any = await apiHelpers.get(API_BASE_URL, endpoint);
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
        await apiHelpers.post(API_BASE_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function fetchHoleDetails(courseId: number, holeNumber: number): Promise<HoleData> {
    const endpoint = `/course/${courseId}/hole/${holeNumber}`;
    try {
        const rawData: any = await apiHelpers.get(API_BASE_URL, endpoint);
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
        await apiHelpers.post(API_BASE_URL, endpoint, requestBody);
    } catch (error) {
        console.error(`${endpoint}: request failed.`);
        console.error(error);
    }
}

export async function fetchTees(courseId: number) {
    const endpoint = `/course/${courseId}/tees/`;
    try {
        const rawData: any = await apiHelpers.get(API_BASE_URL, endpoint);
        
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