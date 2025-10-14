<script lang="ts">
	import { t } from '$lib/i18n';
	
	let isRestarting = false;

	async function handleRestart() {
		if (isRestarting) return;
		
		if (!confirm('🔄 Restart the application?\n\nThis will:\n- Clear all local data\n- Refresh the page\n- Reconnect to backend')) {
			return;
		}

		isRestarting = true;
		
		try {
			// Clear localStorage (except keep token)
			const token = localStorage.getItem('token');
			localStorage.clear();
			if (token) {
				localStorage.setItem('token', token);
			}
			
			// Show notification
			console.log('[RestartButton] Restarting application...');
			
			// Reload page after short delay
			setTimeout(() => {
				window.location.reload();
			}, 100);
			
		} catch (error) {
			console.error('[RestartButton] Error during restart:', error);
			isRestarting = false;
		}
	}
</script>

<button
	on:click={handleRestart}
	disabled={isRestarting}
	class="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 border border-gray-600/50 hover:border-gray-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
	title="Restart Application"
>
	{#if isRestarting}
		<div class="animate-spin rounded-full h-4 w-4 border-2 border-white/30 border-t-white"></div>
		<span class="text-sm font-medium text-white">{$t('common.loading').includes('...') ? 'Restarting...' : 'Перезапуск...'}</span>
	{:else}
		<svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
			/>
		</svg>
		<span class="text-sm font-medium text-white">{$t('common.restart')}</span>
	{/if}
</button>

<style>
	button:hover svg {
		transform: rotate(180deg);
		transition: transform 0.3s ease;
	}
</style>


