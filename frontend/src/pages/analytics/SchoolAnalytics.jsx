import React, { useEffect, useState } from "react";
import { getDashboardStats } from "../../services/analytics";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Legend,
} from "recharts";
import { TrendingUp, Users, BookOpen, Activity } from "lucide-react";

const SchoolAnalytics = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const stats = await getDashboardStats();
        // Reverse data so it goes from Oldest -> Newest (Left to Right)
        setData(stats.reverse());
      } catch (error) {
        console.error("Error loading stats", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="p-8">Loading Data...</div>;

  // Calculate Totals for the Top Cards
  const totalLogins = data.reduce((acc, curr) => acc + curr.total_logins, 0);
  const totalLessons = data.reduce(
    (acc, curr) => acc + curr.lessons_completed,
    0
  );
  const totalLabs = data.reduce((acc, curr) => acc + curr.labs_run, 0);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">School Analytics</h1>
        <p className="text-gray-500 mt-1">
          Performance metrics for the last 7 days.
        </p>
      </div>

      {/* --- KPI CARDS --- */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          title="Total Logins"
          value={totalLogins}
          icon={Users}
          color="bg-blue-500"
        />
        <StatCard
          title="Lessons Completed"
          value={totalLessons}
          icon={BookOpen}
          color="bg-green-500"
        />
        <StatCard
          title="Labs Run"
          value={totalLabs}
          icon={Activity}
          color="bg-purple-500"
        />
        <StatCard
          title="Avg Engagement"
          value={data.length > 0 ? Math.round(totalLogins / data.length) : 0}
          suffix="/day"
          icon={TrendingUp}
          color="bg-orange-500"
        />
      </div>

      {/* --- CHARTS --- */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Chart 1: Activity Trends (Area) */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-80">
          <h3 className="font-bold text-gray-700 mb-6">Activity Trends</h3>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="colorLogins" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="date" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Area
                type="monotone"
                dataKey="total_logins"
                stroke="#3B82F6"
                fillOpacity={1}
                fill="url(#colorLogins)"
                name="Logins"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Chart 2: Learning vs Doing (Bar) */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-80">
          <h3 className="font-bold text-gray-700 mb-6">Theory vs Practice</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="date" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Bar
                dataKey="lessons_completed"
                name="Lessons"
                fill="#10B981"
                radius={[4, 4, 0, 0]}
              />
              <Bar
                dataKey="labs_run"
                name="Labs"
                fill="#8B5CF6"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

// Helper Component for Cards
const StatCard = ({ title, value, suffix = "", color }) => (
  <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
    <div>
      <p className="text-sm text-gray-500 font-medium">{title}</p>
      <h3 className="text-2xl font-bold text-gray-800 mt-1">
        {value}
        {suffix && (
          <span className="text-sm text-gray-400 font-normal">{suffix}</span>
        )}
      </h3>
    </div>
    <div className={`p-3 rounded-lg text-white ${color}`}>
      <Icon size={24} />
    </div>
  </div>
);

export default SchoolAnalytics;
