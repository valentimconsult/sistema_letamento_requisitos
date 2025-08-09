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
  const [fields, setFields] = useState<DynamicField[]>([]);
  const [loading, setLoading] = useState(false);
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
    order_index: '0',
    validation_rules: {}
  });

  const fieldTypes = [
    { value: 'text', label: 'Texto' },
    { value: 'number', label: 'Numero' },
    { value: 'select', label: 'Selecao' },
    { value: 'checkbox', label: 'Caixa de selecao' },
    { value: 'date', label: 'Data' },
    { value: 'textarea', label: 'Area de texto' }
  ];

  const appliesToOptions = [
    { value: 'requirement', label: 'Requisito' },
    { value: 'project', label: 'Projeto' },
    { value: 'user', label: 'Usuario' }
  ];

  useEffect(() => {
    fetchFields();
  }, []);

  const fetchFields = async () => {
    setLoading(true);
    try {
      // Simular chamada da API - substituir pela chamada real
      const mockFields: DynamicField[] = [
        {
          id: '1',
          field_name: 'prioridade',
          field_type: 'select',
          field_label: 'Prioridade',
          field_description: 'Nivel de prioridade do requisito',
          options: ['Baixa', 'Media', 'Alta', 'Critica'],
          is_required: true,
          is_active: true,
          applies_to: 'requirement',
          order_index: '1',
          validation_rules: {},
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        }
      ];
      setFields(mockFields);
    } catch (error) {
      toast.error('Erro ao carregar campos');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (editingField) {
        // Atualizar campo existente
        const updatedFields = fields.map(field =>
          field.id === editingField.id ? { ...field, ...formData } : field
        );
        setFields(updatedFields);
        toast.success('Campo atualizado com sucesso');
      } else {
        // Criar novo campo
        const newField: DynamicField = {
          id: Date.now().toString(),
          ...formData,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };
        setFields([...fields, newField]);
        toast.success('Campo criado com sucesso');
      }

      setShowForm(false);
      setEditingField(null);
      resetForm();
    } catch (error) {
      toast.error('Erro ao salvar campo');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (field: DynamicField) => {
    setEditingField(field);
    setFormData({
      field_name: field.field_name,
      field_type: field.field_type,
      field_label: field.field_label,
      field_description: field.field_description,
      options: field.options,
      is_required: field.is_required,
      is_active: field.is_active,
      applies_to: field.applies_to,
      order_index: field.order_index,
      validation_rules: field.validation_rules
    });
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir este campo?')) {
      try {
        const updatedFields = fields.filter(field => field.id !== id);
        setFields(updatedFields);
        toast.success('Campo excluido com sucesso');
      } catch (error) {
        toast.error('Erro ao excluir campo');
      }
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
      order_index: '0',
      validation_rules: {}
    });
  };

  const addOption = () => {
    setFormData({
      ...formData,
      options: [...formData.options, '']
    });
  };

  const removeOption = (index: number) => {
    const newOptions = formData.options.filter((_, i) => i !== index);
    setFormData({
      ...formData,
      options: newOptions
    });
  };

  const updateOption = (index: number, value: string) => {
    const newOptions = [...formData.options];
    newOptions[index] = value;
    setFormData({
      ...formData,
      options: newOptions
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Configuracoes</h1>
          <p className="text-gray-600">Configure o sistema e campos dinamicos</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <Plus className="h-4 w-4 mr-2" />
          Novo Campo
        </button>
      </div>

      {/* Formulario de Campo Dinamico */}
      {showForm && (
        <div className="bg-white shadow rounded-lg border">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                {editingField ? 'Editar Campo' : 'Novo Campo Dinamico'}
              </h3>
              <button
                onClick={() => {
                  setShowForm(false);
                  setEditingField(null);
                  resetForm();
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Nome do Campo
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.field_name}
                    onChange={(e) => setFormData({ ...formData, field_name: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="ex: prioridade"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Tipo do Campo
                  </label>
                  <select
                    value={formData.field_type}
                    onChange={(e) => setFormData({ ...formData, field_type: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
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
                    Rotulo
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.field_label}
                    onChange={(e) => setFormData({ ...formData, field_label: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="ex: Prioridade"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Aplica-se a
                  </label>
                  <select
                    value={formData.applies_to}
                    onChange={(e) => setFormData({ ...formData, applies_to: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
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
                    type="number"
                    value={formData.order_index}
                    onChange={(e) => setFormData({ ...formData, order_index: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="0"
                  />
                </div>

                <div className="flex items-center space-x-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.is_required}
                      onChange={(e) => setFormData({ ...formData, is_required: e.target.checked })}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <span className="ml-2 text-sm text-gray-700">Campo obrigatorio</span>
                  </label>
                </div>

                <div className="flex items-center space-x-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.is_active}
                      onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <span className="ml-2 text-sm text-gray-700">Campo ativo</span>
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Descricao
                </label>
                <textarea
                  value={formData.field_description}
                  onChange={(e) => setFormData({ ...formData, field_description: e.target.value })}
                  rows={3}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Descreva o proposito deste campo..."
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
                      <div key={index} className="flex space-x-2">
                        <input
                          type="text"
                          value={option}
                          onChange={(e) => updateOption(index, e.target.value)}
                          className="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          placeholder={`Opcao ${index + 1}`}
                        />
                        <button
                          type="button"
                          onClick={() => removeOption(index)}
                          className="px-3 py-2 text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    ))}
                    <button
                      type="button"
                      onClick={addOption}
                      className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      Adicionar Opcao
                    </button>
                  </div>
                </div>
              )}

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingField(null);
                    resetForm();
                  }}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {loading ? (
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
          <h3 className="text-lg font-medium text-gray-900 mb-4">Campos Dinamicos</h3>
          
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">Carregando campos...</p>
            </div>
          ) : fields.length === 0 ? (
            <div className="text-center py-8">
              <Settings className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">Nenhum campo dinamico configurado</p>
              <p className="text-gray-500 text-sm">Clique em "Novo Campo" para comecar</p>
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
                  {fields.map((field) => (
                    <tr key={field.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {field.field_label}
                          </div>
                          <div className="text-sm text-gray-500">
                            {field.field_name}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {fieldTypes.find(t => t.value === field.field_type)?.label || field.field_type}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {appliesToOptions.find(a => a.value === field.applies_to)?.label || field.applies_to}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          field.is_active 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {field.is_active ? 'Ativo' : 'Inativo'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleEdit(field)}
                            className="text-blue-600 hover:text-blue-900"
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
    </div>
  );
};

export default SettingsPage;
