import { callApi } from '@/callApi';
import { CreateNewItemPayload, CreateNewItemSuccessResponse } from '@ItemModule/types/item';

export const createNewItem = async (payload: CreateNewItemPayload) => {
  const { rarityId, itemName, selectedImage, chance } = payload;

  const formData = new FormData();

  formData.append('rarity_id', String(rarityId));
  formData.append('item_name', itemName);
  formData.append('image', selectedImage);
  formData.append('chance', String(chance));

  const requestInit = {
    method: 'POST',
    body: formData,
  };

  return callApi<CreateNewItemSuccessResponse>({
    endpoint: '/game/items/',
    requestInit: requestInit,
  });
};
