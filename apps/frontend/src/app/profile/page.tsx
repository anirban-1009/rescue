import { auth0 } from "@/lib/auth0";
import { AuthSession } from "@/lib/types/User";
import Image from "next/image";
import Link from "next/link";

export default async function Profile() {
    const session = (await auth0.getSession()) as AuthSession | null;

    if (session) {
        return (
            <div className="flex flex-col gap-10 justify-center items-center h-dvh">
                <Image
                    src={session.user.picture}
                    height={100}
                    width={100}
                    alt="profile picture"
                    className="rounded-full"
                />
                <div className="text-3xl">{session.user.name}</div>
                <div className="text-2xl truncate w-70">
                    {session.user.email}
                </div>
                <Link
                    href="/"
                    className="border dark:border-white px-14 py-4 rounded-xl dark:hover:bg-white dark:hover:text-black"
                >
                    Close
                </Link>
            </div>
        );
    }
    return <div>Unauthenticated.</div>;
}
