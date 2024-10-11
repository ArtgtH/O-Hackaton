import API_URL from "@/config/api.ts";
import axios from "axios";
import { IResponseFile, IUploadFileDto } from "../types/api";

class mainService {
  async uploadFileTask(body: IUploadFileDto) {
    const form_data = new FormData();
    form_data.append("file", body.file, body.file.path);
    return axios.post<IResponseFile>(
      `${API_URL}api/tasks/file-task/`,
      form_data,
      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );
  }
}

export default new mainService();
