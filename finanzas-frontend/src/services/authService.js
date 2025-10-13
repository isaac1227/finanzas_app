// AuthService - Manejo de autenticación JWT
const API_URL = 'http://localhost:8001/auth';

export const authService = {
  // 🔐 Login
  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetch(`${API_URL}/token`, {
      method: 'POST',
      body: formData,
    });
    
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('token', data.access_token);
      return data;
    }
    throw new Error('Login fallido');
  },

  // 📝 Registro
  async register(email, password) {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    
    if (response.ok) {
      return await response.json();
    }
    throw new Error('Registro fallido');
  },

  // 🚪 Logout
  logout() {
    localStorage.removeItem('token');
  },

  // 🎫 Obtener token
  getToken() {
    return localStorage.getItem('token');
  },

  // ✅ Verificar si está logueado
  isLoggedIn() {
    return !!this.getToken();
  },

  // 🌐 Fetch con token automático
  async apiCall(endpoint, options = {}) {
    const token = this.getToken();
    
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    };
    
    // Para apiCall, usar la URL base sin /auth
    const baseUrl = 'http://localhost:8001';
    const response = await fetch(`${baseUrl}${endpoint}`, config);
    
    if (response.status === 401) {
      this.logout();
      window.location.href = '/login';
    }
    
    return response;
  }
};