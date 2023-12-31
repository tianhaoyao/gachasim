import { Item } from '@ItemModule/models/Item';
import { Rarity, RarityId } from '@RarityModule/models/Rarity';

export type Roll = {
  rarity: Rarity;
  item: Item;
  pity: Record<RarityId, number>;
};

export type RaritiesHash = Record<RarityId, Rarity>;
