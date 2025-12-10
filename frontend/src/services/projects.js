import api from "./api";

export const getProjectTemplates = async () => {
  const response = await api.get("/projects/templates/");
  return response.data;
};

export const getMyProjects = async () => {
  const response = await api.get("/projects/my-projects/");
  return response.data;
};

export const startProject = async (templateId) => {
  const response = await api.post(
    `/projects/templates/${templateId}/initialize/`
  );
  return response.data;
};

export const submitProject = async (projectId, data) => {
  const response = await api.post(
    `/projects/my-projects/${projectId}/submit/`,
    data
  );
  return response.data;
};
