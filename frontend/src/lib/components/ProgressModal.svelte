<script lang="ts">
	import { onDestroy } from 'svelte';
	import { connectProgress } from '$lib/websocket';
	import { t } from '$lib/i18n';

	export let taskId: string;
	export let title: string = 'Processing...';
	export let onClose: () => void;
	export let onStop: (() => void) | null = null;

	let progress = 0;
	let status = 'Starting...';
	let elapsed = 0;
	let logs: string[] = [];
	let ws: WebSocket | null = null;
	let isCompleted = false;
	let isCancelling = false;
	
	// Debug
	console.log('[ProgressModal] Initialized with onStop:', onStop !== null);

	// Connect to WebSocket
	if (taskId) {
		ws = connectProgress(
			taskId,
			(data) => {
				status = data.status || 'Processing...';
				elapsed = data.elapsed || 0;
				progress = data.progress || Math.min(elapsed * 2, 95);

				// Add to logs
				const logEntry = `[${Math.floor(elapsed)}s] ${status}`;
				logs = [...logs, logEntry];

				// Check if completed
				if (data.status === 'completed') {
					progress = 100;
					isCompleted = true;
					// Auto-close after 2 seconds
					setTimeout(() => {
						if (ws) ws.close();
						onClose();
					}, 2000);
				} else if (data.status === 'failed') {
					isCompleted = true;
				}
			},
			(error) => {
				console.error('WebSocket error:', error);
				status = 'Connection error';
			}
		);
	}

	onDestroy(() => {
		if (ws) {
			ws.close();
		}
	});

	function handleClose() {
		if (ws) ws.close();
		onClose();
	}
</script>

<div class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50">
	<div class="bg-gray-800 rounded-lg shadow-2xl w-full max-w-2xl mx-4">
		<!-- Header -->
		<div class="flex items-center justify-between p-6 border-b border-gray-700">
			<div class="flex items-center gap-3">
				<div class="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-500"></div>
				<h2 class="text-xl font-bold text-white">{title}</h2>
			</div>
			{#if isCompleted}
				<button
					on:click={handleClose}
					class="text-gray-400 hover:text-white transition-colors"
				>
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						/>
					</svg>
				</button>
			{/if}
		</div>

		<!-- Content -->
		<div class="p-6 space-y-4">
			<!-- Progress Bar -->
			<div class="space-y-2">
				<div class="flex justify-between text-sm">
					<span class="text-gray-300">{status}</span>
					<span class="text-gray-400">{Math.floor(elapsed)}s elapsed</span>
				</div>
				<div class="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
					<div
						class="bg-gradient-to-r from-purple-500 to-blue-500 h-full transition-all duration-300 ease-out"
						style="width: {progress}%"
					/>
				</div>
				<div class="text-right text-sm text-gray-400">{Math.round(progress)}%</div>
			</div>

			<!-- Logs -->
			<div class="space-y-2">
				<h3 class="text-sm font-semibold text-gray-300">Detailed Progress:</h3>
				<div
					class="bg-black/50 rounded-lg p-4 h-64 overflow-y-auto font-mono text-xs text-gray-300 space-y-1"
				>
					{#each logs as log}
						<div class="hover:bg-gray-800/50 px-2 py-1 rounded">{log}</div>
					{/each}
					{#if logs.length === 0}
						<div class="text-gray-500 text-center py-8">Waiting for updates...</div>
					{/if}
				</div>
			</div>

			<!-- Actions -->
			<div class="flex justify-end gap-3 pt-4">
				{#if !isCompleted && onStop}
					<button
						on:click={async () => {
							if (isCancelling) {
								console.log('[ProgressModal] Already cancelling, ignoring click');
								return;
							}
							
							isCancelling = true;
							console.log('[ProgressModal] Stop button clicked');
							
							try {
								if (onStop) {
									console.log('[ProgressModal] Calling onStop function');
									await onStop();
									console.log('[ProgressModal] onStop completed');
								} else {
									console.error('[ProgressModal] onStop is null!');
								}
							} catch (error) {
								console.error('[ProgressModal] Error in onStop:', error);
								isCancelling = false;
							}
						}}
						disabled={isCancelling}
						class="px-6 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors"
					>
					{#if isCancelling}
						<span class="flex items-center gap-2">
							<div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
							{$t('common.cancelling')}
						</span>
					{:else}
						⏹️ {$t('common.stop')}
					{/if}
					</button>
				{/if}
				{#if isCompleted}
					<button
						on:click={handleClose}
						class="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition-colors"
					>
						Close
					</button>
				{/if}
			</div>
		</div>
	</div>
</div>

