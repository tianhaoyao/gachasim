import { GameId } from '@GameModule/models/Game';
import { Rarity } from '@RarityModule/models/Rarity';

export type FetchRaritiesPayload = {
  gameId: GameId;
};

export type FetchRaritiesSuccessResponse = Array<Rarity>;

export type CreateNewRarityPayload = {
  gameId: GameId;
  rarityName: string;
  chance: string;
  pity: string;
  softPity: string;
  softPityChance: string;
  color: string;
  includePity: boolean;
  includeSoftPity: boolean;
};

export type CreateNewRaritySuccessResponse = Rarity;
