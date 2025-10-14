<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import { scriptsStore, videosStore } from '$lib/stores';
	import { t } from '$lib/i18n';
	import ProgressModal from '$lib/components/ProgressModal.svelte';
	import LanguageSwitcher from '$lib/components/LanguageSwitcher.svelte';
	import RestartButton from '$lib/components/RestartButton.svelte';

	let stats = {
		totalScripts: 0,
		totalVideos: 0,
		completedVideos: 0,
		pendingVideos: 0
	};

	let showProgressModal = false;
	let currentTaskId = '';
	let generating = false;

	onMount(async () => {
		// Check auth
		const token = localStorage.getItem('auth_token');
		if (!token) {
			goto('/');
			return;
		}

		await loadStats();
	});

	async function loadStats() {
		try {
			// Ensure we have token before making requests
			const token = localStorage.getItem('auth_token');
			if (!token) {
				goto('/');
				return;
			}
			
			const [scripts, videos] = await Promise.all([api.getScripts(), api.getVideos()]);

			scriptsStore.set(scripts);
			videosStore.set(videos);

			stats.totalScripts = scripts.length;
			stats.totalVideos = videos.length;
			stats.completedVideos = videos.filter((v: any) => v.status === 'completed').length;
			stats.pendingVideos = videos.filter((v: any) => v.status === 'pending').length;
		} catch (error) {
			console.error('Error loading stats:', error);
		}
	}

	async function handleGenerateScripts() {
		generating = true;
		try {
			const result = await api.generateScripts(2);
			currentTaskId = result.task_id;
			showProgressModal = true;
		} catch (error: any) {
			alert(`Error: ${error.message}`);
		} finally {
			generating = false;
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
				<div class="flex items-center gap-4">
					<RestartButton />
					<h1 class="text-2xl font-bold text-white">AllAboutMe</h1>
				</div>
				<nav class="flex items-center gap-6">
					<a href="/dashboard" class="text-white font-semibold">{$t('nav.dashboard')}</a>
					<a href="/drafts" class="text-gray-300 hover:text-white transition-colors">{$t('nav.drafts')}</a>
					<a href="/publish" class="text-gray-300 hover:text-white transition-colors">{$t('nav.publish')}</a>
					<a href="/automation" class="text-gray-300 hover:text-white transition-colors">{$t('nav.automation')}</a>
					<a href="/settings" class="text-gray-300 hover:text-white transition-colors">{$t('nav.settings')}</a>
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
		<!-- Stats Cards -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
			<div
				class="bg-white/10 backdrop-blur-md rounded-lg p-6 border border-white/20 hover:border-purple-500/50 transition-all"
			>
				<div class="flex items-center justify-between">
					<div>
						<p class="text-gray-300 text-sm">{$t('common.loading').includes('...') ? 'Scripts' : 'Скрипты'}</p>
						<p class="text-3xl font-bold text-white mt-2">{stats.totalScripts}</p>
					</div>
					<div class="text-4xl">📝</div>
				</div>
			</div>

			<div
				class="bg-white/10 backdrop-blur-md rounded-lg p-6 border border-white/20 hover:border-blue-500/50 transition-all"
			>
				<div class="flex items-center justify-between">
					<div>
						<p class="text-gray-300 text-sm">{$t('common.loading').includes('...') ? 'Videos' : 'Видео'}</p>
						<p class="text-3xl font-bold text-white mt-2">{stats.totalVideos}</p>
					</div>
					<div class="text-4xl">🎥</div>
				</div>
			</div>

			<div
				class="bg-white/10 backdrop-blur-md rounded-lg p-6 border border-white/20 hover:border-green-500/50 transition-all"
			>
				<div class="flex items-center justify-between">
					<div>
						<p class="text-gray-300 text-sm">{$t('common.loading').includes('...') ? 'Completed' : 'Готово'}</p>
						<p class="text-3xl font-bold text-white mt-2">{stats.completedVideos}</p>
					</div>
					<div class="text-4xl">✅</div>
				</div>
			</div>

			<div
				class="bg-white/10 backdrop-blur-md rounded-lg p-6 border border-white/20 hover:border-yellow-500/50 transition-all"
			>
				<div class="flex items-center justify-between">
					<div>
						<p class="text-gray-300 text-sm">{$t('common.loading').includes('...') ? 'Pending' : 'В очереди'}</p>
						<p class="text-3xl font-bold text-white mt-2">{stats.pendingVideos}</p>
					</div>
					<div class="text-4xl">⏳</div>
				</div>
			</div>
		</div>

		<!-- Quick Actions -->
		<div class="bg-white/10 backdrop-blur-md rounded-lg p-8 border border-white/20 mb-8">
			<h2 class="text-2xl font-bold text-white mb-6">{$t('common.loading').includes('...') ? 'Quick Actions' : 'Быстрые Действия'}</h2>
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<button
					on:click={handleGenerateScripts}
					disabled={generating}
					class="p-6 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 rounded-lg text-white font-semibold transition-all transform hover:scale-105"
				>
					<div class="text-3xl mb-2">✨</div>
					<div>{generating ? $t('dashboard.generatingScripts') : $t('dashboard.generate')}</div>
				</button>

				<button
					on:click={() => goto('/drafts')}
					class="p-6 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 rounded-lg text-white font-semibold transition-all transform hover:scale-105"
				>
					<div class="text-3xl mb-2">📋</div>
					<div>{$t('common.loading').includes('...') ? 'Manage Drafts' : 'Управление Черновиками'}</div>
				</button>

				<button
					on:click={() => goto('/publish')}
					class="p-6 bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 rounded-lg text-white font-semibold transition-all transform hover:scale-105"
				>
					<div class="text-3xl mb-2">📤</div>
					<div>{$t('common.loading').includes('...') ? 'Publish Videos' : 'Публикация Видео'}</div>
				</button>
			</div>
		</div>

		<!-- Welcome Message -->
		<div class="bg-white/5 backdrop-blur-md rounded-lg p-6 border border-white/10">
			<h3 class="text-xl font-bold text-white mb-2">{$t('common.loading').includes('...') ? 'Welcome to AllAboutMe!' : 'Добро пожаловать в AllAboutMe!'}</h3>
			<p class="text-gray-300">
				{$t('common.loading').includes('...') 
					? 'Your AI-powered video generation platform. Generate scripts, create videos, and publish to multiple platforms - all from one place.'
					: 'Ваша AI-платформа для генерации видео. Создавайте скрипты, видео и публикуйте на разных платформах - всё в одном месте.'}
			</p>
		</div>
	</main>
</div>

<!-- Progress Modal -->
{#if showProgressModal}
	<ProgressModal
		taskId={currentTaskId}
		title={$t('dashboard.generatingScripts')}
		onClose={() => {
			showProgressModal = false;
			loadStats();
		}}
	/>
{/if}

