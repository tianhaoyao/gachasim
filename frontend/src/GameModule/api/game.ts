import { callApi } from '@/callApi';
import { Game } from '@GameModule/models/Game';
import { CreateNewGamePayload } from '@GameModule/types/game';

export const fetchGames = async () => {
  return callApi<Array<Game>>({ endpoint: '/game/games/' });
};

export const createNewGame = async (payload: CreateNewGamePayload) => {
  const { gameName, selectedImage, authorId } = payload;

  const formData = new FormData();

  formData.append('gameName', gameName);
  formData.append('selectedImage', selectedImage);
  formData.append('authorId', String(authorId));

  const requestInit = {
    method: 'POST',
    body: formData,
  };

  return callApi<Game>({
    endpoint: '/game/games/',
    requestInit,
  });
};
