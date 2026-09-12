import { createBrowserRouter } from "react-router";
import { Layout } from "./components/Layout";
import { Home } from "./pages/Home";
import { Dashboards } from "./pages/Dashboards";
import { Insights } from "./pages/Insights";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: Home },
      { path: "dashboards", Component: Dashboards },
      { path: "insights", Component: Insights },
    ],
  },
]);
