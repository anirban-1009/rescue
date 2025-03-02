
import { auth0 } from '@/lib/auth0';


import UserHome from './components/basicUser';
import ClientComponent from './components/clientComponents/homepage';
import { UserRole } from '@/lib/types/User';
import { getUserRole } from '@/actions/userHandler';
import Home from './components/home';


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
        <Home />
      ) : userRoles.find((role: { name: string }) => role.name === "Basic User") ? (
        <UserHome />
      ) : (
        <div>Access Denied</div>
      )}
    </>
  );
}