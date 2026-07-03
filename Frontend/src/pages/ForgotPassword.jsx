import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Mail, ShieldCheck, Lock } from 'lucide-react';
import { motion } from 'framer-motion';
import { api } from '../lib/api';

export default function ForgotPassword() {
  const navigate = useNavigate();
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      const res = await api.post('/auth/reset-password', { email, new_password: password });
      if (res && res.status === 'success') {
        setIsSubmitted(true);
      } else {
        setError(res.detail || "Failed to reset password.");
      }
    } catch (err) {
      setError("Network error. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50/50 p-4">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-md w-full"
      >
        <button 
          onClick={() => navigate(-1)} 
          className="flex items-center text-sm font-semibold text-slate-500 hover:text-blue-600 transition-colors mb-6"
        >
          <ArrowLeft className="w-4 h-4 mr-1" /> Back
        </button>

        <div className="bg-white p-8 rounded-3xl shadow-xl shadow-blue-900/5 border border-slate-100">
          <div className="w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center mx-auto mb-6 text-blue-600">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-center text-slate-800 mb-2">Reset Password</h2>
          
          {!isSubmitted ? (
            <>
              <p className="text-slate-500 text-center mb-6 text-sm">
                Enter your registered email address and your new password to reset it securely.
              </p>
              {error && <div className="p-3 mb-6 bg-red-50 text-red-600 rounded-lg text-sm text-center font-semibold">{error}</div>}
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1.5">Email Address</label>
                  <div className="relative">
                    <Mail className="absolute left-3.5 top-3 h-5 w-5 text-slate-400" />
                    <input 
                      type="email" 
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full rounded-xl border-slate-200 bg-slate-50 pl-11 pr-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors" 
                      placeholder="name@example.com" 
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1.5">New Password</label>
                  <div className="relative">
                    <Lock className="absolute left-3.5 top-3 h-5 w-5 text-slate-400" />
                    <input 
                      type="password" 
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full rounded-xl border-slate-200 bg-slate-50 pl-11 pr-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors" 
                      placeholder="••••••••" 
                      required
                    />
                  </div>
                </div>
                <button 
                  type="submit"
                  disabled={loading}
                  className={`w-full inline-flex items-center justify-center rounded-xl text-md font-bold text-white bg-blue-600 hover:bg-blue-700 h-12 mt-2 transition-all shadow-lg hover:shadow-blue-500/30 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {loading ? 'Resetting Password...' : 'Reset Password'}
                </button>
              </form>
            </>
          ) : (
             <div className="text-center">
               <div className="bg-green-50 text-green-700 p-4 rounded-xl mb-6 text-sm font-medium border border-green-100">
                 Your password has been successfully reset. You can now log in securely.
               </div>
               <Link to="/login" className="text-blue-600 font-bold hover:underline">
                 Return to Login
               </Link>
             </div>
          )}
        </div>
      </motion.div>
    </div>
  );
}
