import { LoginForm } from '../auth/components/LoginForm';

export function LoginPage() {
  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-slate-50 px-4 py-12">
      <div className="pointer-events-none absolute -top-32 -left-32 size-96 rounded-full bg-blue-100/60 blur-3xl" />
      <div className="pointer-events-none absolute -right-32 -bottom-32 size-96 rounded-full bg-indigo-100/60 blur-3xl" />

      <div className="relative w-full max-w-md rounded-3xl border border-white bg-white p-8 shadow-2xl shadow-slate-200/60 sm:p-10">
        <div className="mb-8 space-y-3">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Welcome back</h1>

          <p className="text-sm leading-6 text-slate-500">
            Sign in to manage your orders and shipments.
          </p>
        </div>

        <LoginForm />
      </div>
    </main>
  );
}
