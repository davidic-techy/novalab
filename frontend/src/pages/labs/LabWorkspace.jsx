import React, { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { startLabSession, saveLabProgress } from "../../services/labs";
import {
  Play,
  Save,
  Terminal,
  ArrowLeft,
  Loader,
  RefreshCw,
} from "lucide-react";

const LabWorkspace = () => {
  const { labId } = useParams();
  const navigate = useNavigate();

  // UI State
  const [session, setSession] = useState(null);
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("Initializing Environment...\n");
  const [isReady, setIsReady] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [saving, setSaving] = useState(false);

  const pyodideRef = useRef(null);

  // 1. Initialization (Session + Python Engine)
  useEffect(() => {
    const init = async () => {
      try {
        // A. Load Session Data from Backend
        const data = await startLabSession(labId);
        setSession(data);
        setCode(data.code_snapshot || "print('Hello World')");

        // B. Wait for Pyodide Script (from index.html)
        if (!window.loadPyodide) {
          setOutput((prev) => prev + "> Error: Pyodide script not loaded.\n");
          return;
        }

        // C. Boot Python Engine
        setOutput((prev) => prev + "> Booting Python 3.11 Kernel...\n");

        const pyodide = await window.loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/",
        });

        // D. Configure Output Capture
        await pyodide.runPythonAsync(`
            import sys
            import io
            sys.stdout = io.StringIO()
        `);

        pyodideRef.current = pyodide;
        setIsReady(true);
        setOutput((prev) => prev + "> Ready! 🚀\n");
      } catch (err) {
        setOutput((prev) => prev + `❌ Initialization Error: ${err.message}\n`);
      }
    };

    init();
  }, [labId]);

  // 2. Run Code
  const handleRun = async () => {
    if (!pyodideRef.current) return;

    setIsRunning(true);
    setOutput((prev) => prev + `\n> Running...\n`);

    try {
      // Clear Python stdout buffer
      pyodideRef.current.runPython("sys.stdout = io.StringIO()");

      // Execute User Code
      await pyodideRef.current.runPythonAsync(code);

      // Capture and Display Output
      const stdout = pyodideRef.current.runPython("sys.stdout.getvalue()");
      setOutput((prev) => prev + stdout);
    } catch (err) {
      setOutput((prev) => prev + `⚠️ Error:\n${err.message}`);
    } finally {
      setIsRunning(false);
    }
  };

  // 3. Save Progress
  const handleSave = async () => {
    setSaving(true);
    try {
      await saveLabProgress(session.id, code);
      // alert("Saved!"); // Optional: generic alert
    } catch (err) {
      console.error("Save failed", err);
    } finally {
      setSaving(false);
    }
  };

  if (!session)
    return (
      <div className="h-screen bg-slate-900 text-white flex items-center justify-center">
        Loading Lab...
      </div>
    );

  return (
    <div className="h-screen flex flex-col bg-slate-900 text-white font-mono">
      {/* --- HEADER --- */}
      <div className="bg-slate-800 h-14 border-b border-slate-700 flex justify-between items-center px-4">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate("/labs")}
            className="text-slate-400 hover:text-white transition"
          >
            <ArrowLeft size={18} />
          </button>
          <div>
            <h1 className="font-bold text-sm text-slate-200">
              {session.simulation_title}
            </h1>
            <div className="flex items-center gap-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  isReady ? "bg-green-500" : "bg-yellow-500 animate-pulse"
                }`}
              ></div>
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">
                {isReady ? "Online" : "Booting"}
              </span>
            </div>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium bg-slate-700 hover:bg-slate-600 rounded transition text-slate-300"
          >
            {saving ? (
              <RefreshCw size={14} className="animate-spin" />
            ) : (
              <Save size={14} />
            )}
            {saving ? "Saving..." : "Save"}
          </button>

          <button
            onClick={handleRun}
            disabled={!isReady || isRunning}
            className={`flex items-center gap-2 px-4 py-1.5 text-xs font-bold text-white rounded transition shadow-lg 
                ${
                  !isReady || isRunning
                    ? "bg-slate-600 opacity-50 cursor-not-allowed"
                    : "bg-green-600 hover:bg-green-700 shadow-green-900/20"
                }
            `}
          >
            {isRunning ? (
              <Loader size={14} className="animate-spin" />
            ) : (
              <Play size={14} />
            )}
            Run Code
          </button>
        </div>
      </div>

      {/* --- SPLIT PANE WORKSPACE --- */}
      <div className="flex-1 flex overflow-hidden">
        {/* Editor */}
        <div className="w-1/2 flex flex-col border-r border-slate-700">
          <div className="bg-slate-950 px-4 py-2 text-xs text-slate-500 border-b border-slate-800">
            main.py
          </div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="flex-1 bg-slate-900 p-4 text-blue-300 outline-none resize-none leading-relaxed text-sm font-mono"
            spellCheck="false"
            placeholder="# Write your Python code here..."
          />
        </div>

        {/* Console */}
        <div className="w-1/2 flex flex-col bg-black">
          <div className="bg-slate-950 px-4 py-2 text-xs text-slate-500 border-b border-slate-800 flex justify-between items-center">
            <div className="flex items-center gap-2">
              <Terminal size={12} /> Console Output
            </div>
            <button onClick={() => setOutput("")} className="hover:text-white">
              Clear
            </button>
          </div>
          <div className="flex-1 p-4 text-green-400 overflow-auto whitespace-pre-wrap text-sm">
            {output}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LabWorkspace;
