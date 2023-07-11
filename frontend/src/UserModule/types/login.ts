export type LoginPayload = {
  userName: string;
  password: string;
};

export type LoginSuccessResponse = {
  access: Token;
  refresh: Token;
};
