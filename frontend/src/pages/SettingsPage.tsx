import React, { useState, useEffect } from 'react';
import LogoUpload from '../components/LogoUpload';
import { Settings, Image, Save } from 'lucide-react';
import toast from 'react-hot-toast';

interface LogoData {
  filename: string;
  url: string;
  size: number;
  uploaded_at: string;
}

const SettingsPage: React.FC = () => {
  const [currentLogo, setCurrentLogo] = useState<LogoData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

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

  const handleUploadSuccess = (data: LogoData) => {
    setCurrentLogo(data);
    toast.success('Logo atualizada com sucesso!');
  };

  const handleUploadError = (error: string) => {
    toast.error(`Erro ao fazer upload: ${error}`);
  };

  const handleRemoveLogo = async () => {
    if (!currentLogo) return;

    setIsLoading(true);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/upload/logo/${currentLogo.filename}`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        }
      );

      if (response.ok) {
        setCurrentLogo(null);
        toast.success('Logo removida com sucesso!');
      } else {
        throw new Error('Erro ao remover logo');
      }
    } catch (error) {
      toast.error('Erro ao remover logo');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Configuracoes</h1>
        <p className="text-gray-600">Configure o sistema e campos dinamicos</p>
      </div>

      {/* Secao de Logo */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex items-center space-x-2 mb-4">
            <Image className="h-5 w-5 text-gray-400" />
            <h3 className="text-lg font-medium text-gray-900">Logo do Sistema</h3>
          </div>
          
          <div className="space-y-4">
            {currentLogo && (
              <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                <img
                  src={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${currentLogo.url}`}
                  alt="Logo atual"
                  className="h-16 w-auto object-contain"
                />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{currentLogo.filename}</p>
                  <p className="text-xs text-gray-500">
                    {(currentLogo.size / 1024).toFixed(1)} KB
                  </p>
                </div>
                <button
                  onClick={handleRemoveLogo}
                  disabled={isLoading}
                  className="px-3 py-1 text-sm text-red-600 hover:text-red-800 disabled:opacity-50"
                >
                  Remover
                </button>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {currentLogo ? 'Substituir Logo' : 'Adicionar Logo'}
              </label>
              <LogoUpload
                onUploadSuccess={handleUploadSuccess}
                onUploadError={handleUploadError}
                className="max-w-md"
              />
            </div>

            <div className="text-xs text-gray-500">
              <p>Formatos suportados: PNG, JPG, JPEG, GIF, SVG</p>
              <p>Tamanho maximo: 5MB</p>
            </div>
          </div>
        </div>
      </div>

      {/* Outras configuracoes */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex items-center space-x-2 mb-4">
            <Settings className="h-5 w-5 text-gray-400" />
            <h3 className="text-lg font-medium text-gray-900">Outras Configuracoes</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Configuracoes do Sistema
              </label>
              <p className="text-sm text-gray-500 mt-1">
                Outras configuracoes serao implementadas aqui.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
