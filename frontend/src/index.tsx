import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import App from "./App";
import Dashboard from "./pages/Dashboard";
import Diet from "./pages/Diet";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Workout from "./pages/Workout";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/diet" element={<Diet />} />
        <Route path="/workout" element={<Workout />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
