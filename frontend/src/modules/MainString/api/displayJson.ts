import API_URL from "@/config/api";

export const fetchFile = async (link: string) => {
  const data = await fetch(API_URL + link);
  return data.json();
};
