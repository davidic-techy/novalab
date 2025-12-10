import React, { useEffect, useState } from "react";
import { getStudentStats } from "../../services/analytics";
import {
  Trophy,
  Star,
  BookOpen,
  Target,
  ArrowRight,
  PlayCircle,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

const StudentDashboard = ({ user }) => {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    getStudentStats().then(setData).catch(console.error);
  }, []);

  if (!data) return <div className="p-8">Loading your progress...</div>;

  // --- CRASH PREVENTION ---
  const recommendations = data.recommendations || [];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Hello, {user.first_name}! 🚀
          </h1>
          <p className="text-gray-500 mt-1">
            Ready to learn something new today?
          </p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          icon={Star}
          label="Total XP"
          value={data.xp || 0}
          color="bg-yellow-500"
        />
        <StatCard
          icon={Trophy}
          label="Badges"
          value={data.badges || 0}
          color="bg-purple-500"
        />
        <StatCard
          icon={Target}
          label="Avg Grade"
          value={`${data.avg_grade || 0}%`}
          color="bg-green-500"
        />
        <StatCard
          icon={BookOpen}
          label="Projects"
          value={data.projects_completed || 0}
          color="bg-blue-500"
        />
      </div>

      {/* Recommended Courses */}
      <div>
        <h2 className="text-xl font-bold text-gray-800 mb-4">
          Recommended For You
        </h2>

        {recommendations.length === 0 ? (
          <div className="p-6 bg-gray-50 rounded-xl text-center text-gray-500 text-sm border border-gray-100">
            You are up to date! No new courses available.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {recommendations.map((course) => (
              <div
                key={course.id}
                className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition group"
              >
                <div className="h-32 bg-blue-50 rounded-lg mb-4 flex items-center justify-center text-blue-200">
                  {course.thumbnail ? (
                    <img
                      src={course.thumbnail}
                      className="w-full h-full object-cover rounded-lg"
                    />
                  ) : (
                    <BookOpen size={40} />
                  )}
                </div>
                <h3 className="font-bold text-gray-800 mb-1 line-clamp-1">
                  {course.title}
                </h3>
                <p className="text-xs text-gray-500 mb-4 line-clamp-2">
                  {course.description}
                </p>

                <button
                  onClick={() => navigate(`/courses/${course.id}`)}
                  className="w-full flex items-center justify-center gap-2 bg-slate-900 text-white py-2 rounded-lg text-sm hover:bg-slate-800 transition"
                >
                  <PlayCircle size={16} /> Start Course
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Encouragement Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-8 text-white flex justify-between items-center shadow-lg">
        <div>
          <h2 className="text-xl font-bold mb-1">Keep the streak alive!</h2>
          <p className="text-blue-100 text-sm">
            Complete one more lab to unlock the "Science Whiz" badge.
          </p>
        </div>
        <button
          onClick={() => navigate("/labs")}
          className="bg-white text-blue-600 hover:bg-blue-50 px-6 py-2 rounded-lg font-bold transition flex items-center gap-2"
        >
          Go to Labs <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
};

// --- FIX IS HERE: Renaming 'icon' prop to 'Icon' variable ---
const StatCard = ({ icon: Icon, label, value, color }) => (
  <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
    <div className={`p-3 rounded-full text-white ${color}`}>
      <Icon size={20} />
    </div>
    <div>
      <p className="text-xs text-gray-500 uppercase font-bold">{label}</p>
      <h3 className="text-xl font-bold text-gray-800">{value}</h3>
    </div>
  </div>
);

export default StudentDashboard;
