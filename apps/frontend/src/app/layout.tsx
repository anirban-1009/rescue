import type { Metadata } from "next";
import "./globals.css";

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
      <body
      >
        {children}
      </body>
    </html>
  );
}
