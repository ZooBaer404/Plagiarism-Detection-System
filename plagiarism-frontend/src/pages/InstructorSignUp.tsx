// src/pages/InstructorSignUp.tsx
import { useState, useEffect } from "react";
import { Button, Input, Select, Upload, message, Spin } from "antd";
import { motion } from "framer-motion";
import { UploadOutlined } from "@ant-design/icons";
import { useNavigate } from "@tanstack/react-router";
import "../style.css";

const { Option } = Select;

interface University {
  id: number;
  university_name: string;
}

export function InstructorSignUp() {
  const [universities, setUniversities] = useState<University[]>([]);
  const [loadingUniversities, setLoadingUniversities] = useState(true);

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [universityId, setUniversityId] = useState<number | null>(null);
  const [certificate, setCertificate] = useState<File | null>(null);
  const [field, setField] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  // CSRF cookie helper
  const getCookie = (name: string) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()!.split(";").shift();
    return "";
  };

  // Fetch universities on mount
  useEffect(() => {
    const fetchUniversities = async () => {
      try {
        const res = await fetch("http://localhost:8000/instructor/signup/", {
          credentials: "include",
        });
        if (!res.ok) throw new Error("Failed to fetch universities");
        const data = await res.json();
        setUniversities(data.universities);
      } catch (err) {
        console.error(err);
        message.error("Failed to load universities");
      } finally {
        setLoadingUniversities(false);
      }
    };
    fetchUniversities();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!firstName || !lastName || !email || !password || !universityId || !certificate || !field) {
      message.error("All fields are required!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("first_name", firstName);
    formData.append("last_name", lastName);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("university_id", universityId.toString());
    formData.append("certificate", certificate);
    formData.append("field", field);

    try {
      const res = await fetch("http://localhost:8000/instructor/signup/", {
        method: "POST",
        body: formData,
        credentials: "include",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      });

      const data = await res.json();
      if (res.ok) {
        message.success(data.message || "Instructor registered successfully!");
        setFirstName("");
        setLastName("");
        setEmail("");
        setPassword("");
        setUniversityId(null);
        setCertificate(null);
        setField("");
        setTimeout(() => navigate({ to: "/login" }), 1000);
      } else {
        message.error(data.error || "Something went wrong");
      }
    } catch (err) {
      console.error(err);
      message.error("Network error");
    } finally {
      setLoading(false);
    }
  };

  if (loadingUniversities) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spin size="large" tip="Loading universities..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-6 py-16">
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="w-full max-w-md bg-white p-8 rounded-xl shadow-lg"
      >
        <h1 className="text-4xl font-extrabold mb-6 text-center text-blue-600">Instructor Signup</h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Input placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
          <Input placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
          <Input placeholder="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <Input.Password placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <Select placeholder="Select University" value={universityId ?? undefined} onChange={(val) => setUniversityId(val)} required>
            {universities.map((u) => (
              <Option key={u.id} value={u.id}>
                {u.university_name}
              </Option>
            ))}
          </Select>
          <Upload beforeUpload={(file) => { setCertificate(file); return false; }} maxCount={1}>
            <Button icon={<UploadOutlined />}>
              {certificate ? certificate.name : "Upload Certificate (PDF / Image)"}
            </Button>
          </Upload>
          <Input placeholder="Field" value={field} onChange={(e) => setField(e.target.value)} required />
          <Button type="primary" htmlType="submit" size="large" loading={loading}>
            {loading ? "Processing..." : "Sign Up"}
          </Button>
        </form>
      </motion.div>
    </div>
  );
}
