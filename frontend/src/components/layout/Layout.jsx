import React from "react";
import Sidebar from "./Sidebar";
import { useAuth } from "../../context/AuthContext";

const Layout = ({ children }) => {
  const { user } = useAuth();

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar (Fixed width) */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-1 ml-64">
        {/* Top Header */}
        <header className="bg-white shadow-sm h-16 flex items-center justify-between px-8 sticky top-0 z-10">
          <h2 className="text-xl font-semibold text-gray-800">
            Welcome back, {user?.first_name || "Student"} 👋
          </h2>
          <div className="flex items-center gap-4">
            {/* Simple Avatar */}
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold border border-blue-200">
              {user?.first_name?.[0] || "U"}
            </div>
          </div>
        </header>

        {/* Dynamic Page Content */}
        <main className="p-8">{children}</main>
      </div>
    </div>
  );
};

export default Layout;
