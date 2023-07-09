import { getCookieValue } from '@/utils';

const backendBaseUrl = 'http://localhost:8000';
const refreshEndpoint = '/auth/token/refresh/';

export const callApi = async <T = unknown>({
  endpoint,
  requestInit = {},
  params,
}: {
  endpoint: string;
  requestInit?: RequestInit;
  params?: Record<string, any>;
}): Promise<T> => {
  const isFormData = requestInit.body instanceof FormData;

  requestInit.headers = {
    ...requestInit.headers,
    ...(isFormData ? {} : { 'Content-Type': 'application/json' }),
  };

  const url = new URL(endpoint, backendBaseUrl);

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url.searchParams.append(key, String(value));
    });
  }

  const accessToken = getCookieValue('access-token');

  if (accessToken) {
    requestInit.headers = {
      ...requestInit.headers,
      Authorization: `Bearer ${accessToken}`,
    };

    requestInit.credentials = 'include';

    const accessTokenExpirationDateString = getCookieValue('access-expiry');

    if (!accessTokenExpirationDateString) {
      throw new Error('Access token exists but expiration is missing');
    }

    const accessTokenExpirationDate = new Date(decodeURIComponent(accessTokenExpirationDateString));
    const currentTime = Date.now();

    // Check if access token has expired
    if (accessTokenExpirationDateString && accessTokenExpirationDate.getTime() <= currentTime) {
      // Access token is expired, try refreshing it
      try {
        const refreshedToken = await refreshAccessToken();
        requestInit.headers = {
          ...requestInit.headers,
          Authorization: `Bearer ${refreshedToken}`,
        };
      } catch (error) {
        console.log('Failed to refresh access token', error);
      }
    }
  }
  const response = await fetch(url.toString(), requestInit);

  if (!response.ok) {
    console.error(response);
    throw new Error('Request failed');
  }

  return response.json() as Promise<T>;
};

const refreshAccessToken = async () => {
  // Check refresh token has not expired
  const refreshTokenExpirationDateString = getCookieValue('refresh-expiry');
  if (refreshTokenExpirationDateString) {
    const currentTime = Date.now();
    const refreshTokenExpirationDate = new Date(
      decodeURIComponent(refreshTokenExpirationDateString)
    );
    // Check if refresh token is expired
    if (refreshTokenExpirationDate.getTime() <= currentTime) {
      // TODO: decide what to do if refresh token is expired
      throw new Error('Refresh token has expired');
    }
  } else {
    throw new Error('Refresh token does not exist');
  }

  // Call the API to refresh the access token using the refresh token

  const response = await fetch(`${backendBaseUrl}${refreshEndpoint}`, {
    method: 'POST',
    body: JSON.stringify({
      refresh: getCookieValue('refresh-token'),
    }),
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to refresh access token');
  }

  try {
    const data = await response.json();
    // Save the new access token in the cookie
    const accessToken = data.access;
    // Set the expiration time to be 5 minutes
    const accessExpiryDate = new Date(Date.now() + 300 * 1000);
    document.cookie = `access-token=${accessToken}`;

    document.cookie = `access-expiry=${accessExpiryDate.toUTCString()}`;
    return accessToken;
  } catch (err) {
    throw new Error('Failed to parse response data');
  }
};
