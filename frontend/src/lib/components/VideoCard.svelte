<script lang="ts">
	import { api } from '$lib/api';
	import ProgressModal from './ProgressModal.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	export let video: any;
	export let onUpdate: () => void;

	let showPublishModal = false;
	let selectedPlatforms: string[] = [];
	let showProgressModal = false;
	let currentTaskId = '';
	
	// Get token for media URLs
	let token = '';
	
	onMount(() => {
		if (browser) {
			token = localStorage.getItem('auth_token') || '';
			console.log('[VideoCard] Token loaded:', token ? `${token.substring(0, 20)}...` : 'EMPTY');
		}
	});
	
	// Reactive URLs - update when token or video.id changes
	$: videoUrl = token && video?.id ? `/api/videos/${video.id}/download?token=${encodeURIComponent(token)}` : '';
	$: audioUrl = token && video?.id ? `/api/videos/${video.id}/download-audio?token=${encodeURIComponent(token)}` : '';
	
	// Reactive logging
	$: {
		if (token && video?.id) {
			console.log(`[VideoCard-${video.id}] URLs:`, { 
				videoUrl: videoUrl.substring(0, 50) + '...',
				audioUrl: audioUrl.substring(0, 50) + '...'
			});
		}
	}

	const platforms = [
		{ id: 'telegram', name: 'Telegram', icon: '📱', color: 'blue' },
		{ id: 'youtube', name: 'YouTube Shorts', icon: '▶️', color: 'red' },
		{ id: 'tiktok', name: 'TikTok', icon: '🎵', color: 'pink' },
		{ id: 'instagram', name: 'Instagram Reels', icon: '📸', color: 'purple' }
	];

	function togglePlatform(platformId: string) {
		if (selectedPlatforms.includes(platformId)) {
			selectedPlatforms = selectedPlatforms.filter((p) => p !== platformId);
		} else {
			selectedPlatforms = [...selectedPlatforms, platformId];
		}
	}

	async function handlePublish() {
		if (selectedPlatforms.length === 0) {
			alert('Select at least one platform');
			return;
		}

		try {
			const result = await api.publishVideo(video.id, selectedPlatforms);
			currentTaskId = result.task_id;
			showPublishModal = false;
			showProgressModal = true;
		} catch (error) {
			alert(`Error publishing: ${error}`);
		}
	}

	async function handleCancelPublish() {
		console.log('[VideoCard] handleCancelPublish called, taskId:', currentTaskId);
		
		if (!currentTaskId) {
			console.error('[VideoCard] No currentTaskId!');
			alert('No task to cancel');
			return;
		}
		
		try {
			console.log('[VideoCard] Calling api.cancelTask...');
			await api.cancelTask(currentTaskId);
			console.log('[VideoCard] Task cancelled successfully');
			
			showProgressModal = false;
			currentTaskId = '';
			alert('Publishing cancelled');
		} catch (error) {
			console.error('[VideoCard] Error cancelling:', error);
			alert(`Error cancelling: ${error}`);
		}
	}

	async function handleDelete() {
		if (!confirm('Delete this video?')) return;

		try {
			await api.deleteVideo(video.id);
			onUpdate();
		} catch (error) {
			alert(`Error deleting video: ${error}`);
		}
	}

	function copyToClipboard(text: string) {
		navigator.clipboard.writeText(text);
		alert('Copied to clipboard!');
	}

	function getStatusColor(status: string) {
		switch (status) {
			case 'completed':
				return 'bg-green-500/20 text-green-300';
			case 'pending':
				return 'bg-yellow-500/20 text-yellow-300';
			case 'failed':
				return 'bg-red-500/20 text-red-300';
			default:
				return 'bg-gray-500/20 text-gray-300';
		}
	}
</script>

