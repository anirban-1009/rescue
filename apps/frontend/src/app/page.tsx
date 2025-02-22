"use server";

import Home from "../components/home";
import { auth0 } from "@/lib/auth0";
import Link from "next/link";

export default async function Page() {

  const session = await auth0.getSession();

  if (!session){
    return (
      <Home />
    )
  }
  return (
    <div className="flex flex-col items-center justify-center w-dvw h-dvh text-2xl">
      <a className="text-2xl">Hello - {session.user.name}</a><br/>
      <Link href="/auth/logout" className="h-fit w-fit py-2 px-7 dark:text-black bg-white rounded-full">Logout</Link>
    </div>
  )
}