import axios from 'axios';
import type { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import type { ApiClientConfig, ApiError, HttpResponse } from '../types';

class ApiClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor(config: ApiClientConfig) {
    this.baseURL = config.baseURL;
    
    this.client = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout || 10000,
      headers: {
        'Content-Type': 'application/json',
        ...config.headers,
      },
    });

    // Request interceptor for logging
    this.client.interceptors.request.use(
      (config) => {
        if (import.meta.env.DEV) {
          console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
          if (config.data) {
            console.log('📦 Request Data:', config.data);
          }
        }
        return config;
      },
      (error) => {
        console.error('❌ Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor for logging and error handling
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        if (import.meta.env.DEV) {
          console.log(`✅ API Response: ${response.status} ${response.config.url}`);
          console.log('📦 Response Data:', response.data);
        }
        return response;
      },
      (error: AxiosError) => {
        console.error('❌ API Error:', error);
        
        if (error.response) {
          // Server responded with error status
          const errorData = error.response.data as any;
          const apiError: ApiError = {
            detail: errorData?.detail || error.message,
            error_code: errorData?.error_code,
            requested_amount: errorData?.requested_amount,
            current_balance: errorData?.current_balance,
            timestamp: new Date().toISOString(),
          };
          throw apiError;
        } else if (error.request) {
          // Network error
          throw {
            detail: 'Network error. Please check your connection.',
            error_code: 'NETWORK_ERROR',
            timestamp: new Date().toISOString(),
          } as ApiError;
        } else {
          // Other error
          throw {
            detail: error.message || 'An unexpected error occurred.',
            error_code: 'UNKNOWN_ERROR',
            timestamp: new Date().toISOString(),
          } as ApiError;
        }
      }
    );
  }

  // Generic request method
  private async request<T>(
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    url: string,
    data?: any
  ): Promise<HttpResponse<T>> {
    const response = await this.client.request<T>({
      method,
      url,
      data,
    });

    return {
      data: response.data,
      status: response.status,
      statusText: response.statusText,
    };
  }

  // GET request
  async get<T>(url: string): Promise<HttpResponse<T>> {
    return this.request<T>('GET', url);
  }

  // POST request
  async post<T>(url: string, data?: any): Promise<HttpResponse<T>> {
    return this.request<T>('POST', url, data);
  }

  // PUT request
  async put<T>(url: string, data?: any): Promise<HttpResponse<T>> {
    return this.request<T>('PUT', url, data);
  }

  // DELETE request
  async delete<T>(url: string): Promise<HttpResponse<T>> {
    return this.request<T>('DELETE', url);
  }

  // Health check
  async healthCheck() {
    return this.get('/health');
  }

  // Get base URL
  getBaseURL(): string {
    return this.baseURL;
  }
}

// Environment-based configuration
const getApiConfig = (): ApiClientConfig => {
  const isDevelopment = import.meta.env.DEV;
  
  return {
    baseURL: isDevelopment 
      ? import.meta.env.VITE_API_URL || 'http://localhost:8000'
      : import.meta.env.VITE_API_URL || 'https://your-production-api-url.com',
    timeout: 10000,
    headers: {
      'Accept': 'application/json',
    },
  };
};

// Create and export the API client instance
export const apiClient = new ApiClient(getApiConfig());
export default apiClient;
