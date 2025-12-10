import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./pages/auth/Login";
import DashboardHome from "./pages/dashboard/DashboardHome";
import Layout from "./components/layout/Layout";
import { useAuth } from "./context/AuthContext";

// Import Pages
import CourseList from "./pages/courses/CourseList";
import CourseViewer from "./pages/courses/CourseViewer";
import LabList from "./pages/labs/LabList";
import LabWorkspace from "./pages/labs/LabWorkspace";
import ProjectList from "./pages/projects/ProjectList";
import ProjectWorkspace from "./pages/projects/ProjectWorkspace";
import Achievements from "./pages/achievements/Achievements";
import SchoolAnalytics from "./pages/analytics/SchoolAnalytics";

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return <div className="p-10">Loading NovaLab...</div>;
  if (!user) return <Navigate to="/login" />;

  return children;
};

// Helper to wrap content in Layout
const LayoutWrapper = ({ children }) => <Layout>{children}</Layout>;

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* --- DASHBOARD --- */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <LayoutWrapper>
                <DashboardHome />
              </LayoutWrapper>
            </ProtectedRoute>
          }
        />

        {/* --- COURSES --- */}
        <Route
          path="/courses/:courseId"
          element={
            <ProtectedRoute>
              <CourseViewer />
            </ProtectedRoute>
          }
        />

        <Route
          path="/courses"
          element={
            <ProtectedRoute>
              <LayoutWrapper>
                <CourseList />
              </LayoutWrapper>
            </ProtectedRoute>
          }
        />

        {/* --- LABS --- */}
        <Route
          path="/labs/:labId"
          element={
            <ProtectedRoute>
              <LabWorkspace />
            </ProtectedRoute>
          }
        />

        <Route
          path="/labs"
          element={
            <ProtectedRoute>
              <LayoutWrapper>
                <LabList />
              </LayoutWrapper>
            </ProtectedRoute>
          }
        />

        {/* --- PROJECTS (The Fix) --- */}

        {/* 1. Project Workspace (Specific Project) */}
        <Route
          path="/projects/:projectId"
          element={
            <ProtectedRoute>
              <LayoutWrapper>
                <ProjectWorkspace />
              </LayoutWrapper>
            </ProtectedRoute>
          }
        />

        {/* 2. Project List (Main Page) */}
        <Route
          path="/projects"
          element={
            <ProtectedRoute>
              <LayoutWrapper>
                <ProjectList />
              </LayoutWrapper>
            </ProtectedRoute>
          }
        />

        {/* ACHIEVEMENTS */}
        <Route
          path="/achievements"
          element={
            <ProtectedRoute>
              <LayoutWrapper>
                <Achievements />
              </LayoutWrapper>
            </ProtectedRoute>
          }
        />
        {/* ANALYTICS */}
        <Route
          path="/analytics"
          element={
            <ProtectedRoute>
              <LayoutWrapper>
                <SchoolAnalytics />
              </LayoutWrapper>
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
