import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

import { createAuthSlice } from './slices/auth.slice';
import type { AppStore } from './types';

export const useAppStore = create<AppStore>()(
  devtools(
    persist(
      (...args) => ({
        ...createAuthSlice(...args),
      }),
      {
        name: 'orderflow-store',
        partialize: (state) => ({
          accessToken: state.accessToken,
          user: state.user,
        }),
      },
    ),
    {
      name: 'OrderFlow Store',
      enabled: import.meta.env.DEV,
    },
  ),
);
