import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getCourseDetail } from "../../services/courses";
import ReactMarkdown from "react-markdown";
import {
  PlayCircle,
  FileText,
  CheckCircle,
  Menu,
  ChevronLeft,
  Lock,
} from "lucide-react";

const CourseViewer = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();

  const [course, setCourse] = useState(null);
  const [activeLesson, setActiveLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // 1. Fetch Course Data
  useEffect(() => {
    const loadCourse = async () => {
      try {
        const data = await getCourseDetail(courseId);
        setCourse(data);

        // Auto-select the first lesson of the first module
        if (data.modules?.length > 0 && data.modules[0].lessons?.length > 0) {
          setActiveLesson(data.modules[0].lessons[0]);
        }
      } catch (error) {
        console.error("Error loading course:", error);
      } finally {
        setLoading(false);
      }
    };
    loadCourse();
  }, [courseId]);

  if (loading)
    return (
      <div className="h-screen flex items-center justify-center">
        Loading Class...
      </div>
    );
  if (!course) return <div className="p-8">Course not found.</div>;

  // 2. Helper to render content based on type
  const renderContent = () => {
    if (!activeLesson)
      return (
        <div className="p-10 text-gray-500">Select a lesson to start.</div>
      );

    const { type, content } = activeLesson;

    switch (type) {
      case "VIDEO":
        return (
          <div className="aspect-video bg-black rounded-xl overflow-hidden shadow-lg">
            <iframe
              src={content.video_url}
              title={activeLesson.title}
              className="w-full h-full"
              allowFullScreen
            />
          </div>
        );
      case "TEXT":
        return (
          <div className="prose prose-blue max-w-none bg-white p-8 rounded-xl shadow-sm border border-gray-100">
            <ReactMarkdown>
              {content.text || "No content available."}
            </ReactMarkdown>
          </div>
        );
      case "QUIZ":
        return (
          <div className="bg-blue-50 p-10 rounded-xl border border-blue-100 text-center">
            <h3 className="text-xl font-bold text-blue-900 mb-4">Quiz Time!</h3>
            <p className="text-blue-700 mb-6">
              Test your knowledge to continue.
            </p>
            <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
              Start Quiz
            </button>
          </div>
        );
      default:
        return <div>Unknown lesson type</div>;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      {/* --- SIDEBAR (Curriculum) --- */}
      <div
        className={`${
          sidebarOpen ? "w-80" : "w-0"
        } bg-white border-r border-gray-200 transition-all duration-300 flex flex-col`}
      >
        {/* Header */}
        <div className="p-4 border-b border-gray-100 flex items-center justify-between bg-gray-50">
          <button
            onClick={() => navigate("/courses")}
            className="text-gray-500 hover:text-gray-800 flex items-center gap-1 text-sm"
          >
            <ChevronLeft size={16} /> Back
          </button>
          <h2 className="font-bold text-gray-700 truncate ml-2 text-sm">
            {course.title}
          </h2>
        </div>

        {/* Modules List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {course.modules.map((module) => (
            <div key={module.id}>
              <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">
                {module.title}
              </h3>
              <div className="space-y-1">
                {module.lessons.map((lesson) => (
                  <button
                    key={lesson.id}
                    onClick={() => setActiveLesson(lesson)}
                    className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                      activeLesson?.id === lesson.id
                        ? "bg-blue-50 text-blue-700 font-medium"
                        : "text-gray-600 hover:bg-gray-50"
                    }`}
                  >
                    {/* Icon based on Type */}
                    {lesson.type === "VIDEO" ? (
                      <PlayCircle size={16} />
                    ) : (
                      <FileText size={16} />
                    )}
                    <span className="truncate">{lesson.title}</span>

                    {/* Checkmark if done (Placeholder for now) */}
                    {/* <CheckCircle size={14} className="ml-auto text-green-500" /> */}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* --- MAIN CONTENT AREA --- */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative">
        {/* Top Bar */}
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            <Menu size={20} className="text-gray-600" />
          </button>

          <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-gray-500">
              {activeLesson ? activeLesson.title : "Select a Lesson"}
            </span>
            <button className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 flex items-center gap-2">
              Mark Complete <CheckCircle size={16} />
            </button>
          </div>
        </header>

        {/* Scrollable Content */}
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-4xl mx-auto">{renderContent()}</div>
        </main>
      </div>
    </div>
  );
};

export default CourseViewer;
