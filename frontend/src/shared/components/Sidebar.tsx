import { NavLink } from 'react-router';

const navigation = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Products', path: '/products' },
  { label: 'Shipments', path: '/shipments' },
];

export function Sidebar() {
  return (
    <aside className="w-60 shrink-0 border-r border-gray-200 bg-white p-4">
      <h1 className="mb-8 text-xl font-bold text-gray-900">OrderFlow</h1>

      <nav className="space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `block rounded-md px-4 py-2 text-sm font-medium ${
                isActive ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
