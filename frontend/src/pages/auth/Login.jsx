import React from "react";
import { GoogleLogin } from "@react-oauth/google"; // Official Button
import { useAuth } from "../../context/AuthContext";
import api from "../../services/api";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSuccess = async (credentialResponse) => {
    console.log("Google Responded:", credentialResponse);

    try {
      // 1. Send the Google Token to YOUR Django Backend
      const res = await api.post("/auth/google/", {
        token: credentialResponse.credential,
      });

      console.log("Django Responded:", res.data);

      // 2. Save the Django JWT Token (Login)
      login(res.data.user, res.data.access, res.data.refresh);

      // 3. Redirect to Dashboard
      navigate("/");
    } catch (error) {
      console.error("Backend Login Failed:", error);
      alert("Login failed! Check console for details.");
    }
  };

  const handleError = () => {
    console.error("Google Popup Failed");
    alert("Google Sign-In failed to open.");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-10 rounded-xl shadow-lg w-96 text-center">
        <h1 className="text-3xl font-bold mb-2 text-blue-600">NovaLab</h1>
        <p className="text-gray-500 mb-8">Future-Ready Learning</p>

        <div className="flex justify-center">
          <GoogleLogin
            onSuccess={handleSuccess}
            onError={handleError}
            theme="filled_blue"
            size="large"
            text="signin_with"
            shape="rectangular"
          />
        </div>

        <p className="mt-6 text-xs text-gray-400">
          By signing in, you agree to our Terms of Service.
        </p>
      </div>
    </div>
  );
};

export default Login;
