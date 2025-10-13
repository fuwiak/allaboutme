<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import ScriptCard from '$lib/components/ScriptCard.svelte';
	import VideoCard from '$lib/components/VideoCard.svelte';

	let scripts: any[] = [];
	let videos: any[] = [];
	let activeTab: 'scripts' | 'videos' = 'scripts';
	let loading = true;

	onMount(async () => {
		// Check auth
		const token = localStorage.getItem('auth_token');
		if (!token) {
			goto('/');
			return;
		}

		await loadData();
	});

	async function loadData() {
		loading = true;
		try {
			// Ensure we have token
			const token = localStorage.getItem('auth_token');
			if (!token) {
				goto('/');
				return;
			}
			
			const [scriptsData, videosData] = await Promise.all([
				api.getScripts('draft'),
				api.getVideos()
			]);

			scripts = scriptsData;
			videos = videosData;
		} catch (error) {
			console.error('Error loading data:', error);
		} finally {
			loading = false;
		}
	}

	function logout() {
		localStorage.removeItem('auth_token');
		goto('/');
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900">
	<!-- Header -->
	<header class="bg-black/30 backdrop-blur-md border-b border-white/10">
		<div class="container mx-auto px-6 py-4">
			<div class="flex items-center justify-between">
				<h1 class="text-2xl font-bold text-white">AllAboutMe</h1>
				<nav class="flex items-center gap-6">
					<a href="/dashboard" class="text-gray-300 hover:text-white transition-colors"
						>Dashboard</a
					>
					<a href="/drafts" class="text-white font-semibold">Drafts</a>
					<a href="/publish" class="text-gray-300 hover:text-white transition-colors">Publish</a>
					<a href="/settings" class="text-gray-300 hover:text-white transition-colors">Settings</a>
					<button
						on:click={logout}
						class="text-red-300 hover:text-red-200 transition-colors text-sm"
					>
						Logout
					</button>
				</nav>
			</div>
		</div>
	</header>

	<!-- Main Content -->
	<main class="container mx-auto px-6 py-8">
		<div class="bg-white/10 backdrop-blur-md rounded-lg border border-white/20 overflow-hidden">
			<!-- Tabs -->
			<div class="flex border-b border-white/10">
				<button
					on:click={() => (activeTab = 'scripts')}
					class="{activeTab === 'scripts' 
						? 'bg-purple-600 text-white' 
						: 'text-gray-300 hover:bg-white/5'} flex-1 px-6 py-4 text-center font-semibold transition-all"
				>
					📝 Scripts ({scripts.length})
				</button>
				<button
					on:click={() => (activeTab = 'videos')}
					class="{activeTab === 'videos' 
						? 'bg-purple-600 text-white' 
						: 'text-gray-300 hover:bg-white/5'} flex-1 px-6 py-4 text-center font-semibold transition-all"
				>
					🎥 Videos ({videos.length})
				</button>
			</div>

			<!-- Content -->
			<div class="p-6">
				{#if loading}
					<div class="text-center py-12">
						<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto"></div>
						<p class="text-gray-300 mt-4">Loading...</p>
					</div>
				{:else if activeTab === 'scripts'}
					{#if scripts.length === 0}
						<div class="text-center py-12">
							<div class="text-6xl mb-4">📝</div>
							<p class="text-gray-300 text-lg">No scripts yet</p>
							<p class="text-gray-400 text-sm mt-2">
								Go to Dashboard to generate new scripts
							</p>
						</div>
					{:else}
						<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
							{#each scripts as script (script.id)}
								<ScriptCard {script} onUpdate={loadData} />
							{/each}
						</div>
					{/if}
				{:else}
					{#if videos.length === 0}
						<div class="text-center py-12">
							<div class="text-6xl mb-4">🎥</div>
							<p class="text-gray-300 text-lg">No videos yet</p>
							<p class="text-gray-400 text-sm mt-2">
								Create videos from your scripts first
							</p>
						</div>
					{:else}
						<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
							{#each videos as video (video.id)}
								<VideoCard {video} onUpdate={loadData} />
							{/each}
						</div>
					{/if}
				{/if}
			</div>
		</div>
	</main>
</div>

