import api from "./api";

export const getSimulations = async () => {
  const response = await api.get("/labs/simulations/");
  return response.data;
};

export const startLabSession = async (simulationId) => {
  // This tells the backend "I want to start working on this lab"
  // It creates or retrieves a SandboxSession
  const response = await api.post(`/labs/simulations/${simulationId}/start/`);
  return response.data;
};

export const saveLabProgress = async (sessionId, code) => {
  const response = await api.post(`/labs/workspace/${sessionId}/save_code/`, {
    code: code,
  });
  return response.data;
};
