import { useState } from "react";
import { Button, Input, Upload, message } from "antd";
import { motion } from "framer-motion";
import { UploadOutlined } from "@ant-design/icons";
import { useNavigate } from "@tanstack/react-router";

export function UniversitySignUp() {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const getCookie = (name: string) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()!.split(";").shift();
    return "";
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !password || !file) {
      message.error("All fields are required!");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("university_name", name);
    formData.append("password", password);
    formData.append("university_certificate", file);

    try {
      const res = await fetch("http://localhost:8000/university/signup/", {
        method: "POST",
        body: formData,
        credentials: "include",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      });

      const data = await res.json();

      if (res.ok) {
        message.success(data.message || "University registered successfully!");

        setName("");
        setPassword("");
        setFile(null);

        setTimeout(() => navigate({ to: "/login" }), 1000);
      } else {
        message.error(data.error || "Something went wrong");
      }
    } catch (err) {
      message.error("Network error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-6 py-16">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="w-full max-w-md bg-white p-10 rounded-2xl border border-gray-200"
      >

        {/* 🔥 Stylish Apple-style Title */}
        <h1
          className="
            text-5xl md:text-6xl 
            font-bold 
            text-center 
            tracking-tight 
            mb-12 
            bg-gradient-to-b from-black to-gray-700 
            bg-clip-text 
            text-transparent
          "
        >
          Register Your University
        </h1>

        <form onSubmit={handleSubmit} className="flex flex-col">

          {/* University Name */}
          <Input
            placeholder="University Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="rounded-xl py-3 bg-gray-100 border border-gray-200 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-400/40 transition-all"
          />

          {/* spacing */}
          <div className="h-5" />

          {/* Password */}
          <Input.Password
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="rounded-xl py-3 bg-gray-100 border border-gray-200 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-400/40 transition-all"
          />

          {/* spacing */}
          <div className="h-5" />

          {/* Certificate Upload */}
          <Upload
            beforeUpload={(file) => {
              setFile(file);
              return false;
            }}
            maxCount={1}
            className="w-full"
          >
            <Button
              icon={<UploadOutlined />}
              className="w-full !h-12 !rounded-xl !text-base"
            >
              {file ? file.name : "Upload University Certificate"}
            </Button>
          </Upload>

          {/* spacing */}
          <div className="h-6" />

          {/* Submit Button */}
          <Button
            type="primary"
            htmlType="submit"
            size="large"
            loading={loading}
            className="!h-12 !rounded-xl !text-lg !font-medium"
          >
            {loading ? "Processing..." : "Submit for Approval"}
          </Button>
        </form>
      </motion.div>
    </div>
  );
}
