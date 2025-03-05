"use client";

import { LatLngTuple } from "leaflet";
import React, { useEffect } from "react";
import NoSsr from "../utils/NoSsr";

interface MapProps {
    location: LatLngTuple;
}

export const Map: React.FC<MapProps> = ({ location }) => {
    useEffect(() => {
        const leafletCSS = document.createElement("link");
        leafletCSS.rel = "stylesheet";
        leafletCSS.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
        leafletCSS.integrity =
            "sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=";
        leafletCSS.crossOrigin = "";
        document.head.appendChild(leafletCSS);

        import("leaflet").then((L) => {
            if (typeof window === "undefined") return;

            const mapContainer = document.getElementById("map");
            if (!mapContainer) return;

            if ((window as any).leafletMap) {
                (window as any).leafletMap.setView(location, 17);
                return;
            }

            const map = L.map(mapContainer, {
                zoomControl: false,
                attributionControl: false,
            }).setView(location, 17);

            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                detectRetina: true,
                maxZoom: 19,
            }).addTo(map);

            (window as any).leafletMap = map;

            return () => {
                if ((window as any).leafletMap) {
                    (window as any).leafletMap.remove();
                    delete (window as any).leafletMap;
                }
            };
        });
    }, []);

    return (
        <NoSsr>
            <div id="map" className="h-full w-full z-0"></div>
        </NoSsr>
    );
};

export default Map;
