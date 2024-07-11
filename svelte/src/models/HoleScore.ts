import type { HoleStatsData } from './HoleStatsData';
import type { PuttData } from './PuttData';
import type { StrokeData } from './StrokeData';

export interface HoleScore {
    roundId?: number;
    stats: HoleStatsData;
    fullShots: StrokeData[];
    putts: PuttData[];
}
