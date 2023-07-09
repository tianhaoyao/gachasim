export const getColor = ({
  pityCount,
  softPity,
  color,
}: {
  pityCount: number;
  softPity?: number;
  color?: string;
}) => {
  if (!softPity) return color;

  if (pityCount > softPity && softPity != 0) {
    return '#FF0000';
  }

  return color;
};

export const calculatePercent = ({
  pityCount,
  rarityPity,
}: {
  pityCount: number;
  rarityPity?: number;
}) => {
  const percentage = rarityPity
    ? Math.min(Math.max(Math.floor((pityCount / rarityPity) * 100), 0), 100)
    : 0;

  return percentage + '%';
};
