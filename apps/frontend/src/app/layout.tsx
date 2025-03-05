import type { Metadata } from "next";
import "./globals.css";
import NavBar from "./components/layout/NavBAR";

export const metadata: Metadata = {
    title: "Rescue",
    description: "Emergency Response Management and Coordination Platform",
    icons: {
        icon: [
            {
                url: "/favicon.ico",
                sizes: "any",
            },
        ],
    },
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body>
                <NavBar>{children}</NavBar>
            </body>
        </html>
    );
}
