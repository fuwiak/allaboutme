/**
 * API client for backend communication
 */

const API_BASE = import.meta.env.VITE_API_URL || '';

export class APIClient {
	private token: string | null = null;

	constructor() {
		// Don't load in constructor - will load on each request
	}
	
	private getToken(): string | null {
		// Always get fresh token from localStorage
		if (typeof window !== 'undefined') {
			return localStorage.getItem('auth_token');
		}
		return this.token;
	}

	setToken(token: string) {
		this.token = token;
		if (typeof window !== 'undefined') {
			localStorage.setItem('auth_token', token);
		}
	}

	clearToken() {
		this.token = null;
		if (typeof window !== 'undefined') {
			localStorage.removeItem('auth_token');
		}
	}

	private async request(endpoint: string, options: RequestInit = {}) {
		// Get fresh token
		const token = this.getToken();
		
		console.log(`[API] ${options.method || 'GET'} ${endpoint}`, {
			hasToken: !!token,
			tokenPrefix: token ? token.substring(0, 20) + '...' : 'none'
		});

		const headers: HeadersInit = {
			'Content-Type': 'application/json',
			...options.headers
		};

		if (token) {
			headers['Authorization'] = `Bearer ${token}`;
			console.log('[API] Authorization header added');
		} else {
			console.warn('[API] No token available!');
		}

		const response = await fetch(`${API_BASE}${endpoint}`, {
			...options,
			headers
		});

		if (!response.ok) {
			// Don't auto-logout - just throw error
			const error = await response.json().catch(() => ({ detail: 'Request failed' }));
			
			if (response.status === 401 || response.status === 403) {
				throw new Error(`Authentication error: ${error.detail || 'Not authenticated'}`);
			}
			
			throw new Error(error.detail || `HTTP ${response.status}`);
		}

		// Handle 204 No Content
		if (response.status === 204) {
			return null;
		}

		return response.json();
	}

	// Auth
	async login(username: string, password: string) {
		const data = await this.request('/api/auth/login', {
			method: 'POST',
			body: JSON.stringify({ username, password })
		});
		this.setToken(data.access_token);
		return data;
	}

	async register(username: string, password: string) {
		return this.request('/api/auth/register', {
			method: 'POST',
			body: JSON.stringify({ username, password })
		});
	}

	// Scripts
	async getScripts(status?: string) {
		const params = status ? `?status_filter=${status}` : '';
		return this.request(`/api/scripts/${params}`);
	}

	async getScript(id: number) {
		return this.request(`/api/scripts/${id}/`);
	}

	async createScript(data: any) {
		return this.request('/api/scripts/', {
			method: 'POST',
			body: JSON.stringify(data)
		});
	}

	async updateScript(id: number, data: any) {
		console.log('[API] updateScript - method: PUT, id:', id);
		const result = await this.request(`/api/scripts/${id}`, {
			method: 'PUT',
			body: JSON.stringify(data)
		});
		console.log('[API] updateScript success');
		return result;
	}

	async deleteScript(id: number) {
		const token = this.getToken();
		
		const response = await fetch(`/api/scripts/${id}`, {
			method: 'DELETE',
			headers: {
				'Authorization': `Bearer ${token}`,
				'Content-Type': 'application/json'
			}
		});

		if (!response.ok) {
			const error = await response.json().catch(() => ({ detail: 'Delete failed' }));
			throw new Error(error.detail || `HTTP ${response.status}`);
		}

		return response.status === 204 ? null : response.json();
	}

	// Videos
	async getVideos(status?: string) {
		const params = status ? `?status_filter=${status}` : '';
		return this.request(`/api/videos/${params}`);
	}

	async getVideo(id: number) {
		return this.request(`/api/videos/${id}/`);
	}

	async deleteVideo(id: number) {
		const token = this.getToken();
		
		const response = await fetch(`/api/videos/${id}`, {
			method: 'DELETE',
			headers: {
				'Authorization': `Bearer ${token}`,
				'Content-Type': 'application/json'
			}
		});

		if (!response.ok) {
			const error = await response.json().catch(() => ({ detail: 'Delete failed' }));
			throw new Error(error.detail || `HTTP ${response.status}`);
		}

		return response.status === 204 ? null : response.json();
	}

	// Generator
	async generateScripts(count: number = 1) {
		return this.request('/api/generate/scripts', {
			method: 'POST',
			body: JSON.stringify({ count })
		});
	}

	async generatePostText(scriptId: number) {
		return this.request(`/api/generate/post-text/${scriptId}`, {
			method: 'POST'
		});
	}

	async generateVideo(
		scriptId: number, 
		textPosition: string = 'center', 
		customBackground?: string,
		voiceId?: string
	) {
		const payload = { 
			script_id: scriptId,
			text_position: textPosition,
			custom_background: customBackground,
			voice_id: voiceId
		};
		
		console.log('[API] 🎬 generateVideo called with:', payload);
		console.log('[API] Background present?', !!customBackground);
		console.log('[API] Voice present?', !!voiceId);
		
		return this.request('/api/generate/video', {
			method: 'POST',
			body: JSON.stringify(payload)
		});
	}

	// Upload
	async uploadBackground(file: File) {
		const formData = new FormData();
		formData.append('file', file);
		
		const token = this.getToken();

		const response = await fetch(`${this.getApiUrl()}/api/upload/background`, {
			method: 'POST',
			headers: {
				'Authorization': `Bearer ${token}`
			},
			body: formData
		});

		if (!response.ok) {
			const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
			throw new Error(error.detail || `HTTP ${response.status}`);
		}

		return response.json();
	}

	async listBackgrounds() {
		return this.request('/api/upload/backgrounds');
	}

	// Tasks
	async cancelTask(taskId: string) {
		console.log('[API] Cancelling task:', taskId);
		const response = await this.request(`/api/tasks/${taskId}/cancel`, {
			method: 'POST'
		});
		console.log('[API] Cancel response:', response);
		return response;
	}

	async getTaskStatus(taskId: string) {
		return this.request(`/api/tasks/${taskId}/status`);
	}

	private getApiUrl() {
		return ''; // Same origin
	}

	// Publisher
	async publishVideo(videoId: number, platforms: string[]) {
		return this.request(`/api/publish/${videoId}`, {
			method: 'POST',
			body: JSON.stringify({ platforms })
		});
	}

	// Settings
	async getSettings() {
		return this.request('/api/settings/');
	}

	async updateSettings(settings: Record<string, any>) {
		return this.request('/api/settings/', {
			method: 'PUT',
			body: JSON.stringify({ settings })
		});
	}
}

export const api = new APIClient();

