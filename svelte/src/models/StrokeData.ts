export interface StrokeData {
    strokeNumber?: number;
    club?: string;
    distance?: number;
    startCoordinate?: [number, number];
    endCoordinate?: [number, number];
    roundId?: number;
    holeNumber: number;
    penalty?: boolean;
}
