import { auth0 } from "@/lib/auth0";

import ClientComponent from "./components/clientComponents/DefaultHomeClient";
import { AuthSession, UserRole } from "@/lib/types/User";
import { getUserRole } from "@/actions/userHandler";
import DefaultHome from "./components/views/DefaultHome";
import BasicUser from "./components/views/BasicUser";
import NavBar from "./components/layout/NavBAR";

export const dynamic = "force-dynamic";

export default async function HomePage() {
    const session = (await auth0.getSession()) as AuthSession | null;
    let userRoles: UserRole[] = [];

    if (session?.user.sub) {
        userRoles = await getUserRole(session.user.sub);
    }

    return (
        <>
            <ClientComponent session={session} userRoles={userRoles} />
            {!session ? (
                <DefaultHome />
            ) : userRoles.find(
                  (role: { name: string }) => role.name === "Basic User"
              ) ? (
                <NavBar>
                    <BasicUser session={session} />
                </NavBar>
            ) : (
                <div>Access Denied</div>
            )}
        </>
    );
}
