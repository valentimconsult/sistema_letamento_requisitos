import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth.tsx';
import { Link, useLocation } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

interface LogoData {
  filename: string;
  url: string;
  size: number;
  uploaded_at: string;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [currentLogo, setCurrentLogo] = useState<LogoData | null>(null);

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: '📊' },
    { name: 'Projetos', href: '/projects', icon: '📁' },
    { name: 'Requisitos', href: '/requirements', icon: '📋' },
    { name: 'Usuários', href: '/users', icon: '👥' },
    { name: 'Configurações', href: '/settings', icon: '⚙️' },
  ];

  // Carregar logo atual
  useEffect(() => {
    loadCurrentLogo();
  }, []);

  const loadCurrentLogo = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/upload/logo`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.logos && data.logos.length > 0) {
          setCurrentLogo(data.logos[0]);
        }
      }
    } catch (error) {
      console.error('Erro ao carregar logo:', error);
    }
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              {currentLogo ? (
                <div className="flex items-center space-x-3">
                  <img
                    src={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${currentLogo.url}`}
                    alt="Logo do sistema"
                    className="h-8 w-auto object-contain"
                  />
                  <h1 className="text-xl font-semibold text-gray-900">
                    Sistema BI - Requisitos
                  </h1>
                </div>
              ) : (
                <h1 className="text-xl font-semibold text-gray-900">
                  Sistema BI - Requisitos
                </h1>
              )}
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">
                Olá, {user?.first_name || user?.username || 'Usuário'}
              </span>
              <button
                onClick={handleLogout}
                className="text-sm text-red-600 hover:text-red-800"
              >
                Sair
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <nav className="w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen">
          <div className="p-4">
            <nav className="space-y-2">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                      isActive
                        ? 'bg-primary-100 text-primary-700 border-r-2 border-primary-700'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <span className="mr-3">{item.icon}</span>
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>
        </nav>

        {/* Main content */}
        <main className="flex-1 p-8">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
