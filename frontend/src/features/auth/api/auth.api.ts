import { apiClient } from '../../../shared/api/client';
import { type LoginFormValues } from '../schemas/login.schema';
import { API_ENDPOINTS } from '../../../shared/api/endpoints';
import type { CurrentUser } from '../types';

type LoginResponse = {
  access: string;
  refresh: string;
  user: CurrentUser | null;
};

export async function login(credentials: LoginFormValues): Promise<LoginResponse> {
  const response = await apiClient.post<LoginResponse>(API_ENDPOINTS.auth.login, credentials);

  return response.data;
}
