import { createBrowserRouter } from 'react-router';

import { DashboardPage } from '../features/dashboard/pages/DashboardPage';
import { LoginPage } from '../features/pages/LoginPage';
import { NotFoundPage } from '../features/pages/NotFoundPage';

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/dashboard',
    element: <DashboardPage />,
  },
  {
    path: '*',
    element: <NotFoundPage />,
  },
]);
