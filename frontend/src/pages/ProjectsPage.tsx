import React, { useState, useEffect } from 'react';
import { Plus, Image, Edit, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import LogoUploadModal from '../components/LogoUploadModal';

interface Project {
  id: string;
  name: string;
  description?: string;
  status: string;
  priority: string;
  client_name?: string;
  logo_url?: string;
  requirements_count: number;
  progress_percentage: number;
  created_at: string;
}

const ProjectsPage: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [isLogoModalOpen, setIsLogoModalOpen] = useState(false);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/projects`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setProjects(data);
      } else {
        throw new Error('Erro ao carregar projetos');
      }
    } catch (error) {
      console.error('Erro ao carregar projetos:', error);
      toast.error('Erro ao carregar projetos');
    } finally {
      setLoading(false);
    }
  };

  const handleLogoUpload = (project: Project) => {
    setSelectedProject(project);
    setIsLogoModalOpen(true);
  };

  const handleUploadSuccess = (data: any) => {
    toast.success('Logo associada ao projeto com sucesso!');
    // Recarregar projetos para mostrar a nova logo
    loadProjects();
  };

  const handleUploadError = (error: string) => {
    toast.error(`Erro ao fazer upload: ${error}`);
  };

  const closeLogoModal = () => {
    setIsLogoModalOpen(false);
    setSelectedProject(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Projetos</h1>
          <p className="text-gray-600">Gerencie seus projetos de Business Intelligence</p>
        </div>
        <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center space-x-2">
          <Plus size={16} />
          <span>Novo Projeto</span>
        </button>
      </div>

      {projects.length === 0 ? (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6 text-center">
            <p className="text-gray-500">Nenhum projeto encontrado.</p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div key={project.id} className="bg-white shadow rounded-lg overflow-hidden">
              {/* Header com logo */}
              <div className="p-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {project.logo_url ? (
                      <img
                        src={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${project.logo_url}`}
                        alt={`Logo ${project.name}`}
                        className="w-12 h-12 object-contain rounded-lg border border-gray-200"
                      />
                    ) : (
                      <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                        <Image className="w-6 h-6 text-gray-400" />
                      </div>
                    )}
                    <div>
                      <h3 className="font-medium text-gray-900">{project.name}</h3>
                      <p className="text-sm text-gray-500">{project.client_name || 'Sem cliente'}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleLogoUpload(project)}
                    className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                    title="Upload de logo"
                  >
                    <Image size={16} />
                  </button>
                </div>
              </div>

              {/* Content */}
              <div className="p-4">
                <p className="text-sm text-gray-600 mb-4">
                  {project.description || 'Sem descrição'}
                </p>
                
                <div className="flex justify-between items-center mb-4">
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    project.status === 'em_andamento' ? 'bg-blue-100 text-blue-800' :
                    project.status === 'concluido' ? 'bg-green-100 text-green-800' :
                    project.status === 'cancelado' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {project.status.replace('_', ' ')}
                  </span>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    project.priority === 'alta' ? 'bg-red-100 text-red-800' :
                    project.priority === 'media' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {project.priority}
                  </span>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Progresso</span>
                    <span className="font-medium">{project.progress_percentage}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full transition-all"
                      style={{ width: `${project.progress_percentage}%` }}
                    ></div>
                  </div>
                </div>

                <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-200">
                  <span className="text-sm text-gray-500">
                    {project.requirements_count} requisitos
                  </span>
                  <div className="flex space-x-2">
                    <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                      <Edit size={14} />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal de upload de logo */}
      <LogoUploadModal
        isOpen={isLogoModalOpen}
        onClose={closeLogoModal}
        projectId={selectedProject?.id}
        projectName={selectedProject?.name}
        onUploadSuccess={handleUploadSuccess}
        onUploadError={handleUploadError}
      />
    </div>
  );
};

export default ProjectsPage;
