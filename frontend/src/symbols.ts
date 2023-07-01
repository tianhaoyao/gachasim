import { Game } from '@GameModule/models/Game';
import { ComputedRef, InjectionKey } from 'vue';

export const SelectedGameKey: InjectionKey<ComputedRef<Game | undefined>> = Symbol('SelectedGame');

export const SetSelectedGameKey: InjectionKey<(game: Game) => void> = Symbol('SetSelectedGame');
