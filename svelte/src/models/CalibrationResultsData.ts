export interface CalibrationResultsData {
    date: Date;
    groundStrikeSuccesses: number;
    faceStrikeSuccesses: number;
    directionSuccesses: number;
}

export interface ChippingCalibrationResultsData {
    date: Date;
    groundStrikeSuccesses: number;
    faceStrikeSuccesses: number;
    distanceSuccesses: number;
    directionSuccesses: number;
}

export interface PuttingCalibrationResultsData {
    date: Date;
    distanceControlSuccesses: number;
    holeSideHigh: number;
    holeSideLow: number;
    numberHoled: number;
}