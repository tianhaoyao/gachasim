import { GameId } from './Game';

export type RarityId = number;

export type Rarity = {
  id: RarityId;
  game_id: GameId;
  rarity_name: string;
  chance: number;
  pity: number;
  softpity: number;
  softpitychance: number;
  color: string;
};
