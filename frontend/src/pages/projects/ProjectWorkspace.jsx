import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getMyProjects, submitProject } from "../../services/projects";
import { FileCode, CheckCircle, ArrowLeft, Save } from "lucide-react";

const ProjectWorkspace = () => {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [activeFile, setActiveFile] = useState(null);

  // Local state to track edits before saving/submitting
  const [fileContent, setFileContent] = useState("");

  useEffect(() => {
    getMyProjects().then((projects) => {
      const found = projects.find((p) => p.id === projectId);
      if (found) {
        setProject(found);
        const files = Object.keys(found.artifact_data || {});
        if (files.length > 0) {
          setActiveFile(files[0]);
          setFileContent(found.artifact_data[files[0]]);
        }
      }
    });
  }, [projectId]);

  // When switching files, update the editor content
  const handleFileSwitch = (filename) => {
    // 1. Save current progress to local project state first
    if (activeFile) {
      // eslint-disable-next-line react-hooks/immutability
      project.artifact_data[activeFile] = fileContent;
    }

    // 2. Switch
    setActiveFile(filename);
    setFileContent(project.artifact_data[filename]);
  };

  // Update the temporary state as student types
  const handleCodeChange = (e) => {
    setFileContent(e.target.value);
    // Also update the main project object so it's ready to submit
    if (project && activeFile) {
      // eslint-disable-next-line react-hooks/immutability
      project.artifact_data[activeFile] = e.target.value;
    }
  };

  const handleSubmit = async () => {
    if (!window.confirm("Submit project for auto-grading?")) return;
    try {
      // Send the EDITED files to the backend
      await submitProject(projectId, { artifact_data: project.artifact_data });
      alert("Project Submitted!");
      navigate("/projects");
    } catch (e) {
      alert("Error submitting: " + e.message);
    }
  };

  if (!project) return <div className="p-8">Loading Project...</div>;

  return (
    <div className="h-[calc(100vh-64px)] flex flex-col">
      {/* Toolbar */}
      <div className="bg-white border-b border-gray-200 px-6 py-3 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate("/projects")}
            className="text-gray-500 hover:text-gray-800"
          >
            <ArrowLeft size={20} />
          </button>
          <div>
            <h1 className="font-bold text-gray-800">
              {project.template_title}
            </h1>
            <p className="text-xs text-gray-500">
              Edit the files to complete the assignment.
            </p>
          </div>
        </div>
        <div className="flex gap-3">
          <button
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 flex items-center gap-2"
            onClick={() => alert("Draft Saved locally!")}
          >
            <Save size={16} /> Save Draft
          </button>
          <button
            onClick={handleSubmit}
            className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-green-700 flex items-center gap-2"
          >
            <CheckCircle size={16} /> Submit for Grading
          </button>
        </div>
      </div>

      {/* Editor Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* File Tree */}
        <div className="w-64 bg-gray-50 border-r border-gray-200 p-4">
          <h3 className="text-xs font-bold text-gray-400 uppercase mb-4">
            Project Files
          </h3>
          <div className="space-y-1">
            {Object.keys(project.artifact_data).map((filename) => (
              <button
                key={filename}
                onClick={() => handleFileSwitch(filename)}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm flex items-center gap-2 ${
                  activeFile === filename
                    ? "bg-blue-100 text-blue-700 font-bold"
                    : "text-gray-600 hover:bg-gray-100"
                }`}
              >
                <FileCode size={16} /> {filename}
              </button>
            ))}
          </div>
        </div>

        {/* Code Editor (Editable Textarea) */}
        <div className="flex-1 flex flex-col bg-slate-900">
          <div className="bg-slate-950 px-4 py-2 text-xs text-slate-500 font-mono border-b border-slate-800">
            {activeFile}{" "}
            {project.status === "GRADED" ? "(Read Only)" : "(Editable)"}
          </div>
          <textarea
            value={fileContent}
            onChange={handleCodeChange}
            disabled={project.status === "GRADED"} // Lock if already graded
            className="flex-1 w-full bg-slate-900 p-6 text-sm font-mono text-blue-300 outline-none resize-none leading-relaxed"
            spellCheck="false"
          />
        </div>
      </div>
    </div>
  );
};

export default ProjectWorkspace;
