import { RouterProvider, useRouterState } from "@tanstack/react-router";
import { AnimatePresence } from "framer-motion";
import type { Router } from "@tanstack/react-router";

export function ViewTransitionRouter({ router }: { router: Router }) {
  return (
    <RouterProvider
      router={router}
      defaultPreload="intent"
      context={{
        animatePresence: AnimatePresenceWrapper,
      }}
    />
  );
}

function AnimatePresenceWrapper({ children }: { children: React.ReactNode }) {
  const { location } = useRouterState();

  return (
    <AnimatePresence mode="wait">
      {/* key makes old page animate out and new animate in */}
      <div key={location.pathname}>{children}</div>
    </AnimatePresence>
  );
}
