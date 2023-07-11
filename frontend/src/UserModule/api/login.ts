import { callApi } from '@/callApi';
import { TokenCookieKeys } from '@/constants/token';
import { LoginPayload, LoginSuccessResponse } from '@UserModule/types/login';
import { fetchUserDetails } from './user';
import { useUserStore } from '@UserModule/stores/UserStore';

export const login = async (payload: LoginPayload) => {
  const { userName, password } = payload;

  const requestInit = {
    method: 'POST',
    body: JSON.stringify({
      username: userName,
      password,
    }),
  };

  const { access: accessToken, refresh: refreshToken } = await callApi<LoginSuccessResponse>({
    endpoint: '/auth/token/',
    requestInit,
  });

  // save access-expiration time cookie set to 5 minutes
  const accessTokenMaxAge = new Date(Date.now() + 300 * 1000).toUTCString();

  // save refresh-expiration time cookie set to 1 day
  const refreshTokenMaxAge = new Date(Date.now() + 86400 * 1000).toUTCString();

  document.cookie = `${TokenCookieKeys.AccessToken}=${accessToken}`;
  document.cookie = `${TokenCookieKeys.RefreshToken}=${refreshToken}`;
  document.cookie = `${TokenCookieKeys.AccessTokenMaxAge}=${accessTokenMaxAge}`;
  document.cookie = `${TokenCookieKeys.RefreshTokenMaxAge}=${refreshTokenMaxAge}`;

  const user = await fetchUserDetails();

  const userStore = useUserStore();

  userStore.setUser(user);
};
