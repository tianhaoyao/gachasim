import { Game } from '@GameModule/models/Game';
import { ComputedRef, InjectionKey } from 'vue';

// Not being used anymore, left as examples for typed provide / inject
export const SelectedGameKey: InjectionKey<ComputedRef<Game | undefined>> = Symbol('SelectedGame');
