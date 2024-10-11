import LoginPage from "@/pages/LoginPage.tsx";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import AboutPage from "./pages/AboutPage.tsx";
import FilePage from "./pages/FilePage.tsx";
import StringPage from "./pages/StringPage.tsx";
import Error from "./ui/Error.tsx";
import Layout from "./ui/Layout.tsx";

const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
    errorElement: <Error />,
  },

  {
    path: "/",
    element: (
      <Layout>
        <StringPage />
      </Layout>
    ),
    errorElement: <Error />,
  },
  {
    path: "/file",
    element: (
      <Layout>
        <FilePage />
      </Layout>
    ),
    errorElement: <Error />,
  },
  {
    path: "/about",
    element: (
      <Layout>
        <AboutPage />
      </Layout>
    ),
    errorElement: <Error />,
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
