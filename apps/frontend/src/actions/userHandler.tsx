// User management and interaction code will go here

"use server";

import axios from "axios";
import { getManagementApiToken } from "./authHandler";

export type UserRole = {
    id: string;
    name: string;
    description: string;
};

export const getUserRole = async (user_id: string): Promise<[UserRole]> => {
    const token = await getManagementApiToken();
    const base_url = process.env.AUTH0_DOMAIN;

    if (!token || !base_url ){
        throw Error("Missing required Environment Variables.");
    }

    try{
        const response = await axios.get(
            `https://${base_url}/api/v2/users/${user_id}/roles`,
            {
                headers: {
                    "Authorization": `Bearer ${token.access_token}`,
                    "Content-Type": "application/json",
                },
            }
        );
        return response.data;
    }catch (error) {
        console.error("Error fetching User Role:", error);
        throw new Error("Failed to retrieve User Role");
    }
}