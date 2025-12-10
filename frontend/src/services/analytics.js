import api from "./api";

export const getDashboardStats = async () => {
  // Fetches the last 7 days of activity for the user's school
  const response = await api.get("/analytics/dashboard/");
  return response.data;
};

export const logEvent = async (eventType, metadata = {}) => {
  // Fire-and-forget event logger (useful for tracking clicks)
  try {
    await api.post("/analytics/events/", {
      event_type: eventType,
      metadata: metadata,
    });
  } catch (e) {
    console.error("Failed to log event", e);
  }
};

export const getStudentStats = async () => {
  const response = await api.get("/analytics/student-stats/");
  return response.data;
};

export const getSchoolStats = async () => {
  const response = await api.get("/analytics/school-stats/");
  return response.data;
};
