// src/pages/admin/AdminDashboard.tsx
import React, { useEffect, useState } from "react";
import { PageTransition } from "../components/PageTransition";
import { motion } from "framer-motion";
import { Card, Statistic, List, Skeleton, Empty, message } from "antd";
import { Link } from "@tanstack/react-router";

type InstructorActivity = {
  id: number;
  checking_document_name?: string;
  instructor_id__first_name?: string;
  instructor_id__last_name?: string;
  created_at?: string;
};

type UniversityActivity = {
  id: number;
  university_id__university_name?: string;
  research_document_name?: string;
  created_at?: string;
};

type Report = {
  id: number;
  checking_document_name?: string;
  uploaded_by_id?: number;
  created_at?: string;
  status?: string;
};

export function AdminDashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalUniversities, setTotalUniversities] = useState<number>(0);
  const [totalInstructors, setTotalInstructors] = useState<number>(0);
  const [totalDocumentsProcessed, setTotalDocumentsProcessed] = useState<number>(0);
  const [latestReports, setLatestReports] = useState<Report[]>([]);
  const [latestInstructorActivities, setLatestInstructorActivities] = useState<InstructorActivity[]>([]);
  const [latestUniversityActivities, setLatestUniversityActivities] = useState<UniversityActivity[]>([]);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError(null);

      try {
        // <-- FULL Django backend URL -->
        const res = await fetch("http://localhost:8000/administrator/panel/", {
          method: "GET",
          credentials: "include", // Send cookies/session
          headers: {
            "Accept": "application/json",
          },
        });

        if (!res.ok) {
          const body = await res.json().catch(() => ({}));
          throw new Error(body?.error || `Request failed with status ${res.status}`);
        }

        const data = await res.json();

        setTotalUniversities(data.total_universities ?? 0);
        setTotalInstructors(data.total_instructors ?? 0);
        setTotalDocumentsProcessed(data.total_documents_processed ?? 0);
        setLatestReports(Array.isArray(data.latest_reports) ? data.latest_reports : []);
        setLatestInstructorActivities(Array.isArray(data.latest_instructor_activities) ? data.latest_instructor_activities : []);
        setLatestUniversityActivities(Array.isArray(data.latest_university_activities) ? data.latest_university_activities : []);
      } catch (err: any) {
        console.error("Admin dashboard fetch error:", err);
        setError(err.message || "Failed to load admin dashboard");
        message.error(err.message || "Failed to load admin dashboard");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  const timeSince = (iso?: string) => {
    if (!iso) return "";
    try {
      const d = new Date(iso);
      const diff = Date.now() - d.getTime();
      const mins = Math.floor(diff / 60000);
      if (mins < 1) return "just now";
      if (mins < 60) return `${mins}m`;
      const hours = Math.floor(mins / 60);
      if (hours < 24) return `${hours}h`;
      const days = Math.floor(hours / 24);
      return `${days}d`;
    } catch {
      return "";
    }
  };

  return (
    <PageTransition>
      <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 p-4">
        {/* HEADER */}
        <header className="flex items-center justify-between px-4 py-3 bg-white border-b rounded-xl shadow-sm mb-6">
          <div className="flex items-center gap-4">
            <h2 className="text-xl font-semibold text-slate-700">Plagiarism Detection</h2>
            <span className="text-sm text-slate-500">Admin Dashboard</span>
          </div>

          <div className="flex items-center gap-3">
            <Link to="/administrator/account/" className="flex items-center justify-center w-9 h-9 rounded-full bg-slate-200 text-slate-700 font-semibold hover:bg-slate-300 transition">
              A
            </Link>
          </div>
        </header>

        {/* MAIN GRID */}
        <main className="grid grid-cols-12 gap-4 flex-1">

          {/* LEFT COLUMN */}
          <section className="col-span-3 grid grid-rows-2 gap-4">
            <Card className="rounded-xl border p-3 bg-white shadow-sm">
              <h3 className="text-base font-semibold text-slate-700 mb-2">
                <Link to="/administrator/universities/" className="hover:text-blue-600">Universities</Link>
              </h3>

              {loading ? (
                <Skeleton active paragraph={{ rows: 3 }} />
              ) : (
                <div className="flex flex-col gap-2 overflow-y-auto max-h-60">
                  <div className="text-sm text-slate-500">See all universities →</div>
                  <List
                    size="small"
                    dataSource={[]}
                    renderItem={() => null}
                  />
                </div>
              )}
            </Card>

            <Card className="rounded-xl border p-3 bg-white shadow-sm">
              <h3 className="text-base font-semibold text-slate-700 mb-2">
                <Link to="/administrator/pending/" className="hover:text-yellow-600">Pending Approval</Link>
              </h3>

              {loading ? (
                <Skeleton active paragraph={{ rows: 3 }} />
              ) : (
                <div className="flex flex-col gap-2 overflow-y-auto max-h-60">
                  <div className="text-sm text-slate-500">Open pending list →</div>
                </div>
              )}
            </Card>
          </section>

          {/* CENTER: Latest Reports */}
          <section className="col-span-4 bg-white rounded-xl border p-3 flex flex-col max-h-[700px]">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-base font-semibold text-slate-700">
                <Link to="/administrator/reports/" className="hover:text-blue-600">Latest Reports</Link>
              </h3>
              <div className="text-sm text-slate-400">Recent</div>
            </div>

            <div className="flex-1 overflow-y-auto">
              {loading ? (
                <Skeleton active paragraph={{ rows: 6 }} />
              ) : latestReports.length === 0 ? (
                <Empty description="No reports" />
              ) : (
                <List
                  dataSource={latestReports}
                  renderItem={(r: Report) => (
                    <List.Item className="p-3 bg-slate-50 rounded-lg border hover:bg-slate-100 transition mb-2">
                      <div className="w-full">
                        <div className="flex justify-between items-start">
                          <div>
                            <div className="text-sm text-slate-600">
                              {r.checking_document_name ?? "Report"}
                            </div>
                            <div className="text-xs text-slate-400 mt-1">
                              {r.created_at ? timeSince(r.created_at) : ""}
                            </div>
                          </div>

                          <div className="text-right">
                            <div className="text-sm text-blue-600 font-semibold">
                              {r.status ?? "Unknown"}
                            </div>
                          </div>
                        </div>
                      </div>
                    </List.Item>
                  )}
                />
              )}
            </div>
          </section>

          {/* RIGHT: Activities */}
          <section className="col-span-5 bg-white rounded-xl border p-3 flex flex-col max-h-[700px]">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-base font-semibold text-slate-700">
                <Link to="/administrator/activities/" className="hover:text-blue-600">Latest Activities</Link>
              </h3>
              <div className="text-sm text-slate-400">Live</div>
            </div>

            <div className="flex-1 overflow-y-auto space-y-3">
              {loading ? (
                <Skeleton active paragraph={{ rows: 6 }} />
              ) : (
                <>
                  {latestInstructorActivities.length === 0 && latestUniversityActivities.length === 0 && (
                    <Empty description="No recent activity" />
                  )}

                  {latestInstructorActivities.map((act) => (
                    <div key={`i-${act.id}`} className="p-3 bg-slate-50 rounded-lg border hover:bg-slate-100 transition text-sm">
                      <p className="text-xs text-slate-500"><strong>{timeSince(act.created_at)}</strong></p>
                      <p className="mt-1">
                        Instructor <strong>{`${act.instructor_id__first_name ?? ""} ${act.instructor_id__last_name ?? ""}`.trim()}</strong>
                        {act.checking_document_name ? ` uploaded ${act.checking_document_name}` : " uploaded a document."}
                      </p>
                    </div>
                  ))}

                  {latestUniversityActivities.map((act) => (
                    <div key={`u-${act.id}`} className="p-3 bg-blue-50 border border-blue-300 rounded-lg hover:bg-blue-100 transition text-sm">
                      <p><strong>{act.university_id__university_name}</strong></p>
                      <p className="text-xs mt-1 text-blue-900">{act.research_document_name ?? "Submitted repository"}</p>
                    </div>
                  ))}
                </>
              )}
            </div>
          </section>

          {/* BOTTOM: System Overview */}
          <section className="col-span-12 bg-white rounded-xl border p-4 flex flex-col">
            <h3 className="text-lg font-semibold text-slate-700 mb-3">System Overview</h3>

            <div className="grid grid-cols-3 gap-4">
              <Card className="bg-slate-50 border rounded-xl p-4 flex flex-col items-center">
                <p className="text-sm text-slate-500">Total Universities</p>
                <Statistic title={null} value={loading ? <Skeleton active paragraph={false} /> : totalUniversities} />
              </Card>

              <Card className="bg-slate-50 border rounded-xl p-4 flex flex-col items-center">
                <p className="text-sm text-slate-500">Total Instructors</p>
                <Statistic title={null} value={loading ? <Skeleton active paragraph={false} /> : totalInstructors} />
              </Card>

              <Card className="bg-slate-50 border rounded-xl p-4 flex flex-col items-center">
                <p className="text-sm text-slate-500">Documents Processed</p>
                <Statistic title={null} value={loading ? <Skeleton active paragraph={false} /> : totalDocumentsProcessed} />
              </Card>
            </div>
          </section>

        </main>
      </div>
    </PageTransition>
  );
}

export default AdminDashboard;
