export default function FirstResponderHome() {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold">Welcome, First Responder!</h1>
        <p className="text-gray-600">Here you can manage incidents, view reports, and update your status.</p>
        
        {/* Example Buttons */}
        <div className="mt-4 flex gap-4">
          <button className="bg-blue-500 text-white px-4 py-2 rounded">View Incidents</button>
          <button className="bg-green-500 text-white px-4 py-2 rounded">Update Status</button>
        </div>
      </div>
    );
}