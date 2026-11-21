import { useAppStore } from '../../../app/store';

export function DashboardPage() {
  const user = useAppStore((state) => state.user);

  return (
    <main>
      <h1>Dashboard</h1>
      <p>Welcome, {user?.firstName}!</p>
    </main>
  );
}
