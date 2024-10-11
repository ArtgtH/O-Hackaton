import { useMutation } from "@tanstack/react-query";
import { IUploadFileDto } from "../types/api.ts";
import mainService from "./mainService.ts";

export const useUploadFile = () =>
  useMutation({
    mutationFn: (body: IUploadFileDto) => mainService.uploadFileTask(body),
  });
