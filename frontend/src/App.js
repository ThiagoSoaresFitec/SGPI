import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"; // Importa o CSS

import Login from "./components/Login";
import PatentForm from "./components/PatentForm";
import PatentList from "./components/PatentList";
import PrivateRoute from "./components/PrivateRoute";
import Register from "./components/Register";
import Layout from "./components/Layout";
import PatentDashboard from "./components/PatentDashboard";

const App = () => {
  return (
    <Router>
      <ToastContainer position="top-right" autoClose={3000} />
      <Routes>
        {/* Página inicial de login */}
        <Route path="/" element={<Login />} />

        {/* Rotas protegidas para Administrador */}
        <Route element={<PrivateRoute allowedRoles={["Administrador"]} />}>
          <Route path="/administrador" element={<Navigate to="/patents" />} />
          <Route path="/register" element={<Layout><Register /></Layout>} />
          <Route path="/dashboard" element={<Layout><PatentDashboard /></Layout>} />
          <Route path="/patents" element={<Layout><PatentList /></Layout>} />
          <Route path="/patent/new" element={<Layout><PatentForm /></Layout>} />
        </Route>

        {/* Rotas protegidas para Pesquisador */}
        <Route element={<PrivateRoute allowedRoles={["Pesquisador"]} />}>
          <Route path="/pesquisador" element={<Navigate to="/patents" />} />
          <Route path="/patents" element={<Layout><PatentList /></Layout>} />
          <Route path="/patent/new" element={<Layout><PatentForm /></Layout>} />
          <Route path="/dashboard" element={<Layout><PatentDashboard /></Layout>} />
        </Route>

        {/* Rotas protegidas para Engenheiro */}
        <Route element={<PrivateRoute allowedRoles={["Engenheiro"]} />}>
          <Route path="/engenheiro" element={<Navigate to="/patents" />} />
          <Route path="/patents" element={<Layout><PatentList /></Layout>} />
          <Route path="/patent/new" element={<Layout><PatentForm /></Layout>} />
          <Route path="/dashboard" element={<Layout><PatentDashboard /></Layout>} />
        </Route>

        {/* Página de acesso negado */}
        <Route path="/unauthorized" element={<h1>Acesso Negado</h1>} />
      </Routes>
    </Router>
  );
};

export default App;
