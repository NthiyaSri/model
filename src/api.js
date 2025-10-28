const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5001'

let memoryToken = null
export function setToken(t) { memoryToken = t }
export function clearToken() { memoryToken = null }

async function request(path, options = {}) {
  const headers = options.headers || {}
  if (memoryToken) headers['Authorization'] = `Bearer ${memoryToken}`
  return fetch(`${API_BASE}${path}`, { credentials: 'include', ...options, headers })
}

export const api = {
  register: (data) => request('/api/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }),
  login: async (data) => {
    const res = await request('/api/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
    const json = await res.json()
    if (res.ok && json.token) setToken(json.token)
    return { res, json }
  },
  products: (query = '') => request(`/api/products${query}`),
  product: (id) => request(`/api/products/${id}`),
  createProduct: (body) => request(`/api/products`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }),
  updateProduct: (id, body) => request(`/api/products/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }),
  deleteProduct: (id) => request(`/api/products/${id}`, { method: 'DELETE' }),
  addToCart: (body) => request(`/api/cart`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }),
  getCart: () => request(`/api/cart`),
  checkout: (body) => request(`/api/checkout`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }),
  aiDescription: (body) => request(`/api/ai/description`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }),
  aiRecommendations: () => request(`/api/ai/recommendations`)
}
