'use client';

import { useEffect } from 'react';
import { UserRole } from "@/lib/types/User";

type ClientComponentProps = {
  session: any;
  userRoles: UserRole[];
};

export default function ClientComponent({ session, userRoles }: ClientComponentProps) {

  return null;
}