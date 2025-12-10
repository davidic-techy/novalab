import React, { useEffect, useState } from "react";
import { getSchoolStats } from "../../services/analytics";
import { Users, Activity, Award } from "lucide-react";

const TeacherDashboard = ({ user }) => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getSchoolStats().then(setStats).catch(console.error);
  }, []);

  if (!stats) return <div>Loading school data...</div>;

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">School Overview</h1>
        <span className="bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full font-bold">
          {user.school || "No School Assigned"}
        </span>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-3 mb-2">
            <Users className="text-blue-600" />
            <h3 className="font-bold text-gray-700">Total Students</h3>
          </div>
          <p className="text-3xl font-bold">{stats.total_students}</p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="text-orange-600" />
            <h3 className="font-bold text-gray-700">Active Projects</h3>
          </div>
          <p className="text-3xl font-bold">{stats.active_projects}</p>
        </div>
      </div>

      {/* Leaderboard Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h3 className="font-bold text-gray-800">Top Performing Students</h3>
          <Award className="text-yellow-500" />
        </div>
        <table className="w-full text-left text-sm text-gray-600">
          <thead className="bg-gray-50 text-xs uppercase font-bold text-gray-500">
            <tr>
              <th className="px-6 py-3">Student Name</th>
              <th className="px-6 py-3">Email</th>
              <th className="px-6 py-3">Badges Earned</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {stats.leaderboard.map((student, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-6 py-4 font-medium text-gray-800">
                  {student.user__first_name} {student.user__last_name}
                </td>
                <td className="px-6 py-4">{student.user__email}</td>
                <td className="px-6 py-4 text-blue-600 font-bold">
                  {student.badge_count}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TeacherDashboard;
