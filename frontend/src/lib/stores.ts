/**
 * Svelte stores for app state
 */
import { writable } from 'svelte/store';

// Auth store
export const authStore = writable<{
	isAuthenticated: boolean;
	username: string | null;
}>({
	isAuthenticated: false,
	username: null
});

// Scripts store
export const scriptsStore = writable<any[]>([]);

// Videos store
export const videosStore = writable<any[]>([]);

// Settings store
export const settingsStore = writable<Record<string, any>>({});

// Active tasks (for progress tracking)
export const activeTasksStore = writable<Record<string, any>>({});

