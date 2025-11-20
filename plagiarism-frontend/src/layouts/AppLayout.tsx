// AppLayout.tsx
import { Layout } from "antd";
import { Outlet, useRouterState } from "@tanstack/react-router";
import { AnimatePresence, motion } from "framer-motion";
import "../style.css";

const { Content } = Layout;

export function AppLayout() {
  const { location } = useRouterState();

  return (
    <Layout className="app-layout">
      <Content className="page-content" style={{ position: "relative", overflow: "hidden" }}>
        <AnimatePresence mode="wait">
          <motion.div
            key={location.key}        // <-- IMPORTANT FIX
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.22, ease: "easeOut" }}
            style={{ width: "100%", height: "100%" }}
          >
            <Outlet />
          </motion.div>
        </AnimatePresence>
      </Content>
    </Layout>
  );
}
