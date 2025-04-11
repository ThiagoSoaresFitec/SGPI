import React from "react";
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemText,
  Avatar,
  Button
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { getAuthenticatedUser, logoutUser } from "./auth";
import logo from "../assets/logo.png";


const drawerWidth = 240;

const Layout = ({ children }) => {
  const navigate = useNavigate();
  const user = getAuthenticatedUser();

  const handleLogout = () => {
    logoutUser();
    navigate("/");
  };

  const getMenuItems = () => {
    const commonItems = [
      { label: "Cadastrar Patente", path: "/patent/new" },
      { label: "Listar Patentes", path: "/patents" },
      { label: "Dashboard", path: "/dashboard" },
    ];

    if (user.role === "Administrador") {
      return [
        { label: "Cadastrar Usuários", path: "/register" },
        ...commonItems
      ];
    }

    return commonItems;
  };

  return (
    <Box sx={{ display: "flex", width: "100%", minHeight: "100vh" }}>
      <AppBar position="fixed" sx={{ zIndex: 1300, backgroundColor: "#007B8F" }}>
        <Toolbar>
          <Avatar src={logo} sx={{ mr: 2, width: 28, height: 40, p: 1 }} />
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Sistema de Gerenciamento de Patentes Industriais
          </Typography>
          <Button color="inherit" onClick={handleLogout}>Sair</Button>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
            backgroundColor: "#f5f5f5",
            borderRight: "1px solid #ddd",
            display: "flex",         // <-- importante!
            flexDirection: "column", // <-- importante!
          },
        }}
      >
        {/* Toolbar dentro do papel do Drawer */}
        <Toolbar />

        <List>
          {getMenuItems().map((item, index) => (
            <ListItem
              button
              key={index}
              onClick={() => navigate(item.path)}
              sx={{
                m: 1,
                borderRadius: 2,
                cursor: 'pointer',
                transition: 'all 0.2s ease-in-out',
                '&:hover': {
                  backgroundColor: '#e0f7fa',
                  transform: 'scale(1.02)',
                  boxShadow: '0 2px 6px rgba(0, 0, 0, 0.1)',
                },
              }}
            >
              <ListItemText
                primary={item.label}
                primaryTypographyProps={{
                  fontWeight: 500,
                  color: '#007B8F'
                }}
              />
            </ListItem>
          ))}
        </List>
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          padding: 3,
          width: `calc(100% - ${drawerWidth}px)`,
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>

  );
};

export default Layout;
