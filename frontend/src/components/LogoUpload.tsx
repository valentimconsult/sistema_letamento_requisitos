import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, Image, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

interface LogoUploadProps {
  onUploadSuccess?: (data: any) => void;
  onUploadError?: (error: string) => void;
  className?: string;
}

const LogoUpload: React.FC<LogoUploadProps> = ({ 
  onUploadSuccess, 
  onUploadError, 
  className = '' 
}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedLogo, setUploadedLogo] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    
    // Validar tipo de arquivo
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/svg+xml'];
    if (!allowedTypes.includes(file.type)) {
      toast.error('Tipo de arquivo nao permitido. Use apenas: JPEG, JPG, PNG, GIF ou SVG');
      onUploadError?.('Tipo de arquivo nao permitido');
      return;
    }

    // Validar tamanho (5MB)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      toast.error('Arquivo muito grande. Tamanho maximo permitido: 5MB');
      onUploadError?.('Arquivo muito grande');
      return;
    }

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/upload/logo`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro ao fazer upload');
      }

      const data = await response.json();
      
      // Criar URL para preview
      const logoUrl = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${data.url}`;
      setUploadedLogo(logoUrl);
      
      toast.success('Logo enviada com sucesso!');
      onUploadSuccess?.(data);
      
    } catch (error) {
      console.error('Erro no upload:', error);
      const errorMessage = error instanceof Error ? error.message : 'Erro ao fazer upload';
      toast.error(errorMessage);
      onUploadError?.(errorMessage);
    } finally {
      setIsUploading(false);
    }
  }, [onUploadSuccess, onUploadError]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.svg']
    },
    maxFiles: 1,
    disabled: isUploading
  });

  const removeLogo = () => {
    setUploadedLogo(null);
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {uploadedLogo ? (
        <div className="relative inline-block">
          <img
            src={uploadedLogo}
            alt="Logo enviada"
            className="max-w-xs max-h-32 object-contain border border-gray-300 rounded-lg"
          />
          <button
            onClick={removeLogo}
            className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
          >
            <X size={16} />
          </button>
        </div>
      ) : (
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors
            ${isDragActive && !isDragReject 
              ? 'border-primary-500 bg-primary-50' 
              : isDragReject 
                ? 'border-red-500 bg-red-50' 
                : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            }
            ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input {...getInputProps()} />
          
          {isUploading ? (
            <div className="space-y-2">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
              <p className="text-sm text-gray-600">Enviando logo...</p>
            </div>
          ) : (
            <div className="space-y-2">
              {isDragReject ? (
                <AlertCircle className="mx-auto h-8 w-8 text-red-500" />
              ) : (
                <Upload className="mx-auto h-8 w-8 text-gray-400" />
              )}
              
              {isDragActive && !isDragReject ? (
                <p className="text-primary-600 font-medium">Solte a logo aqui...</p>
              ) : isDragReject ? (
                <p className="text-red-600 font-medium">Tipo de arquivo nao permitido</p>
              ) : (
                <div>
                  <p className="text-gray-600 font-medium">
                    Arraste e solte uma logo aqui, ou clique para selecionar
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    PNG, JPG, JPEG, GIF ou SVG (max. 5MB)
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LogoUpload;
