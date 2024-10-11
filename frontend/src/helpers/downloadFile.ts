import API_URL from "@/config/api";

export const downloadFile = async (url: string) => {
  try {
    const response = await fetch(API_URL + url);

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const blob = await response.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = url.split("/").pop() || "download";
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);
  } catch (error) {
    console.error("There has been a problem with your fetch operation:", error);
  }
};
