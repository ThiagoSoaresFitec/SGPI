import React, { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
} from "@mui/material";
import { loginUser } from "./auth";
import logo from "../assets/logo.png";
import backgroundImage from "../assets/copia2.png";
const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const handleLogin = () => {
    const user = loginUser(email, password);
    if (user) {
      console.log("================>".user);
      navigate(`/${user.role}`);
    } else {
      setError("Usuário ou senha incorretos.");
    }
  };
  return (
    <Box
      sx={{
        minHeight: "100vh",
        width: "100vw",
        position: "relative",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <Card
        sx={{
          p: 5,
          minWidth: 340,
          borderRadius: 4,
          boxShadow: 6,
          backgroundColor: "rgba(255, 255, 255, 0.95)",
          backdropFilter: "blur(6px)",
        }}
      >
        <CardContent
          component="form"
          onSubmit={(e) => {
            e.preventDefault();
            handleLogin();
          }}
        >
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0.7, 1] }}
            transition={{
              duration: 2,
              repeat: Infinity,
              repeatType: "reverse",
            }}
          >
            <Typography
              variant="h4"
              align="center"
              gutterBottom
              color="primary"
              sx={{
                fontWeight: "bold",
                letterSpacing: 2,
              }}
            >
              SGPI
            </Typography>
          </motion.div>

          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: 120,
              height: 120,
              backgroundColor: "#007B8F",
              borderRadius: "50%",
              margin: "0 auto 24px",
              boxShadow: "0 6px 12px rgba(0,0,0,0.2)",
            }}
          >
            <img src={logo} alt="SGPI Logo" style={{ width: 70 }} />
          </Box>

          <TextField
            fullWidth
            label="Email"
            variant="outlined"
            margin="normal"
            value={email}
            type="email"
            onChange={(e) => setEmail(e.target.value)}
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                '&:hover fieldset': {
                  borderColor: '#007B8F',
                },
                '&.Mui-focused fieldset': {
                  borderColor: '#007B8F',
                },
              },
            }}
          />

          <TextField
            fullWidth
            label="Senha"
            type="password"
            variant="outlined"
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                '&:hover fieldset': {
                  borderColor: '#007B8F',
                },
                '&.Mui-focused fieldset': {
                  borderColor: '#007B8F',
                },
              },
            }}
          />

          {error && (
            <Typography color="error" sx={{ mt: 1 }}>
              {error}
            </Typography>
          )}

          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            sx={{ mt: 3, borderRadius: 2, py: 1.5, fontWeight: 'bold' }}
          >
            Entrar
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
};
export default Login;