// src/pages/Login.tsx
import { useState } from "react";
import { Button, message } from "antd";
import { useNavigate } from "@tanstack/react-router";
import { motion } from "framer-motion";
import axios from "axios";
import { PageTransition } from "../components/PageTransition";

export function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(
        "http://localhost:8000/login/", // full URL to your Django backend
        form, // send JSON
        {
          headers: { "Content-Type": "application/json" },
          withCredentials: true, // important if using session cookies
        }
      );

      const data = response.data;

      if (data.status === "success") {
        message.success(`Logged in as ${data.user_type}`);

        // Redirect to the correct dashboard
        switch (data.user_type) {
          case "admin":
            navigate("/admin");
            break;
          case "university":
            navigate("/university");
            break;
          case "instructor":
            navigate("/instructor");
            break;
          default:
            message.error("Unknown user type");
        }
      } else {
        message.error(data.message || "Login failed");
      }
    } catch (error: any) {
      console.error(error);
      message.error(
        error.response?.data?.message ||
          "Login failed: server error"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <PageTransition>
      <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <motion.div
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.22 }}
          className="w-full max-w-md bg-white rounded-2xl p-10 flex flex-col border border-gray-200 shadow-lg"
        >
          {/* Title */}
          <h1 className="text-4xl font-semibold text-center text-gray-900 mb-10 tracking-tight">
            Login
          </h1>

          <form className="flex flex-col" onSubmit={handleSubmit}>
            <input
              type="text"
              name="username"
              placeholder="Username or Email"
              value={form.username}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-xl bg-gray-100 border border-gray-200 text-gray-900 placeholder-gray-500 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-400/40 transition-all"
              required
            />
            <div className="h-5" />

            <input
              type="password"
              name="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-xl bg-gray-100 border border-gray-200 text-gray-900 placeholder-gray-500 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-400/40 transition-all"
              required
            />
            <div className="h-6" />

            <Button
              type="primary"
              htmlType="submit"
              block
              loading={loading}
              className="!h-12 !rounded-xl !text-lg !font-medium"
            >
              Login
            </Button>
          </form>

          <p className="text-center text-gray-600 mt-10">
            Don’t have an account?
            <a
              href="/signup"
              className="text-blue-600 font-medium hover:underline ml-1"
            >
              Create one
            </a>
          </p>
        </motion.div>
      </div>
    </PageTransition>
  );
}

export default Login;
