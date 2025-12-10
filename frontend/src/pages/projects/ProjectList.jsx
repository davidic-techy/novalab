import React, { useEffect, useState } from "react";
import {
  getProjectTemplates,
  getMyProjects,
  startProject,
} from "../../services/projects";
import { FolderPlus, Code, ArrowRight, Loader } from "lucide-react";
import { useNavigate } from "react-router-dom";

const ProjectList = () => {
  const [templates, setTemplates] = useState([]);
  const [myProjects, setMyProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [tplData, projData] = await Promise.all([
          getProjectTemplates(),
          getMyProjects(),
        ]);
        setTemplates(tplData);
        setMyProjects(projData);
      } catch (error) {
        console.error("Error fetching projects:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleStart = async (templateId) => {
    if (!window.confirm("Start this new project?")) return;
    try {
      const newProj = await startProject(templateId);
      navigate(`/projects/${newProj.id}`);
    } catch (err) {
      alert(
        "Could not start project: " + err.response?.data?.error || err.message
      );
    }
  };

  if (loading) return <div className="p-8">Loading Projects...</div>;

  return (
    <div className="space-y-10">
      {/* SECTION 1: MY ACTIVE PROJECTS */}
      <div>
        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <Code className="text-blue-600" /> My Active Projects
        </h2>
        {myProjects.length === 0 ? (
          <div className="p-6 bg-blue-50 rounded-xl border border-blue-100 text-blue-700 text-sm">
            You haven't started any projects yet. Pick a template below!
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {myProjects.map((proj) => (
              <div
                key={proj.id}
                className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex justify-between items-center"
              >
                <div>
                  <h3 className="font-bold text-gray-800">
                    {proj.template_title}
                  </h3>
                  <span
                    className={`text-xs px-2 py-1 rounded-full ${
                      proj.status === "GRADED"
                        ? "bg-green-100 text-green-700"
                        : "bg-yellow-100 text-yellow-700"
                    }`}
                  >
                    {proj.status}
                  </span>
                </div>
                <button
                  onClick={() => navigate(`/projects/${proj.id}`)}
                  className="text-blue-600 font-semibold text-sm hover:underline"
                >
                  Continue &rarr;
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* SECTION 2: AVAILABLE TEMPLATES */}
      <div>
        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <FolderPlus className="text-purple-600" /> Start a New Project
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {templates.map((tpl) => (
            <div
              key={tpl.id}
              className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition"
            >
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-bold text-gray-800">{tpl.title}</h3>
                <span className="text-[10px] uppercase font-bold bg-gray-100 text-gray-500 px-2 py-1 rounded">
                  {tpl.difficulty}
                </span>
              </div>
              <p className="text-sm text-gray-500 mb-6 h-10 line-clamp-2">
                {tpl.description}
              </p>
              <button
                onClick={() => handleStart(tpl.id)}
                className="w-full py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition text-sm font-medium"
              >
                Initialize Project
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProjectList;
