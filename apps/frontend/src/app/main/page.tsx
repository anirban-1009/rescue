'use client';
import React from 'react';

const MainPage = () => {
    return (
        <div className="min-h-screen p-8">
            <h1 className="text-3xl font-bold mb-6">Welcome to Rescue</h1>
            <div className="bg-white rounded-lg shadow-md p-6">
                <p className="text-gray-700">
                    This is a sample main page. You can start building your application here.
                </p>
                <button className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors">
                    Get Started
                </button>
            </div>
        </div>
    );
};

export default MainPage;