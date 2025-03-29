export const loginUser = async (email, password) => {
  const response = await fetch('http://localhost:5000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email,
      senha: password,
    }),
  });

  const data = await response.json();

  if (response.ok) {
    // Armazena o token JWT no localStorage
    localStorage.setItem('token', data.token);
    return data; // Retorna o token ou dados do usuário, se necessário
  } else {
    // Caso haja erro
    return { error: data.error || 'Erro ao autenticar.' };
  }
};

export const getAuthenticatedUser = () => {
  const token = localStorage.getItem('token');
  if (token) {
    // Pode-se decodificar o token JWT aqui se necessário
    return JSON.parse(localStorage.getItem('user')); // Retorna o usuário ou dados do token
  }
  return null;
};

export const logoutUser = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};
