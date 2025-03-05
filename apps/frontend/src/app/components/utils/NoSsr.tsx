import dynamic from "next/dynamic";
import React from "react";

const NoSsr: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <>{children}</>
);

export default dynamic(() => Promise.resolve(NoSsr), { ssr: false });
