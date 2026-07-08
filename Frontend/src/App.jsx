import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Signup from './pages/Signup';
import ForgotPassword from './pages/ForgotPassword';
import PatientDashboard from './pages/PatientDashboard';
import DoctorDashboard from './pages/DoctorDashboard';
import AboutUs from './pages/AboutUs';
import ContactUs from './pages/ContactUs';

// Protected Route wrapper component
function ProtectedRoute({ children, allowedRole }) {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  if (!token) {
    // If not logged in, redirect to login page
    return <Navigate to="/login" replace />;
  }

  if (allowedRole && role !== allowedRole) {
    // If logged in but role mismatch, redirect to correct portal
    return <Navigate to={role === 'doctor' ? '/doctor/dashboard' : '/patient/dashboard'} replace />;
  }

  return children;
}

// Public Route wrapper component (prevents logged in users from visiting login/signup)
function PublicRoute({ children }) {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  if (token) {
    // If already logged in, redirect to their dashboard
    return <Navigate to={role === 'doctor' ? '/doctor/dashboard' : '/patient/dashboard'} replace />;
  }

  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/about" element={<AboutUs />} />
        <Route path="/contact" element={<ContactUs />} />
        
        {/* Public auth routes (restricted if logged in) */}
        <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
        <Route path="/signup" element={<PublicRoute><Signup /></PublicRoute>} />
        <Route path="/forgot-password" element={<PublicRoute><ForgotPassword /></PublicRoute>} />
        
        {/* Protected dashboards */}
        <Route 
          path="/patient/dashboard" 
          element={
            <ProtectedRoute allowedRole="patient">
              <PatientDashboard />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/doctor/dashboard" 
          element={
            <ProtectedRoute allowedRole="doctor">
              <DoctorDashboard />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
