import Typography from "@/ui/Typography";
import { UploadString } from "./ui/UploadString";

export const MainString = () => {
  return (
    <div className="flex flex-col gap-10 my-20 px-10 mx-auto">
      <Typography variant="h3" className="flex gap-2 text-lime-300">
        Введите описание
      </Typography>

      <UploadString />
    </div>
  );
};
