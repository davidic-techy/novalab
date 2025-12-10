import React, { useEffect, useState } from "react";
import { getCourses } from "../../services/courses";
import { BookOpen, Clock, ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";

const CourseList = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const data = await getCourses();
        setCourses(data);
      } catch (error) {
        console.error("Failed to fetch courses", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, []);

  if (loading) return <div className="p-8">Loading Courses...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">My Courses</h1>
          <p className="text-gray-500 mt-1">Continue where you left off</p>
        </div>
      </div>

      {courses.length === 0 ? (
        <div className="p-10 text-center bg-white rounded-xl shadow-sm">
          <p className="text-gray-400">No courses available yet.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <div
              key={course.id}
              className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition duration-200 flex flex-col"
            >
              {/* Thumbnail Placeholder */}
              <div className="h-40 bg-blue-100 flex items-center justify-center">
                {course.thumbnail ? (
                  <img
                    src={course.thumbnail}
                    alt={course.title}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <BookOpen size={48} className="text-blue-300" />
                )}
              </div>

              {/* Content */}
              <div className="p-5 flex-1 flex flex-col">
                <h3 className="font-bold text-lg text-gray-800 mb-2">
                  {course.title}
                </h3>
                <p className="text-sm text-gray-500 line-clamp-2 mb-4 flex-1">
                  {course.description}
                </p>

                <div className="flex items-center justify-between mt-auto pt-4 border-t border-gray-50">
                  <div className="flex items-center text-xs text-gray-400 gap-1">
                    <Clock size={14} />
                    <span>2h 15m</span>
                  </div>

                  <Link
                    to={`/courses/${course.id}`}
                    className="flex items-center gap-1 text-sm font-semibold text-blue-600 hover:text-blue-700"
                  >
                    Start Learning <ChevronRight size={16} />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CourseList;
