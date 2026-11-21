import { useAppStore } from '../../app/store';

export function Header() {
  const user = useAppStore((state) => state.user);

  return (
    <header className="flex h-16 items-center justify-between border-b border-gray-200 bg-white px-6">
      <span className="text-sm font-medium text-gray-600">Order Management</span>

      <div className="flex items-center gap-3">
        <span className="text-sm text-gray-700">
          {user?.firstName} {user?.lastName}
        </span>
      </div>
    </header>
  );
}
