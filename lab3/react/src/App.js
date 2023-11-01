import React from 'react';
import LoginView from './views/LoginView';
import RegisterView from './views/RegisterView';
import UsersView from './views/UsersView';
import './css/bootstrap.min.css';
import { Route, Routes, useNavigate } from "react-router-dom";

export default function App() {
  const navigate = useNavigate();
    return (
      <Routes>
        <Route path="/" element={<LoginView navigate={navigate}/>} />
        <Route path="/register" element={<RegisterView navigate={navigate}/>} />
        <Route path="/users" element={<UsersView/>} />
      </Routes>
    );
}