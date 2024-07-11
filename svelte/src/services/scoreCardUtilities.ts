export function getScoreElementBorder(score: number, par: number, borderColor: string = 'black') {
        let differential = par - score;
        if (differential >= 2) return `border: 6px double ${borderColor}; border-radius: 20px;`;
        if (differential === 1) return `border: 2px solid ${borderColor}; border-radius: 20px`;
        if (differential === 0) return ``;
        if (differential === -1) return `border: 2px solid ${borderColor};`;
        if (differential <= -2) return `border: 6px double ${borderColor};`;
}