import { toast } from "react-toastify";

const API_URL = "http://localhost:5000/login"; // URL da sua API Flask

// 🔐 Login real na API
export const loginUser = async (email, senha) => {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, senha }),
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("user", JSON.stringify({
        token: data.token,
        email: data.email,
        role: data.role,
        username: data.username,
        id: data.id
      }));

      toast.success("Login realizado com sucesso!");
      return data;
    } else {
      toast.error(data.error || "Email ou senha incorretos!");
      return null;
    }
  } catch (error) {
    toast.error("Erro de rede ao tentar fazer login.");
    console.error(error);
    return null;
  }
};

// ✅ Recupera usuário autenticado do localStorage
export const getAuthenticatedUser = () => {
  const userData = localStorage.getItem("user");
  return userData ? JSON.parse(userData) : null;
};

// 🚪 Faz logout removendo os dados do localStorage
export const logoutUser = () => {
  localStorage.removeItem("user");
};

// 🔐 Envia headers com Authorization para outras chamadas autenticadas
export const authHeaders = () => {
  const user = getAuthenticatedUser();
  return user
    ? { Authorization: `Bearer ${user.token}`, "Content-Type": "application/json" }
    : { "Content-Type": "application/json" };
};
