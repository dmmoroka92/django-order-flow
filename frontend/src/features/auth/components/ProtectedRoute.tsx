import { Navigate, Outlet } from 'react-router';
import { useAppStore } from '../../../app/store';

export function ProtectedRoute() {
  const accessToken = useAppStore((state) => state.accessToken);

  if (!accessToken) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
