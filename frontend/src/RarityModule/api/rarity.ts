import { callApi } from '@/callApi';
import {
  CreateNewRarityPayload,
  CreateNewRaritySuccessResponse,
  FetchRaritiesPayload,
  FetchRaritiesSuccessResponse,
} from '@RarityModule/types/rarity';

export const fetchRarities = async (payload: FetchRaritiesPayload) => {
  const { gameId } = payload;

  return callApi<FetchRaritiesSuccessResponse>({
    endpoint: `/game/rarities/`,
    params: { game_id: gameId },
  });
};

export const createNewRarity = async (payload: CreateNewRarityPayload) => {
  const {
    gameId,
    rarityName,
    chance,
    pity,
    softPity,
    softPityChance,
    color,
    includePity,
    includeSoftPity,
  } = payload;

  const body = JSON.stringify({
    game_id: gameId,
    rarity_name: rarityName,
    chance: chance,
    pity: includePity ? pity : '0',
    softpity: includeSoftPity ? softPity : '0',
    softpitychance: includeSoftPity ? softPityChance : 0,
    color,
  });

  const requestInit = {
    method: 'POST',
    body,
  };

  return callApi<CreateNewRaritySuccessResponse>({
    endpoint: '/game/rarities/',
    requestInit: requestInit,
  });
};
