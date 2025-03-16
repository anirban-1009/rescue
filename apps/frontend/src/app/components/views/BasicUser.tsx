import Image from "next/image";
import ClientComponentBasicUser from "../clientComponents/BasicUserClient";
import Link from "next/link";
import { AuthSession } from "@/lib/types/User";

type HomePageProps = {
    session: AuthSession;
};

export default function BasicUser({ session }: HomePageProps) {
    return (
        <>
            <div className="h-dvh w-dvw">
                <div className="absolute z-10 right-3 top-3">
                    <Link href="/profile">
                        <Image
                            src={session.user.picture}
                            alt="Profile picture"
                            width={50}
                            height={50}
                            className="rounded-full"
                            priority={true}
                        />
                    </Link>
                </div>
                <ClientComponentBasicUser
                    location={[20.5937, 78.9629]}
                    session={session}
                />
            </div>
        </>
    );
}
