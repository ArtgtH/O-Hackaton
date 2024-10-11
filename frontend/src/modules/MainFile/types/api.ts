import { File } from "./file";

export interface IUploadFileDto {
  file: File;
}

export interface IResponseFile {
  result: string;
  result_csv: string;
  accuracy: string;
}
