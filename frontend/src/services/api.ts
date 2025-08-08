import axios, { AxiosInstance, AxiosResponse } from 'axios';
import toast from 'react-hot-toast';

// Configuracao base da API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Criar instancia do axios
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticacao
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratamento de respostas
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    // Tratamento de erros
    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          // Token expirado ou invalido
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
          toast.error('Sessao expirada. Faca login novamente.');
          break;
        
        case 403:
          toast.error('Voce nao tem permissao para realizar esta acao.');
          break;
        
        case 404:
          toast.error('Recurso nao encontrado.');
          break;
        
        case 422:
          // Erro de validacao
          if (data.detail && Array.isArray(data.detail)) {
            const errors = data.detail.map((err: any) => err.msg).join(', ');
            toast.error(`Erro de validacao: ${errors}`);
          } else {
            toast.error(data.message || 'Erro de validacao');
          }
          break;
        
        case 500:
          toast.error('Erro interno do servidor. Tente novamente mais tarde.');
          break;
        
        default:
          toast.error(data.message || 'Erro inesperado');
      }
    } else if (error.request) {
      // Erro de rede
      toast.error('Erro de conexao. Verifique sua internet.');
    } else {
      // Outros erros
      toast.error('Erro inesperado');
    }
    
    return Promise.reject(error);
  }
);

// Funcoes auxiliares
export const handleApiError = (error: any): string => {
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  if (error.message) {
    return error.message;
  }
  return 'Erro inesperado';
};

export const formatDate = (dateString: string): string => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('pt-BR');
};

export const formatDateTime = (dateString: string): string => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleString('pt-BR');
};

export default api;
