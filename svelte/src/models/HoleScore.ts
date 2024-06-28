import type { HoleStatsData } from "./HoleStatsData";
import type { PuttData } from "./PuttData";
import type { StrokeData } from "./StrokeData";

export interface HoleScore {
    score?: number;
    roundId?: number;
    stats: HoleStatsData;
    strokes: StrokeData[];
    putts: PuttData[];
}