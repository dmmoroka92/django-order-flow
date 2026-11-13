import { useForm } from 'react-hook-form';
import { LoginSchema, type LoginFormValues } from '../schemas/login.schema';
import { zodResolver } from '@hookform/resolvers/zod';

export const LoginForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
    },
  });

  const onSubmit = (data: LoginFormValues) => {
    console.log('Login form submitted', data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate className="w-full space-y-6">
      <div className="space-y-2">
        <label htmlFor="email" className="block text-sm font-semibold text-slate-700">
          Email address
        </label>

        <input
          id="email"
          type="email"
          autoComplete="email"
          placeholder="you@company.com"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
          {...register('email')}
          className={`block w-full rounded-xl border bg-white px-4 py-3.5
            text-sm text-slate-900 shadow-sm outline-none
            transition-all duration-200
            placeholder:text-slate-400
            hover:border-slate-300
            focus:ring-4
            ${
              errors.email
                ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/10'
                : 'border-slate-200 focus:border-blue-500 focus:ring-blue-500/10'
            }`}
        />

        {errors.email && (
          <p
            id="email-error"
            role="alert"
            className="flex items-center gap-1.5 text-xs font-medium text-rose-600"
          >
            <span aria-hidden="true">!</span>
            {errors.email.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="password" className="block text-sm font-semibold text-slate-700">
          Password
        </label>

        <input
          id="password"
          type="password"
          autoComplete="new-password"
          placeholder="Enter your password"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : undefined}
          {...register('password')}
          className={`block w-full rounded-xl border bg-white px-4 py-3.5
            text-sm text-slate-900 shadow-sm outline-none
            transition-all duration-200
            placeholder:text-slate-400
            hover:border-slate-300
            focus:ring-4
            ${
              errors.password
                ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/10'
                : 'border-slate-200 focus:border-blue-500 focus:ring-blue-500/10'
            }`}
        />

        {errors.password && (
          <p id="password-error" role="alert" className="text-xs font-medium text-rose-600">
            {errors.password.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="confirmPassword" className="block text-sm font-semibold text-slate-700">
          Confirm password
        </label>

        <input
          id="confirmPassword"
          type="password"
          autoComplete="new-password"
          placeholder="Confirm your password"
          aria-invalid={!!errors.confirmPassword}
          aria-describedby={errors.confirmPassword ? 'confirm-password-error' : undefined}
          {...register('confirmPassword')}
          className={`block w-full rounded-xl border bg-white px-4 py-3.5
            text-sm text-slate-900 shadow-sm outline-none
            transition-all duration-200
            placeholder:text-slate-400
            hover:border-slate-300
            focus:ring-4
            ${
              errors.confirmPassword
                ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/10'
                : 'border-slate-200 focus:border-blue-500 focus:ring-blue-500/10'
            }`}
        />

        {errors.confirmPassword && (
          <p id="confirm-password-error" role="alert" className="text-xs font-medium text-rose-600">
            {errors.confirmPassword.message}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="group flex w-full items-center justify-center gap-2
          rounded-xl bg-blue-600 px-5 py-3.5
          text-sm font-semibold text-white
          shadow-lg shadow-blue-600/20
          transition-all duration-200
          hover:-translate-y-0.5 hover:bg-blue-700
          hover:shadow-xl hover:shadow-blue-600/25
          focus-visible:outline-2 focus-visible:outline-offset-2
          focus-visible:outline-blue-600
          active:translate-y-0
          disabled:cursor-not-allowed disabled:opacity-60
          disabled:hover:translate-y-0"
      >
        {isSubmitting ? (
          <>
            <span
              className="size-4 animate-spin rounded-full
                border-2 border-white/30 border-t-white"
              aria-hidden="true"
            />
            <span>Processing...</span>
          </>
        ) : (
          <>
            <span>Continue</span>
            <span aria-hidden="true" className="transition-transform group-hover:translate-x-1">
              →
            </span>
          </>
        )}
      </button>
    </form>
  );
};
