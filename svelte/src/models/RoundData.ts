export interface RoundData {
    id?: number;
    nickname?: string;
    datePlayed?: Date;
    teeTime?: string;
    finishTime?: string;
    holesCompleted?: number;
    groupMakeup?: string;
    mobility?: string;
    roundCountsTowardHci?: boolean;
    notes?: string;

    playedTeeId?: number;
    courseId?: number;
}