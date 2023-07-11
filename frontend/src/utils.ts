import { InjectionKey, inject } from 'vue';

// Ref https://logaretm.com/blog/type-safe-provide-inject/
export const injectStrict = <T>(key: InjectionKey<T>, fallback?: T) => {
  const resolved = inject(key, fallback);
  if (!resolved) {
    throw new Error(`Could not resolve ${key.description}`);
  }
  return resolved;
};

export const getCookieValue = (key: String) => {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(key + '=')) {
      return cookie.substring(key.length + 1);
    }
  }
  return null;
};
