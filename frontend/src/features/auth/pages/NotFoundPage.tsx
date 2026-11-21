import { Link } from 'react-router';

export function NotFoundPage() {
  return (
    <main>
      <h1>404 — Page not found</h1>
      <Link to="/login">Return to login</Link>
    </main>
  );
}
