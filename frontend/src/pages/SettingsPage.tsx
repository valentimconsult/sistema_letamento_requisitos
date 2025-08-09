import React, { useState, useEffect } from 'react';
import { Settings, Plus, Edit, Trash2, Save, X, CheckCircle, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

interface DynamicField {
  id: string;
  field_name: string;
  field_type: string;
  field_label: string;
  field_description: string;
  options: string[];
  is_required: boolean;
  is_active: boolean;
  applies_to: string;
  order_index: string;
  validation_rules: any;
  created_at: string;
  updated_at: string;
}

interface DynamicFieldForm {
  field_name: string;
  field_type: string;
  field_label: string;
  field_description: string;
  options: string[];
  is_required: boolean;
  is_active: boolean;
  applies_to: string;
  order_index: string;
  validation_rules: any;
}

const SettingsPage: React.FC = () => {
  const [dynamicFields, setDynamicFields] = useState<DynamicField[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingField, setEditingField] = useState<DynamicField | null>(null);
  const [formData, setFormData] = useState<DynamicFieldForm>({
    field_name: '',
    field_type: 'text',
    field_label: '',
    field_description: '',
    options: [],
    is_required: false,
    is_active: true,
    applies_to: 'requirement',
    order_index: '',
    validation_rules: {}
  });

  // Carregar campos dinamicos
  useEffect(() => {
    loadDynamicFields();
  }, []);

  const loadDynamicFields = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/dynamic-fields`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setDynamicFields(data);
      } else {
        throw new Error('Erro ao carregar campos dinamicos');
      }
    } catch (error) {
      console.error('Erro ao carregar campos dinamicos:', error);
      toast.error('Erro ao carregar campos dinamicos');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      field_name: '',
      field_type: 'text',
      field_label: '',
      field_description: '',
      options: [],
      is_required: false,
      is_active: true,
      applies_to: 'requirement',
      order_index: '',
      validation_rules: {}
    });
    setEditingField(null);
    setShowForm(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const url = editingField 
        ? `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/dynamic-fields/${editingField.id}`
        : `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/dynamic-fields`;

      const method = editingField ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const message = editingField ? 'Campo atualizado com sucesso!' : 'Campo criado com sucesso!';
        toast.success(message);
        resetForm();
        loadDynamicFields();
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro ao salvar campo');
      }
    } catch (error) {
      console.error('Erro ao salvar campo:', error);
      toast.error(error instanceof Error ? error.message : 'Erro ao salvar campo');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (field: DynamicField) => {
    setEditingField(field);
    setFormData({
      field_name: field.field_name,
      field_type: field.field_type,
      field_label: field.field_label,
      field_description: field.field_description,
      options: field.options || [],
      is_required: field.is_required,
      is_active: field.is_active,
      applies_to: field.applies_to,
      order_index: field.order_index || '',
      validation_rules: field.validation_rules || {}
    });
    setShowForm(true);
  };

  const handleDelete = async (fieldId: string) => {
    if (!confirm('Tem certeza que deseja excluir este campo?')) return;

    setIsLoading(true);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/dynamic-fields/${fieldId}`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        }
      );

      if (response.ok) {
        toast.success('Campo excluido com sucesso!');
        loadDynamicFields();
      } else {
        throw new Error('Erro ao excluir campo');
      }
    } catch (error) {
      console.error('Erro ao excluir campo:', error);
      toast.error('Erro ao excluir campo');
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleActive = async (field: DynamicField) => {
    try {
      const action = field.is_active ? 'deactivate' : 'activate';
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/dynamic-fields/${field.id}/${action}`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        }
      );

      if (response.ok) {
        toast.success(`Campo ${field.is_active ? 'desativado' : 'ativado'} com sucesso!`);
        loadDynamicFields();
      } else {
        throw new Error('Erro ao alterar status do campo');
      }
    } catch (error) {
      console.error('Erro ao alterar status do campo:', error);
      toast.error('Erro ao alterar status do campo');
    }
  };

  const addOption = () => {
    setFormData(prev => ({
      ...prev,
      options: [...prev.options, '']
    }));
  };

  const updateOption = (index: number, value: string) => {
    setFormData(prev => ({
      ...prev,
      options: prev.options.map((opt, i) => i === index ? value : opt)
    }));
  };

  const removeOption = (index: number) => {
    setFormData(prev => ({
      ...prev,
      options: prev.options.filter((_, i) => i !== index)
    }));
  };

  const fieldTypes = [
    { value: 'text', label: 'Texto' },
    { value: 'number', label: 'Numero' },
    { value: 'date', label: 'Data' },
    { value: 'select', label: 'Selecao' },
    { value: 'textarea', label: 'Area de Texto' },
    { value: 'boolean', label: 'Booleano' }
  ];

  const appliesToOptions = [
    { value: 'requirement', label: 'Requisito' },
    { value: 'project', label: 'Projeto' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Configuracoes</h1>
          <p className="text-gray-600">Configure o sistema e campos dinamicos</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <Plus className="h-4 w-4 mr-2" />
          Novo Campo
        </button>
      </div>

      {/* Formulario de Campo Dinamico */}
      {showForm && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                {editingField ? 'Editar Campo' : 'Novo Campo Dinamico'}
              </h3>
              <button
                onClick={resetForm}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Nome do Campo *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.field_name}
                    onChange={(e) => setFormData(prev => ({ ...prev, field_name: e.target.value }))}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    placeholder="nome_campo"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Tipo do Campo *
                  </label>
                  <select
                    required
                    value={formData.field_type}
                    onChange={(e) => setFormData(prev => ({ ...prev, field_type: e.target.value }))}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  >
                    {fieldTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Rotulo do Campo
                  </label>
                  <input
                    type="text"
                    value={formData.field_label}
                    onChange={(e) => setFormData(prev => ({ ...prev, field_label: e.target.value }))}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    placeholder="Rotulo para exibicao"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Aplica-se a *
                  </label>
                  <select
                    required
                    value={formData.applies_to}
                    onChange={(e) => setFormData(prev => ({ ...prev, applies_to: e.target.value }))}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  >
                    {appliesToOptions.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Ordem
                  </label>
                  <input
                    type="text"
                    value={formData.order_index}
                    onChange={(e) => setFormData(prev => ({ ...prev, order_index: e.target.value }))}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    placeholder="1, 2, 3..."
                  />
                </div>

                <div className="flex items-center space-x-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.is_required}
                      onChange={(e) => setFormData(prev => ({ ...prev, is_required: e.target.checked }))}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <span className="ml-2 text-sm text-gray-700">Campo obrigatorio</span>
                  </label>

                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.is_active}
                      onChange={(e) => setFormData(prev => ({ ...prev, is_active: e.target.checked }))}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <span className="ml-2 text-sm text-gray-700">Ativo</span>
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Descricao
                </label>
                <textarea
                  value={formData.field_description}
                  onChange={(e) => setFormData(prev => ({ ...prev, field_description: e.target.value }))}
                  rows={3}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Descricao do campo..."
                />
              </div>

              {/* Opcoes para campos do tipo select */}
              {formData.field_type === 'select' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Opcoes
                  </label>
                  <div className="space-y-2">
                    {formData.options.map((option, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <input
                          type="text"
                          value={option}
                          onChange={(e) => updateOption(index, e.target.value)}
                          className="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                          placeholder={`Opcao ${index + 1}`}
                        />
                        <button
                          type="button"
                          onClick={() => removeOption(index)}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    ))}
                    <button
                      type="button"
                      onClick={addOption}
                      className="inline-flex items-center px-3 py-1 border border-gray-300 rounded-md text-sm text-gray-700 hover:bg-gray-50"
                    >
                      <Plus className="h-4 w-4 mr-1" />
                      Adicionar Opcao
                    </button>
                  </div>
                </div>
              )}

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={resetForm}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
                >
                  {isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Salvando...
                    </>
                  ) : (
                    <>
                      <Save className="h-4 w-4 mr-2" />
                      {editingField ? 'Atualizar' : 'Criar'}
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Lista de Campos Dinamicos */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex items-center space-x-2 mb-4">
            <Settings className="h-5 w-5 text-gray-400" />
            <h3 className="text-lg font-medium text-gray-900">Campos Dinamicos</h3>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
              <span className="ml-2 text-gray-600">Carregando campos...</span>
            </div>
          ) : dynamicFields.length === 0 ? (
            <div className="text-center py-8">
              <AlertCircle className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhum campo dinamico</h3>
              <p className="mt-1 text-sm text-gray-500">
                Comece criando seu primeiro campo dinamico para personalizar os requisitos.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Campo
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Tipo
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Aplica-se a
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Acoes
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {dynamicFields.map((field) => (
                    <tr key={field.id}>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {field.field_label || field.field_name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {field.field_description || 'Sem descricao'}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {fieldTypes.find(t => t.value === field.field_type)?.label || field.field_type}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {appliesToOptions.find(o => o.value === field.applies_to)?.label || field.applies_to}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button
                          onClick={() => handleToggleActive(field)}
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            field.is_active
                              ? 'bg-green-100 text-green-800 hover:bg-green-200'
                              : 'bg-red-100 text-red-800 hover:bg-red-200'
                          }`}
                        >
                          {field.is_active ? (
                            <>
                              <CheckCircle className="h-3 w-3 mr-1" />
                              Ativo
                            </>
                          ) : (
                            <>
                              <AlertCircle className="h-3 w-3 mr-1" />
                              Inativo
                            </>
                          )}
                        </button>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleEdit(field)}
                            className="text-primary-600 hover:text-primary-900"
                          >
                            <Edit className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(field.id)}
                            className="text-red-600 hover:text-red-900"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Configuracoes do Sistema */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex items-center space-x-2 mb-4">
            <Settings className="h-5 w-5 text-gray-400" />
            <h3 className="text-lg font-medium text-gray-900">Configuracoes do Sistema</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Configuracoes Gerais
              </label>
              <p className="text-sm text-gray-500 mt-1">
                Outras configuracoes do sistema serao implementadas aqui.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
