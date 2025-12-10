import React, { useEffect, useState } from "react";
import { getSimulations } from "../../services/labs";
import { Beaker, ArrowRight, Code } from "lucide-react";
import { useNavigate } from "react-router-dom";

const LabList = () => {
  const [labs, setLabs] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLabs = async () => {
      try {
        const data = await getSimulations();
        setLabs(data);
      } catch (error) {
        console.error("Failed to fetch labs", error);
      } finally {
        setLoading(false);
      }
    };
    fetchLabs();
  }, []);

  if (loading) return <div className="p-8">Loading Simulations...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">Virtual Labs</h1>
        <p className="text-gray-500 mt-1">
          Interactive environments needed no hardware.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {labs.map((lab) => (
          <div
            key={lab.id}
            className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:border-blue-200 transition-all group"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="p-3 bg-indigo-50 text-indigo-600 rounded-lg group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                <Beaker size={24} />
              </div>
              <span className="text-xs font-bold px-2 py-1 bg-gray-100 text-gray-600 rounded">
                {lab.lab_type}
              </span>
            </div>

            <h3 className="text-xl font-bold text-gray-800 mb-2">
              {lab.title}
            </h3>
            <p className="text-sm text-gray-500 mb-6">{lab.description}</p>

            <button
              onClick={() => navigate(`/labs/${lab.id}`)}
              className="w-full flex items-center justify-center gap-2 bg-slate-900 text-white py-2 rounded-lg hover:bg-slate-800 transition"
            >
              Enter Lab <ArrowRight size={16} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LabList;
