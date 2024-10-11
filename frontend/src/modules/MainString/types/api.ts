import { File } from "./file";

export interface IUploadFileDto {
  file: File;
}
export interface IUploadStringDto {
  data: string;
}

export interface IResponseFile {
  result: string;
}
export interface IResponseString {
  result: string;
  result_csv: string;
  accuracy: string;
}

export interface IJSONResponse {
  data: {
    [key in string]: { [key in string]: number }[];
  };
}
