import type { StateCreator } from 'zustand';
import type { CurrentUser } from '../../../features/auth/types';
import type { AppStore } from '../types';

export type AuthSlice = {
  user: CurrentUser | null;
  accessToken: string | null;

  setUser: (user: CurrentUser | null) => void;
  setAccessToken: (token: string | null) => void;
  clearAuth: () => void;
};

export const createAuthSlice: StateCreator<AppStore, [], [], AuthSlice> = (set) => ({
  user: null,
  accessToken: null,

  setUser: (user) => set({ user }),

  setAccessToken: (accessToken) => set({ accessToken }),

  clearAuth: () =>
    set({
      user: null,
      accessToken: null,
    }),
});
