import React from "react";
import { useAuth } from "../../context/AuthContext";
import StudentDashboard from "./StudentDashboard";
import TeacherDashboard from "./TeacherDashboard";

const DashboardHome = () => {
  const { user } = useAuth();

  // Guard clause if user data isn't loaded yet
  if (!user) return null;

  // LOGIC SWITCH
  // Check the 'role' field we defined in the backend User model
  if (
    user.role === "TEACHER" ||
    user.role === "SCHOOL_ADMIN" ||
    user.is_staff
  ) {
    return <TeacherDashboard user={user} />;
  }

  // Default to Student View
  return <StudentDashboard user={user} />;
};

export default DashboardHome;
