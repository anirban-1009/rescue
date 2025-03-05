import ClientComponentBasicUser from "../clientComponents/BasicUserClient";
import NavBar from "../layout/NavBAR";

type HomePageProps = {
    session: any;
};

export default function BasicUser({ session }: HomePageProps) {
    return (
        <>
            <div className="h-dvh w-dvw">
                <ClientComponentBasicUser
                    location={[20.5937, 78.9629]}
                    session={session}
                />
            </div>
        </>
    );
}
