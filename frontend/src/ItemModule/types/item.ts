import { Item } from '@ItemModule/models/Item';

export type CreateNewItemPayload = {
  rarityId: number;
  itemName: string;
  selectedImage: File;
  chance: number;
};

export type CreateNewItemSuccessResponse = Item;
