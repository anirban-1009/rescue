import Link from "next/link";

export default function HomePage() {
  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100 dark:bg-gray-900">
      {/* Kinda header */}
      <div className="flex flex-col justify-center items-center w-dvw h-10">
        <div className="text-4xl font-bold">Rescue</div>
      </div>
      {/* Kinda body */}
      <div className="w-dvw p-4">
        <div className="mt-4 w-full max-w-md">
          <Link href="/report">
            <button className="w-full p-4 bg-red-500 text-white rounded-lg text-lg">
              🚨 Report an Incident
            </button>
          </Link>
        </div>

        <div className="mt-6 w-full max-w-md bg-white dark:bg-gray-700 p-4 shadow rounded-lg">
          <h2 className="text-xl font-semibold">Recent Incidents</h2>
          {/* Map incidents here */}
          <p className="text-gray-500">No recent incidents.</p>
          <Link href="/dashboard" className="text-blue-600 underline">View All</Link>
        </div>
      </div>

      {/* Bottom Navigation */}
      <div className="fixed bottom-0 w-full max-w-md dark:bg-gray-700 bg-white flex justify-around p-2 shadow-md">
        <Link href="/" className="text-center">🏠 Home</Link>
        <Link href="/dashboard" className="text-center">📍 Map</Link>
        <Link href="/my-reports" className="text-center">📝 My Reports</Link>
        <Link href="/settings" className="text-center">⚙️ Settings</Link>
      </div>
    </div>
  );
}