import React from "react";
import ReactDOM from "react-dom/client";
import { router } from "./router";
import { ViewTransitionRouter } from "./components/ViewTransitionRouter";

import "antd/dist/reset.css";
import "./style.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ViewTransitionRouter router={router} />
  </React.StrictMode>
);