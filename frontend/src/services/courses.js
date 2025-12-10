import api from "./api";

// Get list of all courses
export const getCourses = async () => {
  const response = await api.get("/learn/catalog/");
  return response.data;
};

// Get single course details (modules + lessons)
export const getCourseDetail = async (id) => {
  const response = await api.get(`/learn/catalog/${id}/`);
  return response.data;
};
