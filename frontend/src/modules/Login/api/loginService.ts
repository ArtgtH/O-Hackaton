import API_URL from "@/config/api.ts";
import LoginDto from "@/modules/Login/types/login.dto.ts";
import axios from "axios";
import { IExist, ILogin } from "../types/responses";

class loginService {
  async login(body: LoginDto) {
    return axios.post<ILogin>(`${API_URL}login/`, body);
  }
  async registration(body: LoginDto) {
    return axios.post<void>(`${API_URL}register/`, body);
  }
  async isExist(email: string) {
    return axios.post<IExist>(`${API_URL}user-check/`, {
      email,
    });
  }
}

export default new loginService();
