<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api';

	let currentLanguage = 'ru';
	let loading = false;

	onMount(async () => {
		try {
			const settings = await api.getSettings();
			currentLanguage = settings.language || 'ru';
		} catch (error) {
			console.error('Error loading language:', error);
		}
	});

	async function toggleLanguage() {
		loading = true;
		try {
			const newLang = currentLanguage === 'ru' ? 'en' : 'ru';
			await api.updateSettings({ language: newLang });
			currentLanguage = newLang;
			
			// Reload page to apply new language
			window.location.reload();
		} catch (error) {
			console.error('Error changing language:', error);
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

