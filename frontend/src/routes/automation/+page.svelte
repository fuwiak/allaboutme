<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import { t } from '$lib/i18n';
	import LanguageSwitcher from '$lib/components/LanguageSwitcher.svelte';
	import RestartButton from '$lib/components/RestartButton.svelte';

	let automationEnabled = false;
	let pendingPosts = 0;
	let publishedToday = 0;
	let currentLanguage = 'ru';
	let languages: any[] = [];
	let logs: any[] = [];
	let loading = true;
	
	// Schedule settings
	let scheduleSettings = {
		post_interval_minutes: 30,
		start_hour: 7,
		end_hour: 24,
		min_posts_per_day: 10,
		max_posts_per_day: 15
	};
	let savingSchedule = false;

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
			const [status, langs, logsData, settings] = await Promise.all([
				fetch('/api/automation/status', {
					headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
				}).then(r => r.json()),
				fetch('/api/automation/languages', {
					headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
				}).then(r => r.json()),
				fetch('/api/automation/logs?limit=20', {
					headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
				}).then(r => r.json()),
				api.getSettings()
			]);

			automationEnabled = status.enabled;
			pendingPosts = status.pending_posts;
			publishedToday = status.published_today;

			languages = langs.languages;
			currentLanguage = languages.find((l: any) => l.is_active)?.code || 'ru';

			logs = logsData.logs;
			
			// Load schedule settings from backend
			if (settings.post_interval_minutes) scheduleSettings.post_interval_minutes = parseInt(settings.post_interval_minutes) || 30;
			if (settings.start_hour) scheduleSettings.start_hour = parseInt(settings.start_hour) || 7;
			if (settings.end_hour) scheduleSettings.end_hour = parseInt(settings.end_hour) || 24;
			if (settings.min_posts_per_day) scheduleSettings.min_posts_per_day = parseInt(settings.min_posts_per_day) || 10;
			if (settings.max_posts_per_day) scheduleSettings.max_posts_per_day = parseInt(settings.max_posts_per_day) || 15;
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
	
	async function saveScheduleSettings() {
		savingSchedule = true;
		try {
			// Validate settings
			if (scheduleSettings.start_hour < 0 || scheduleSettings.start_hour > 23) {
				alert('Start hour must be between 0-23');
				savingSchedule = false;
				return;
			}
			if (scheduleSettings.end_hour < 1 || scheduleSettings.end_hour > 24) {
				alert('End hour must be between 1-24');
				savingSchedule = false;
				return;
			}
			if (scheduleSettings.start_hour >= scheduleSettings.end_hour) {
				alert('Start hour must be before end hour');
				savingSchedule = false;
				return;
			}
			if (scheduleSettings.post_interval_minutes < 5) {
				alert('Interval must be at least 5 minutes');
				savingSchedule = false;
				return;
			}
			if (scheduleSettings.min_posts_per_day > scheduleSettings.max_posts_per_day) {
				alert('Min posts must be ≤ max posts');
				savingSchedule = false;
				return;
			}
			
			// Save to backend
			await api.updateSettings({
				post_interval_minutes: scheduleSettings.post_interval_minutes.toString(),
				start_hour: scheduleSettings.start_hour.toString(),
				end_hour: scheduleSettings.end_hour.toString(),
				min_posts_per_day: scheduleSettings.min_posts_per_day.toString(),
				max_posts_per_day: scheduleSettings.max_posts_per_day.toString()
			});
			
			alert('✅ Schedule settings saved!');
		} catch (error: any) {
			alert(`Error: ${error.message}`);
		} finally {
			savingSchedule = false;
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
					<a href="/dashboard" class="text-gray-300 hover:text-white transition-colors">{$t('nav.dashboard')}</a>
					<a href="/drafts" class="text-gray-300 hover:text-white transition-colors">{$t('nav.drafts')}</a>
					<a href="/publish" class="text-gray-300 hover:text-white transition-colors">{$t('nav.publish')}</a>
					<a href="/automation" class="text-white font-semibold">{$t('nav.automation')}</a>
					<a href="/settings" class="text-gray-300 hover:text-white transition-colors">{$t('nav.settings')}</a>
					<LanguageSwitcher />
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

			<!-- Schedule Settings -->
			<div class="bg-white/10 backdrop-blur-md rounded-lg border border-white/20 p-6 mb-6">
				<h3 class="text-xl font-bold text-white mb-4">⏰ Настройки Расписания</h3>
				
				<div class="grid grid-cols-2 gap-6 mb-6">
					<!-- Post Interval -->
					<div>
						<label class="block text-sm font-semibold text-gray-300 mb-2">
							📅 Интервал между постами (минуты)
						</label>
						<input
							type="number"
							bind:value={scheduleSettings.post_interval_minutes}
							min="5"
							max="180"
							class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
						/>
						<p class="text-xs text-gray-400 mt-1">Минимум: 5 минут</p>
					</div>

					<!-- Time Range -->
					<div>
						<label class="block text-sm font-semibold text-gray-300 mb-2">
							🕐 Часы работы
						</label>
						<div class="flex gap-2 items-center">
							<input
								type="number"
								bind:value={scheduleSettings.start_hour}
								min="0"
								max="23"
								placeholder="7"
								class="flex-1 px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
							/>
							<span class="text-white font-bold">—</span>
							<input
								type="number"
								bind:value={scheduleSettings.end_hour}
								min="1"
								max="24"
								placeholder="24"
								class="flex-1 px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
							/>
						</div>
						<p class="text-xs text-gray-400 mt-1">
							С {scheduleSettings.start_hour}:00 до {scheduleSettings.end_hour}:00
						</p>
					</div>

					<!-- Min Posts Per Day -->
					<div>
						<label class="block text-sm font-semibold text-gray-300 mb-2">
							📊 Минимум постов в день
						</label>
						<input
							type="number"
							bind:value={scheduleSettings.min_posts_per_day}
							min="1"
							max="50"
							class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
						/>
						<p class="text-xs text-gray-400 mt-1">Минимум постов для публикации</p>
					</div>

					<!-- Max Posts Per Day -->
					<div>
						<label class="block text-sm font-semibold text-gray-300 mb-2">
							📈 Максимум постов в день
						</label>
						<input
							type="number"
							bind:value={scheduleSettings.max_posts_per_day}
							min="1"
							max="50"
							class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
						/>
						<p class="text-xs text-gray-400 mt-1">Максимум постов для публикации</p>
					</div>
				</div>

				<!-- Calculated Stats -->
				<div class="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4 mb-4">
					<h4 class="text-sm font-semibold text-purple-300 mb-2">📊 Рассчитанные параметры:</h4>
					<div class="grid grid-cols-3 gap-4 text-sm">
						<div>
							<span class="text-gray-400">Рабочих часов:</span>
							<span class="text-white font-bold ml-2">
								{scheduleSettings.end_hour - scheduleSettings.start_hour} ч
							</span>
						</div>
						<div>
							<span class="text-gray-400">Постов в час:</span>
							<span class="text-white font-bold ml-2">
								{Math.round(60 / scheduleSettings.post_interval_minutes * 10) / 10}
							</span>
						</div>
						<div>
							<span class="text-gray-400">Макс. за день:</span>
							<span class="text-white font-bold ml-2">
								{Math.floor((scheduleSettings.end_hour - scheduleSettings.start_hour) * 60 / scheduleSettings.post_interval_minutes)}
							</span>
						</div>
					</div>
				</div>

				<!-- Save Button -->
				<button
					on:click={saveScheduleSettings}
					disabled={savingSchedule}
					class="w-full py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold rounded-lg transition-all disabled:cursor-not-allowed"
				>
					{savingSchedule ? '💾 Сохранение...' : '💾 Сохранить Расписание'}
				</button>
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

