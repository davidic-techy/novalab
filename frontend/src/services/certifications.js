import api from "./api";

export const getMyBadges = async () => {
  const response = await api.get("/certifications/badges/");
  return response.data;
};

export const getMyCertificates = async () => {
  const response = await api.get("/certifications/certificates/");
  return response.data;
};

export const downloadCertificate = async (id, filename) => {
  const response = await api.get(
    `/certifications/certificates/${id}/download/`,
    {
      responseType: "blob", // Important for PDF
    }
  );

  // Create a temporary download link
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", filename || `certificate-${id}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};
