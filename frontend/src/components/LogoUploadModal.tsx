import React from 'react';
import Modal from './Modal';
import LogoUpload from './LogoUpload';

interface LogoUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  projectId?: string;
  projectName?: string;
  onUploadSuccess?: (data: any) => void;
  onUploadError?: (error: string) => void;
}

const LogoUploadModal: React.FC<LogoUploadModalProps> = ({
  isOpen,
  onClose,
  projectId,
  projectName,
  onUploadSuccess,
  onUploadError
}) => {
  const handleUploadSuccess = (data: any) => {
    onUploadSuccess?.(data);
    // O modal será fechado automaticamente pelo LogoUpload
  };

  const handleUploadError = (error: string) => {
    onUploadError?.(error);
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={projectId ? `Upload de Logo - ${projectName || 'Projeto'}` : 'Upload de Logo'}
      size="md"
    >
      <div className="space-y-4">
        <p className="text-gray-600">
          {projectId 
            ? `Selecione uma logo para associar ao projeto "${projectName || 'selecionado'}"`
            : 'Selecione uma logo para o sistema'
          }
        </p>
        
        <LogoUpload
          projectId={projectId}
          onUploadSuccess={handleUploadSuccess}
          onUploadError={handleUploadError}
          onClose={onClose}
        />
      </div>
    </Modal>
  );
};

export default LogoUploadModal;
