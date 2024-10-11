import Typography from "@/ui/Typography.tsx";
import { useNavigate } from "react-router-dom";

const UserInfo = () => {
  const navigate = useNavigate();

  const handleLeave = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="flex flex-col gap-4 px-4 py-4">
      <Typography variant="h3" className="flex gap-2 text-lime-300">
        ОСТРОВОК ХАКАТОН
      </Typography>

      <div className="flex  gap-2 justify-between text-gray-100 w-full pt-4">
        <Typography variant="paragraph" className="flex gap-2 text-gray-100">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="size-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z"
            />
          </svg>
          Гость
        </Typography>
        <button
          className="hover:text-main-red transition"
          onClick={handleLeave}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="size-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15"
            />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default UserInfo;
