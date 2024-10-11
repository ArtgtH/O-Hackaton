import { useMutation } from "@tanstack/react-query";
import { IUploadStringDto } from "../types/api.ts";
import mainService from "./mainService.ts";

export const useUploadString = () =>
  useMutation({
    mutationFn: (body: IUploadStringDto) => mainService.uploadStringTask(body),
  });
