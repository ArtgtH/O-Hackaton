import API_URL from "@/config/api.ts";
import axios from "axios";
import { IResponseString, IUploadStringDto } from "../types/api";

class mainService {
  async uploadStringTask(body: IUploadStringDto) {
    return axios.post<IResponseString>(`${API_URL}api/tasks/str-task/`, body, {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });
  }
}

export default new mainService();
