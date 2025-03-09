export type UserRole = {
    id: string;
    name: string;
    description: string;
};

type User = {
    given_name: string;
    family_name: string;
    nickname: string;
    name: string;
    picture: string;
    email: string;
    email_verified: boolean;
    sub: string;
};

type TokenSet = {
    accessToken: string;
    scope: string;
    refreshToken: string;
    expiresAt: number;
};

type Internal = {
    sid: string;
    createdAt: number;
};

export type AuthSession = {
    user: User;
    tokenSet: TokenSet;
    internal: Internal;
};
