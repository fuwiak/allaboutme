<script lang="ts">
	import { onMount } from 'svelte';
	import { language, type Language } from '$lib/i18n';
	import { api } from '$lib/api';

	let currentLanguage: Language = 'ru';
	let loading = false;

	// Subscribe to language store
	const unsubscribe = language.subscribe(value => {
		currentLanguage = value;
	});

	onMount(() => {
		// Load language from backend
		api.getSettings()
			.then(settings => {
				if (settings.language) {
					language.set(settings.language as Language);
				}
			})
			.catch(error => {
				console.error('Error loading language:', error);
			});
		
		// Return cleanup function
		return () => {
			unsubscribe();
		};
	});

	async function toggleLanguage() {
		loading = true;
		try {
			const newLang: Language = currentLanguage === 'ru' ? 'en' : 'ru';
			
			// Update local store immediately for instant UI change
			language.set(newLang);
			
			// Save to backend
			await api.updateSettings({ language: newLang });
		} catch (error) {
			console.error('Error changing language:', error);
			// Revert on error
			language.set(currentLanguage === 'ru' ? 'en' : 'ru');
			alert('Failed to change language');
		} finally {
			loading = false;
		}
	}
</script>

<button
	on:click={toggleLanguage}
	disabled={loading}
	class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/10 transition-all disabled:opacity-50"
	title={currentLanguage === 'ru' ? 'Switch to English' : 'Переключить на русский'}
>
	{#if loading}
		<div class="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
	{:else}
		<span class="text-2xl">{currentLanguage === 'ru' ? '🇷🇺' : '🇬🇧'}</span>
	{/if}
	<span class="text-sm font-medium text-white uppercase">{currentLanguage}</span>
</button>

<style>
	button:hover span {
		transform: scale(1.1);
	}
</style>


