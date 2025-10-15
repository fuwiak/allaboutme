import { writable } from 'svelte/store';

export interface VideoSettings {
	textPosition: 'top' | 'center' | 'bottom';
	voiceId: string;
	backgroundUrl: string | null;
	backgroundTheme: string;
}

// Default settings - NO custom background by default!
const defaultSettings: VideoSettings = {
	textPosition: 'center',
	voiceId: 'pNInz6obpgDQGcFmaJgB', // Adam (ElevenLabs)
	backgroundUrl: null, // null = auto-detect from script, user can override
	backgroundTheme: 'cosmic' // Default theme for generation
};

// Load from localStorage if available
function loadSettings(): VideoSettings {
	if (typeof window === 'undefined') return defaultSettings;
	
	const saved = localStorage.getItem('video_settings');
	if (saved) {
		try {
			return { ...defaultSettings, ...JSON.parse(saved) };
		} catch (e) {
			console.error('Failed to load video settings:', e);
		}
	}
	return defaultSettings;
}

// Create store
export const videoSettings = writable<VideoSettings>(loadSettings());

// Save to localStorage on changes (but skip blob URLs)
if (typeof window !== 'undefined') {
	videoSettings.subscribe(value => {
		// Don't save blob URLs to localStorage (they won't work after reload)
		const valueToSave = {
			...value,
			backgroundUrl: value.backgroundUrl?.startsWith('blob:') ? null : value.backgroundUrl
		};
		localStorage.setItem('video_settings', JSON.stringify(valueToSave));
		console.log('[VideoSettings] Settings saved:', valueToSave);
	});
}

// Helper functions
export function updateTextPosition(position: 'top' | 'center' | 'bottom') {
	videoSettings.update(s => ({ ...s, textPosition: position }));
}

export function updateVoice(voiceId: string) {
	videoSettings.update(s => ({ ...s, voiceId }));
}

export function updateBackground(url: string | null, theme?: string) {
	videoSettings.update(s => ({ 
		...s, 
		backgroundUrl: url,
		...(theme && { backgroundTheme: theme })
	}));
}

export function clearBackground() {
	videoSettings.update(s => ({ ...s, backgroundUrl: null }));
}

export function resetSettings() {
	videoSettings.set(defaultSettings);
}

