export interface HoleData {
    id?: number;
    holeNumber: number;
    nickname?: string;
    par: number;
    boundPoints: [number, number][];
    centerGreenPoint?: [number, number];
}