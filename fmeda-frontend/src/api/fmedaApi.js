import axios from 'axios';

// Use environment variable for API base URL, fallback to localhost for development
const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Projects API
export const getProjects = async () => {
  try {
    const response = await apiClient.get(`/projects/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching projects:', error);
    throw error;
  }
};

export const createProject = async (projectData) => {
  try {
    const response = await apiClient.post(`/projects/`, projectData);
    return response.data;
  } catch (error) {
    console.error('Error creating project:', error);
    throw error;
  }
};

export const updateProject = async (projectId, projectData) => {
  try {
    const response = await apiClient.patch(`/projects/${projectId}/`, projectData);
    return response.data;
  } catch (error) {
    console.error('Error updating project:', error);
    throw error;
  }
};

export const deleteProject = async (projectId) => {
  try {
    const response = await apiClient.delete(`/projects/${projectId}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting project:', error);
    throw error;
  }
};

// Safety Functions API
export const getSafetyFunctions = async (projectId) => {
  try {
    const response = await apiClient.get(`/safety-functions/?project=${projectId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching safety functions:', error);
    throw error;
  }
};

export const createSafetyFunction = async (safetyFunctionData) => {
  try {
    const response = await apiClient.post(`/safety-functions/`, safetyFunctionData);
    return response.data;
  } catch (error) {
    console.error('Error creating safety function:', error);
    throw error;
  }
};

export const updateSafetyFunction = async (safetyFunctionId, safetyFunctionData) => {
  try {
    const response = await apiClient.patch(`/safety-functions/${safetyFunctionId}/`, safetyFunctionData);
    return response.data;
  } catch (error) {
    console.error('Error updating safety function:', error);
    throw error;
  }
};

export const deleteSafetyFunction = async (safetyFunctionId) => {
  try {
    const response = await apiClient.delete(`/safety-functions/${safetyFunctionId}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting safety function:', error);
    throw error;
  }
};

// Components API
export const getComponents = async (projectId) => {
  try {
    const response = await apiClient.get(`/components/?project=${projectId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching components:', error);
    throw error;
  }
};

export const createComponent = async (componentData) => {
  try {
    const response = await apiClient.post(`/components/`, componentData);
    return response.data;
  } catch (error) {
    console.error('Error creating component:', error);
    throw error;
  }
};

export const updateComponent = async (componentId, componentData) => {
  try {
    const response = await apiClient.patch(`/components/${componentId}/`, componentData);
    return response.data;
  } catch (error) {
    console.error('Error updating component:', error);
    throw error;
  }
};

export const deleteComponent = async (componentId) => {
  try {
    const response = await apiClient.delete(`/components/${componentId}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting component:', error);
    throw error;
  }
};

// Failure Modes API
export const getFailureModes = async (componentId) => {
  try {
    const response = await apiClient.get(`/failure-modes/by-component/${componentId}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching failure modes:', error);
    throw error;
  }
};

export const createFailureMode = async (failureModeData) => {
  try {
    const response = await apiClient.post(`/failure-modes/`, failureModeData);
    return response.data;
  } catch (error) {
    console.error('Error creating failure mode:', error);
    throw error;
  }
};

export const updateFailureMode = async (failureModeId, failureModeData) => {
  try {
    const response = await apiClient.patch(`/failure-modes/${failureModeId}/`, failureModeData);
    return response.data;
  } catch (error) {
    console.error('Error updating failure mode:', error);
    throw error;
  }
};

export const deleteFailureMode = async (failureModeId) => {
  try {
    const response = await apiClient.delete(`/failure-modes/${failureModeId}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting failure mode:', error);
    throw error;
  }
};

// FMEDA Analysis API
export const calculateFMEDA = async (projectId) => {
  try {
    const response = await apiClient.post(`/fmeda/calculate/`, {
      project: projectId
    });
    return response.data;
  } catch (error) {
    console.error('Error calculating FMEDA:', error);
    throw error;
  }
};

export const getProjectResults = async (projectId) => {
  try {
    const response = await apiClient.get(`/fmeda/results/${projectId}/`);
    return response.data;
  } catch (error) {
    console.error('Error getting project results:', error);
    throw error;
  }
};

// CSV Import/Export API
export const importProject = async (formData) => {
  try {
    const response = await apiClient.post(`/projects/import-csv/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error importing project:', error);
    throw error;
  }
};

// Export project to CSV
export const exportProject = async (projectId) => {
  try {
    const response = await apiClient.get(`/projects/${projectId}/export-csv/`, {
      responseType: 'blob'
    });
    
    // Create and download the file
    const blob = new Blob([response.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fmeda_project_${projectId}.csv`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Clear all data
export const clearAllData = async () => {
  try {
    const response = await apiClient.get(`/projects/clear-all/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
