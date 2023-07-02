import { RarityId } from '@RarityModule/models/Rarity';

export type ItemId = number;

export type Item = {
  id: ItemId;
  rarity_id: RarityId;
  item_name: string;
  image: string;
  chance: number;
};
