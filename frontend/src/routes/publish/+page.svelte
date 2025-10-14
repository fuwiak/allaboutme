<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import VideoCard from '$lib/components/VideoCard.svelte';
	import LanguageSwitcher from '$lib/components/LanguageSwitcher.svelte';
	import RestartButton from '$lib/components/RestartButton.svelte';

	let videos: any[] = [];
	let loading = true;
	let filter: 'all' | 'completed' | 'pending' | 'failed' = 'completed';

	onMount(async () => {
		// Check auth
		const token = localStorage.getItem('auth_token');
		if (!token) {
			goto('/');
			return;
		}

		await loadVideos();
	});

	async function loadVideos() {
		loading = true;
		try {
			// Ensure we have token
			const token = localStorage.getItem('auth_token');
			if (!token) {
				goto('/');
				return;
			}
			
			const allVideos = await api.getVideos();
			videos = allVideos;
		} catch (error) {
			console.error('Error loading videos:', error);
		} finally {
			loading = false;
		}
	}

	function logout() {
		localStorage.removeItem('auth_token');
		goto('/');
	}

	$: filteredVideos =
		filter === 'all' ? videos : videos.filter((v) => v.status === filter);
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900">
	<!-- Header -->
	<header class="bg-black/30 backdrop-blur-md border-b border-white/10">
		<div class="container mx-auto px-6 py-4">
			<div class="flex items-center justify-between">
				<div class="flex items-center gap-4">
					<RestartButton />
					<h1 class="text-2xl font-bold text-white">AllAboutMe</h1>
				</div>
				<nav class="flex items-center gap-6">
					<a href="/dashboard" class="text-gray-300 hover:text-white transition-colors"
						>Dashboard</a
					>
					<a href="/drafts" class="text-gray-300 hover:text-white transition-colors">Drafts</a>
					<a href="/publish" class="text-white font-semibold">Publish</a>
					<a href="/automation" class="text-gray-300 hover:text-white transition-colors">Automation</a>
					<a href="/settings" class="text-gray-300 hover:text-white transition-colors">Settings</a>
					<LanguageSwitcher />
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
			<!-- Header -->
			<div class="p-6 border-b border-white/10">
				<div class="flex items-center justify-between">
					<h2 class="text-2xl font-bold text-white">📤 Publish Videos</h2>

					<!-- Filter -->
					<div class="flex gap-2">
						<button
							on:click={() => (filter = 'all')}
							class="{filter === 'all' 
								? 'bg-purple-600 text-white' 
								: 'bg-white/10 text-gray-300'} px-4 py-2 rounded-lg text-sm font-semibold transition-all"
						>
							All ({videos.length})
						</button>
						<button
							on:click={() => (filter = 'completed')}
							class="{filter === 'completed' 
								? 'bg-green-600 text-white' 
								: 'bg-white/10 text-gray-300'} px-4 py-2 rounded-lg text-sm font-semibold transition-all"
						>
							Ready ({videos.filter((v) => v.status === 'completed').length})
						</button>
						<button
							on:click={() => (filter = 'pending')}
							class="{filter === 'pending' 
								? 'bg-yellow-600 text-white' 
								: 'bg-white/10 text-gray-300'} px-4 py-2 rounded-lg text-sm font-semibold transition-all"
						>
							Pending ({videos.filter((v) => v.status === 'pending').length})
						</button>
						<button
							on:click={() => (filter = 'failed')}
							class="{filter === 'failed' 
								? 'bg-red-600 text-white' 
								: 'bg-white/10 text-gray-300'} px-4 py-2 rounded-lg text-sm font-semibold transition-all"
						>
							Failed ({videos.filter((v) => v.status === 'failed').length})
						</button>
					</div>
				</div>
			</div>

			<!-- Content -->
			<div class="p-6">
				{#if loading}
					<div class="text-center py-12">
						<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto"></div>
						<p class="text-gray-300 mt-4">Loading videos...</p>
					</div>
				{:else if filteredVideos.length === 0}
					<div class="text-center py-12">
						<div class="text-6xl mb-4">📹</div>
						<p class="text-gray-300 text-lg">No videos found</p>
						<p class="text-gray-400 text-sm mt-2">
							{#if filter === 'completed'}
								No completed videos ready for publishing
							{:else if filter === 'pending'}
								No videos currently being processed
							{:else if filter === 'failed'}
								No failed videos
							{:else}
								Create some videos in the Drafts section first
							{/if}
						</p>
					</div>
				{:else}
					<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
						{#each filteredVideos as video (video.id)}
							<VideoCard {video} onUpdate={loadVideos} />
						{/each}
					</div>
				{/if}
			</div>
		</div>
	</main>
</div>

