import Link from "next/link";
import React from "react";

const NavBar: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div className="relative">
        {children}
        <div className="absolute bottom-0 w-full h-fit left-1/2 transform -translate-x-1/2 z-10 bg-white p-4 rounded-t-lg shadow-md dark:bg-gray-700 dark:text-slate-50">
            <div className="flex justify-center items-center text-2xl gap-24">
                <Link href="#">📃</Link>
                <Link href="/">🏠</Link>
                <Link href="#">‼</Link>
            </div>
        </div>
    </div>
);

export default NavBar;
