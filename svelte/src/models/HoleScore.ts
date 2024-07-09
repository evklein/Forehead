import type { HoleStatsData } from './HoleStatsData';
import type { PuttData } from './PuttData';
import type { StrokeData } from './StrokeData';

export interface HoleScore {
    numberOfStrokes?: number;
    numberOfPutts?: number;
    roundId?: number;
    stats: HoleStatsData;
    strokes: StrokeData[];
    putts: PuttData[];
}
