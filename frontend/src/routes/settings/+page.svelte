<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';

	let settings: Record<string, string> = {};
	let loading = true;
	let saving = false;
	let activeTab: 'content' | 'tokens' | 'video' = 'content';

	onMount(async () => {
		// Check auth
		const token = localStorage.getItem('auth_token');
		if (!token) {
			console.log('No token found, redirecting to login');
			goto('/');
			return;
		}

		console.log('Token found, loading settings...');
		await loadSettings();
	});

	async function loadSettings() {
		loading = true;
		try {
			// Ensure we have token
			const token = localStorage.getItem('auth_token');
			if (!token) {
				goto('/');
				return;
			}
			
			settings = await api.getSettings();
		} catch (error) {
			console.error('Error loading settings:', error);
		} finally {
			loading = false;
		}
	}

	async function saveSettings() {
		saving = true;
		try {
			await api.updateSettings(settings);
			alert('Settings saved successfully!');
		} catch (error: any) {
			alert(`Error saving settings: ${error.message}`);
		} finally {
			saving = false;
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
					<a href="/drafts" class="text-gray-300 hover:text-white transition-colors">Drafts</a>
					<a href="/publish" class="text-gray-300 hover:text-white transition-colors">Publish</a>
					<a href="/settings" class="text-white font-semibold">Settings</a>
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
					on:click={() => (activeTab = 'content')}
					class="px-6 py-4 font-semibold transition-all"
					class:bg-purple-600={activeTab === 'content'}
					class:text-white={activeTab === 'content'}
					class:text-gray-300={activeTab !== 'content'}
				>
					📝 Content Settings
				</button>
				<button
					on:click={() => (activeTab = 'tokens')}
					class="px-6 py-4 font-semibold transition-all"
					class:bg-purple-600={activeTab === 'tokens'}
					class:text-white={activeTab === 'tokens'}
					class:text-gray-300={activeTab !== 'tokens'}
				>
					🔐 API Tokens
				</button>
				<button
					on:click={() => (activeTab = 'video')}
					class="px-6 py-4 font-semibold transition-all"
					class:bg-purple-600={activeTab === 'video'}
					class:text-white={activeTab === 'video'}
					class:text-gray-300={activeTab !== 'video'}
				>
					🎥 Video Generator
				</button>
			</div>

			<!-- Content -->
			<div class="p-6">
				{#if loading}
					<div class="text-center py-12">
						<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto"></div>
						<p class="text-gray-300 mt-4">Loading settings...</p>
					</div>
				{:else if activeTab === 'content'}
					<div class="space-y-6">
						<div>
							<label class="block text-sm font-semibold text-gray-300 mb-2">
								Daily Videos
							</label>
							<input
								type="number"
								bind:value={settings.daily_videos}
								class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
							/>
						</div>

						<div>
							<label class="block text-sm font-semibold text-gray-300 mb-2">
								Themes (comma-separated)
							</label>
							<textarea
								bind:value={settings.themes}
								rows="3"
								class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
							/>
						</div>

						<div>
							<label class="block text-sm font-semibold text-gray-300 mb-2">
								System Prompt
							</label>
							<textarea
								bind:value={settings.system_prompt}
								rows="4"
								class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
							/>
						</div>

						<div>
							<label class="block text-sm font-semibold text-gray-300 mb-2">
								Caption Template
							</label>
							<textarea
								bind:value={settings.caption_template}
								rows="3"
								class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
							/>
							<p class="text-xs text-gray-400 mt-1">Use {'{hook}'} as placeholder</p>
						</div>
					</div>
				{:else if activeTab === 'tokens'}
					<div class="space-y-6">
						<p class="text-sm text-gray-400 mb-4">
							Note: For security, API tokens are stored as environment variables on the server.
							These fields are read-only placeholders.
						</p>

						<div class="space-y-4 opacity-60">
							<div>
								<label class="block text-sm font-semibold text-gray-300 mb-2">
									Groq API Key
								</label>
								<input
									type="password"
									value="••••••••••••••••"
									disabled
									class="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg text-gray-500 cursor-not-allowed"
								/>
							</div>

							<div>
								<label class="block text-sm font-semibold text-gray-300 mb-2">
									HeyGen API Key
								</label>
								<input
									type="password"
									value="••••••••••••••••"
									disabled
									class="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg text-gray-500 cursor-not-allowed"
								/>
							</div>

							<div>
								<label class="block text-sm font-semibold text-gray-300 mb-2">
									Telegram Bot Token
								</label>
								<input
									type="password"
									value="••••••••••••••••"
									disabled
									class="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg text-gray-500 cursor-not-allowed"
								/>
							</div>
						</div>

						<div class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
							<p class="text-sm text-blue-300">
								💡 To update API tokens, modify the environment variables on Railway or in your
								.env file.
							</p>
						</div>
					</div>
				{:else}
					<div class="space-y-6">
						<div>
							<label class="block text-sm font-semibold text-gray-300 mb-2">
								Video Generator
							</label>
							<select
								bind:value={settings.video_generator}
								class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
							>
								<option value="heygen">HeyGen (Paid, High Quality)</option>
								<option value="opensource">Open Source (Free)</option>
							</select>
						</div>

						<div>
							<label class="block text-sm font-semibold text-gray-300 mb-2">
								Video Duration (seconds)
							</label>
							<input
								type="number"
								bind:value={settings.video_duration}
								class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
							/>
						</div>

						<div>
							<label class="block text-sm font-semibold text-gray-300 mb-2">
								HeyGen Voice
							</label>
							<input
								type="text"
								bind:value={settings.heygen_voice}
								class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
							/>
						</div>

						<div>
							<label class="block text-sm font-semibold text-gray-300 mb-2">
								Open Source Background
							</label>
							<select
								bind:value={settings.opensource_background}
								class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
							>
								<option value="space">Space</option>
								<option value="planets">Planets</option>
								<option value="mystical">Mystical</option>
								<option value="astrology">Astrology</option>
							</select>
						</div>

						<div class="flex items-center gap-3">
							<input
								type="checkbox"
								id="subtitles"
								checked={settings.opensource_add_subtitles === 'true'}
								on:change={(e) =>
									(settings.opensource_add_subtitles = e.currentTarget.checked
										? 'true'
										: 'false')}
								class="w-5 h-5 rounded bg-gray-900 border-gray-600 text-purple-600 focus:ring-2 focus:ring-purple-500"
							/>
							<label for="subtitles" class="text-sm font-semibold text-gray-300">
								Add Subtitles (Open Source)
							</label>
						</div>
					</div>
				{/if}

				<!-- Save Button -->
				<div class="flex justify-end mt-8 pt-6 border-t border-white/10">
					<button
						on:click={saveSettings}
						disabled={saving}
						class="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold rounded-lg transition-all"
					>
						{saving ? 'Saving...' : '💾 Save Settings'}
					</button>
				</div>
			</div>
		</div>
	</main>
</div>

