"use server";
import axios from "axios";

type TokenResponse = {
    access_token: string;
    scope: string;
    expires_in: number;
    token_type: string;
}

export const getManagementApiToken = async (): Promise<TokenResponse> => {
    const base_url = process.env.AUTH0_DOMAIN;

    if (!base_url || !process.env.AUTH0_CLIENT_ID || !process.env.AUTH0_CLIENT_SECRET) {
        throw new Error("Missing required environment variables.");
    }
    try {
        const response = await axios.post(`https://${base_url}/oauth/token`,
            {
                "client_id": process.env.AUTH0_CLIENT_ID,
                "client_secret": process.env.AUTH0_CLIENT_SECRET,
                "audience": `https://${base_url}/api/v2/`,
                "grant_type": "client_credentials"
            },
            {
                headers: { 'content-type': 'application/json' },
            }
        );
        return response.data;
    } catch (error) {
      console.error("Error fetching management API token:", error);
      throw new Error("Failed to retrieve management API token");
    }
};
