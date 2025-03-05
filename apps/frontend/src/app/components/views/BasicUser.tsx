import ClientComponentBasicUser from "../clientComponents/BasicUserClient";

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
