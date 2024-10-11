import Typography from "@/ui/Typography";
import { UploadFile } from "./ui/UploadFile";

export const MainFile = () => {
  return (
    <div className="flex flex-col gap-10 my-20 px-10 mx-auto">
      <Typography variant="h3" className="flex gap-2 text-lime-300">
        Загрузите файл!
      </Typography>

      <UploadFile />
    </div>
  );
};
