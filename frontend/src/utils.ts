import { InjectionKey, inject } from 'vue';

// Ref https://logaretm.com/blog/type-safe-provide-inject/
export const injectStrict = <T>(key: InjectionKey<T>, fallback?: T) => {
  const resolved = inject(key, fallback);
  if (!resolved) {
    throw new Error(`Could not resolve ${key.description}`);
  }
  return resolved;
};
