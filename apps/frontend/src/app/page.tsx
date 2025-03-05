import { auth0 } from "@/lib/auth0";

import ClientComponent from "./components/clientComponents/DefaultHomeClient";
import { UserRole } from "@/lib/types/User";
import { getUserRole } from "@/actions/userHandler";
import DefaultHome from "./components/views/DefaultHome";
import BasicUser from "./components/views/BasicUser";

export default async function HomePage() {
    const session = await auth0.getSession();
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
                <BasicUser session={session} />
            ) : (
                <div>Access Denied</div>
            )}
        </>
    );
}
