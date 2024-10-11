import Sidebar from "@/modules/Sidebar";
import { ReactNode, useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface Props {
  children: ReactNode;
}

function Layout({ children }: Props) {
  const token = localStorage.getItem("token");
  const navigate = useNavigate();
  useEffect(() => {
    if (!token) navigate("/login");
  }, [navigate, token]);

  return (
    <div className="flex gap-6 max-w-[100vw] overflow-x-hidden bg-black">
      <Sidebar />
      <div className="lg:ml-80 w-full bg-black p-6 md:py-6 md:px-12 min-h-[100vh]">
        <div className="w-full h-full">{children}</div>
      </div>
    </div>
  );
}

export default Layout;
