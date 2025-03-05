import ClientComponentBasicUser from "../clientComponents/BasicUserClient";

type HomePageProps = {
    session: any;
};

export default function BasicUser({ session }: HomePageProps) {
    return (
        <>
            <div className="z-1 w-fit">Hello</div>
            <div className="h-dvh w-dvw">
                <ClientComponentBasicUser location={[0, 0]} session={session} />
            </div>
        </>
    );
}
