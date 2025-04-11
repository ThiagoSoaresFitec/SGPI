import React, { useState, useEffect } from "react";
import { Container, TextField, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { getAuthenticatedUser } from "./auth"; // Importa o usuário logado

const PatentForm = () => {
  const navigate = useNavigate();
  const [titulo, setTitulo] = useState("");
  const [numero, setNumero] = useState("");
  const [observacao, setObservacao] = useState("");
  const [usuario, setUsuario] = useState(localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")).username : "");
  const [dataHoraAbertura, setDataHoraAbertura] = useState("");

  // Obtém usuário logado e define a data/hora automaticamente
  useEffect(() => {
    const user = getAuthenticatedUser();
    if (user) {
      setUsuario(user.username);
    }
    setDataHoraAbertura(new Date().toLocaleString());
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (titulo && numero) {
      const newPatent = {
        id: Date.now(),
        titulo,
        numero,
        dataHoraAbertura,
        usuario,
        observacao,
        status: 0
      };

      const storedPatents = JSON.parse(localStorage.getItem("patents")) || [];
      storedPatents.push(newPatent);
      localStorage.setItem("patents", JSON.stringify(storedPatents));

      navigate("/patents");
    }
  };

  return (
    <Container>
      <Button variant="outlined" color="secondary" onClick={() => navigate(-1)} style={{ marginBottom: "20px" }}>
        Voltar
      </Button>
      <Typography variant="h4">Cadastro de Patente</Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Título da Patente"
          fullWidth
          margin="normal"
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
          required
        />
        <TextField
          label="Número do Pedido"
          fullWidth
          margin="normal"
          value={numero}
          onChange={(e) => setNumero(e.target.value)}
          required
        />
        <TextField
          label="Data e Hora da Abertura"
          fullWidth
          margin="normal"
          value={dataHoraAbertura}
          disabled
        />
        <TextField
          label="Usuário"
          fullWidth
          margin="normal"
          value={usuario}
          disabled
        />
        <TextField
          label="Observação"
          fullWidth
          margin="normal"
          multiline
          rows={3}
          value={observacao}
          onChange={(e) => setObservacao(e.target.value)}
        />
        <Button variant="contained" color="primary" type="submit" fullWidth sx={{ mt: 2 }}>
          Cadastrar
        </Button>
      </form>
    </Container>
  );
};

export default PatentForm;
