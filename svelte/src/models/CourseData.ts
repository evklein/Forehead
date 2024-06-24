export interface CourseData {
    courseId: number;
    numberOfHoles: number;
    public: boolean;
    par: number;
    name: string;
    designer: string;
    address: string;
    imageUrl: string;
    boundPoints: [number, number][];
}