import { Game } from '@GameModule/models/Game';
import { UserId } from '@UserModule/models/User';

export type CreateNewGamePayload = {
  gameName: string;
  selectedImage: File;
  authorId: UserId;
};

export type CreateNewGameSuccessResponse = Game;
