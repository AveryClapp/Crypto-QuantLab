import React from "react";

export default function Home() {
  return (
    <div className="relative h-screen w-full overflow-hidden bg-gray-900">
      <div className="absolute -top-48 -left-96 w-1/2 h-1/2 bg-red-500 rounded-full blur-3xl bg-opacity-40"></div>
      <div className="absolute -bottom-48 -left-10 w-1/3 h-1/2 bg-purple-600 rounded-full blur-3xl bg-opacity-30"></div>
      <div className="absolute bottom-48 -right-80 w-1/2 h-1/2 bg-yellow-500 rounded-full blur-3xl bg-opacity-40"></div>

      {/* Content */}
      <div className="relative z-10 flex items-center justify-center h-full">
        <h1 className="text-4xl font-bold text-white">Welcome to My Site</h1>
      </div>
    </div>
  );
}
