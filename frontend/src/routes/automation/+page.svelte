<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';

	let automationEnabled = false;
	let pendingPosts = 0;
	let publishedToday = 0;
	let currentLanguage = 'ru';
	let languages: any[] = [];
	let logs: any[] = [];
	let loading = true;

	onMount(async () => {
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
			const [status, langs, logsData] = await Promise.all([
				fetch('/api/automation/status', {
					headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
				}).then(r => r.json()),
				fetch('/api/automation/languages', {
					headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
				}).then(r => r.json()),
				fetch('/api/automation/logs?limit=20', {
					headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
				}).then(r => r.json())
			]);

			automationEnabled = status.enabled;
			pendingPosts = status.pending_posts;
			publishedToday = status.published_today;

			languages = langs.languages;
			currentLanguage = languages.find((l: any) => l.is_active)?.code || 'ru';

			logs = logsData.logs;
		} catch (error) {
			console.error('Error loading automation data:', error);
		} finally {
			loading = false;
		}
	}

	async function toggleAutomation() {
		try {
			const endpoint = automationEnabled ? '/api/automation/disable' : '/api/automation/enable';
			await fetch(endpoint, {
				method: 'POST',
				headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
			});

			automationEnabled = !automationEnabled;
			alert(automationEnabled ? 'Automation enabled!' : 'Automation disabled');
		} catch (error: any) {
			alert(`Error: ${error.message}`);
		}
	}

	async function switchLanguage(code: string) {
		try {
			await fetch(`/api/automation/languages/${code}/activate`, {
				method: 'POST',
				headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
			});

			currentLanguage = code;
			languages = languages.map((l) => ({ ...l, is_active: l.code === code }));
			alert(`Language switched to ${code.toUpperCase()}`);
		} catch (error: any) {
			alert(`Error: ${error.message}`);
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
					<a href="/dashboard" class="text-gray-300 hover:text-white transition-colors">Dashboard</a>
					<a href="/drafts" class="text-gray-300 hover:text-white transition-colors">Drafts</a>
					<a href="/publish" class="text-gray-300 hover:text-white transition-colors">Publish</a>
					<a href="/automation" class="text-white font-semibold">Automation</a>
					<a href="/settings" class="text-gray-300 hover:text-white transition-colors">Settings</a>
					<button on:click={logout} class="text-red-300 hover:text-red-200 transition-colors text-sm">
						Logout
					</button>
				</nav>
			</div>
		</div>
	</header>

	<!-- Main Content -->
	<main class="container mx-auto px-6 py-8">
		{#if loading}
			<div class="text-center py-12">
				<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto"></div>
				<p class="text-gray-300 mt-4">Loading...</p>
			</div>
		{:else}
			<!-- Automation Control -->
			<div class="bg-white/10 backdrop-blur-md rounded-lg border border-white/20 p-6 mb-6">
				<div class="flex items-center justify-between mb-6">
					<div>
						<h2 class="text-2xl font-bold text-white mb-2">🤖 Автономная Работа</h2>
						<p class="text-gray-300 text-sm">
							Система автоматически генерирует и публикует видео по расписанию
						</p>
					</div>
					
					<!-- Enable/Disable Toggle -->
					<button
						on:click={toggleAutomation}
						class="px-8 py-4 rounded-lg font-bold text-lg transition-all transform hover:scale-105 {automationEnabled
							? 'bg-gradient-to-r from-green-600 to-emerald-600 text-white'
							: 'bg-gradient-to-r from-gray-600 to-gray-700 text-gray-300'}"
					>
						{automationEnabled ? '✅ Включено' : '⏸️ Выключено'}
					</button>
				</div>

				<!-- Stats -->
				<div class="grid grid-cols-2 gap-4">
					<div class="bg-white/5 rounded-lg p-4">
						<p class="text-gray-400 text-sm">Ожидают публикации</p>
						<p class="text-3xl font-bold text-white mt-2">{pendingPosts}</p>
					</div>
					<div class="bg-white/5 rounded-lg p-4">
						<p class="text-gray-400 text-sm">Опубликовано сегодня</p>
						<p class="text-3xl font-bold text-white mt-2">{publishedToday}</p>
					</div>
				</div>
			</div>

			<!-- Language Switcher -->
			<div class="bg-white/10 backdrop-blur-md rounded-lg border border-white/20 p-6 mb-6">
				<h3 class="text-xl font-bold text-white mb-4">🌍 Язык Контента</h3>
				<div class="flex gap-4">
					{#each languages as lang}
						<button
							on:click={() => switchLanguage(lang.code)}
							class="flex-1 px-6 py-4 rounded-lg font-semibold text-lg transition-all {lang.is_active
								? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white border-2 border-white/30'
								: 'bg-white/5 text-gray-300 hover:bg-white/10'}"
						>
							{lang.code === 'ru' ? '🇷🇺 Русский' : '🇬🇧 English'}
						</button>
					{/each}
				</div>
				<p class="text-gray-400 text-sm mt-3">
					Текущий язык: <span class="text-white font-semibold">{currentLanguage.toUpperCase()}</span>
				</p>
			</div>

			<!-- Automation Logs -->
			<div class="bg-white/10 backdrop-blur-md rounded-lg border border-white/20 p-6">
				<h3 class="text-xl font-bold text-white mb-4">📋 Логи Автоматизации</h3>
				
				{#if logs.length === 0}
					<p class="text-gray-400 text-center py-8">Нет логов</p>
				{:else}
					<div class="space-y-2 max-h-96 overflow-y-auto">
						{#each logs as log}
							<div
								class="p-3 rounded-lg {log.level === 'ERROR'
									? 'bg-red-500/10 border border-red-500/30'
									: log.level === 'WARNING'
									? 'bg-yellow-500/10 border border-yellow-500/30'
									: 'bg-blue-500/10 border border-blue-500/30'}"
							>
								<div class="flex items-start justify-between">
									<div class="flex-1">
										<div class="flex items-center gap-2 mb-1">
											<span class="text-xs font-semibold {log.level === 'ERROR'
												? 'text-red-300'
												: log.level === 'WARNING'
												? 'text-yellow-300'
												: 'text-blue-300'}">
												{log.level}
											</span>
											<span class="text-xs text-gray-400">
												{new Date(log.created_at).toLocaleString('ru-RU')}
											</span>
										</div>
										<p class="text-sm text-white">{log.message}</p>
										{#if log.details}
											<p class="text-xs text-gray-400 mt-1 font-mono">{log.details}</p>
										{/if}
									</div>
									{#if log.notified}
										<span class="text-xs text-green-400">✓ Sent</span>
									{/if}
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		{/if}
	</main>
</div>

