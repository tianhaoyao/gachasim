import { Game } from '@GameModule/models/Game';
import { User } from '@UserModule/models/User';
import { ComputedRef, InjectionKey } from 'vue';

export const SelectedGameKey: InjectionKey<ComputedRef<Game | undefined>> = Symbol('SelectedGame');

export const SetSelectedGameKey: InjectionKey<(game: Game) => void> = Symbol('SetSelectedGame');

export const LoggedInUserKey: InjectionKey<ComputedRef<User | undefined>> = Symbol('LoggedInUser');

export const SetLoggedInUserKey: InjectionKey<(user: User) => void> = Symbol('SetLoggedInUser');
