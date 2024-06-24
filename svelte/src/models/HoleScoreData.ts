interface HoleScoreData {
    score: number;
    putts: number;
    greenInRegulation: boolean;
    greenLightDrive: boolean;
    scrambling?: boolean;
    roundId: number;
    holeId: number;
}