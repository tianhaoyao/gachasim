import { callApi } from '@/callApi';
import { User } from '@UserModule/models/User';

export const fetchUserDetails = async () => {
  return callApi<User>({ endpoint: '/auth/user-details/' });
};