<div class="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700 hover:border-blue-500/50 transition-all">
	<!-- Header -->
	<div class="flex items-start justify-between mb-4">
		<div class="flex-1">
			<div class="flex items-center gap-2 mb-2">
				<span class="text-xs px-2 py-1 {getStatusColor(video.status)} rounded">
					{video.status}
				</span>
				<span class="text-xs px-2 py-1 bg-blue-500/20 text-blue-300 rounded">
					{video.generator || 'unknown'}
				</span>
			</div>
			<p class="text-sm text-gray-400">Video ID: {video.id}</p>
			{#if video.script_id}
				<p class="text-xs text-gray-500">Script ID: {video.script_id}</p>
			{/if}
		</div>
		<button on:click={handleDelete} class="text-red-400 hover:text-red-300 transition-colors">
			<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
				/>
			</svg>
		</button>
	</div>

	<!-- Media Preview -->
	<div class="space-y-3 mb-4">
		{#if video.video_path}
			<!-- Video Player -->
			<div class="bg-gray-900 rounded-lg p-3">
				<div class="flex items-center justify-between mb-2">
					<span class="text-sm font-semibold text-gray-300">🎥 Video Preview</span>
					<button
						on:click={() => copyToClipboard(video.video_path)}
						class="text-xs text-purple-400 hover:text-purple-300"
					>
						📋 Copy Path
					</button>
				</div>
				
			<!-- HTML5 Video Player -->
			<video
				controls
				preload="metadata"
				class="w-full rounded-lg bg-black mb-2"
				style="max-height: 400px;"
				on:error={(e) => console.error(`[VideoCard-${video.id}] Video load error:`, e)}
			>
				<source src={videoUrl} type="video/mp4" />
				Your browser doesn't support video playback.
			</video>
			{#if !videoUrl}
				<div class="text-xs text-yellow-400 mt-1">⚠️ Video URL not available (token: {token ? 'yes' : 'no'})</div>
			{/if}
				
				<div class="flex gap-2">
					<a
						href={videoUrl}
						download
						class="flex-1 text-center px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded transition-colors"
					>
						⬇️ Download Video
					</a>
				</div>
			</div>
		{/if}

		{#if video.audio_path}
			<!-- Audio Player -->
			<div class="bg-gray-900 rounded-lg p-3">
				<div class="flex items-center justify-between mb-2">
					<span class="text-sm font-semibold text-gray-300">🎵 Audio Preview</span>
					<button
						on:click={() => copyToClipboard(video.audio_path)}
						class="text-xs text-purple-400 hover:text-purple-300"
					>
						📋 Copy Path
					</button>
				</div>
				
			<!-- HTML5 Audio Player -->
			<audio
				controls
				preload="metadata"
				class="w-full mb-2"
				on:error={(e) => console.error(`[VideoCard-${video.id}] Audio load error:`, e)}
			>
				<source src={audioUrl} type="audio/mpeg" />
				Your browser doesn't support audio playback.
			</audio>
			{#if !audioUrl}
				<div class="text-xs text-yellow-400 mt-1">⚠️ Audio URL not available (token: {token ? 'yes' : 'no'})</div>
			{/if}
				
				<div class="flex gap-2">
					<a
						href={audioUrl}
						download
						class="flex-1 text-center px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded transition-colors"
					>
						⬇️ Download Audio
					</a>
				</div>
			</div>
		{/if}

		{#if video.error_message}
			<div class="bg-red-500/10 border border-red-500/30 rounded-lg p-3">
				<p class="text-xs text-red-300">❌ Error: {video.error_message}</p>
			</div>
		{/if}
	</div>

	<!-- Actions -->
	{#if video.status === 'completed'}
		<div class="flex gap-3">
			<button
				on:click={() => (showPublishModal = true)}
				class="flex-1 px-4 py-2 bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-bold rounded-lg transition-all"
			>
				📤 Publish
			</button>
		</div>
	{/if}
</div>

<!-- Publish Modal -->
{#if showPublishModal}
	<div
		class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-40"
		on:click={() => (showPublishModal = false)}
	>
		<div
			class="bg-gray-800 rounded-lg shadow-2xl w-full max-w-md mx-4 p-6"
			on:click|stopPropagation
		>
			<h3 class="text-xl font-bold text-white mb-4">📤 Publish Video</h3>

			<div class="space-y-3 mb-6">
				{#each platforms as platform}
					<button
						on:click={() => togglePlatform(platform.id)}
						class="w-full p-4 rounded-lg border-2 transition-all text-left {selectedPlatforms.includes(platform.id)
							? 'border-purple-500 bg-purple-500/10'
							: 'border-gray-600 bg-gray-900'}"
					>
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-3">
								<span class="text-2xl">{platform.icon}</span>
								<span class="text-white font-semibold">{platform.name}</span>
							</div>
							{#if selectedPlatforms.includes(platform.id)}
								<span class="text-purple-400">✓</span>
							{/if}
						</div>
					</button>
				{/each}
			</div>

			<div class="flex gap-3">
				<button
					on:click={handlePublish}
					disabled={selectedPlatforms.length === 0}
					class="flex-1 px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors"
				>
					Publish to {selectedPlatforms.length} platform{selectedPlatforms.length !== 1 ? 's' : ''}
				</button>
				<button
					on:click={() => (showPublishModal = false)}
					class="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
				>
					Cancel
				</button>
			</div>
		</div>
	</div>
{/if}

<!-- Progress Modal -->
{#if showProgressModal}
	<ProgressModal
		taskId={currentTaskId}
		title="Publishing Video"
		onClose={() => {
			showProgressModal = false;
			onUpdate();
		}}
		onStop={handleCancelPublish}
	/>
{/if}

