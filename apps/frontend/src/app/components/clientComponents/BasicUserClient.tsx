"use client";

import { LatLngTuple } from "leaflet";
import Map from "./map_client";
import NoSsr from "../utils/NoSsr";

type ClientComponentProps = {
    session: any;
    location: LatLngTuple;
};

export default function ClientComponentBasicUser({
    session,
    location,
}: ClientComponentProps) {
    return <Map location={location} />;
}
