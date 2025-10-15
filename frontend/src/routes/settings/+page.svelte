<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import { t } from '$lib/i18n';
	import LanguageSwitcher from '$lib/components/LanguageSwitcher.svelte';
	import RestartButton from '$lib/components/RestartButton.svelte';

	let loading = true;

	onMount(async () => {
		// Check auth
		const token = localStorage.getItem('auth_token');
		if (!token) {
			console.log('No token found, redirecting to login');
			goto('/');
			return;
		}

		console.log('Token found, settings page loaded');
		loading = false;
	});


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
					<a href="/dashboard" class="text-gray-300 hover:text-white transition-colors"
						>{$t('nav.dashboard')}</a
					>
					<a href="/drafts" class="text-gray-300 hover:text-white transition-colors">{$t('nav.drafts')}</a>
					<a href="/publish" class="text-gray-300 hover:text-white transition-colors">{$t('nav.publish')}</a>
					<a href="/automation" class="text-gray-300 hover:text-white transition-colors">{$t('nav.automation')}</a>
					<a href="/settings" class="text-white font-semibold">{$t('nav.settings')}</a>
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
			<!-- Single Tab (API Tokens only) -->
			<div class="flex border-b border-white/10">
				<button
					class="px-6 py-4 font-semibold transition-all bg-purple-600 text-white"
				>
					🔐 API Tokens
				</button>
			</div>

			<!-- Content -->
			<div class="p-6">
				{#if loading}
					<div class="text-center py-12">
						<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto"></div>
						<p class="text-gray-300 mt-4">Loading settings...</p>
					</div>
				{:else}
					<!-- API Tokens (Read-only) -->
					<div class="space-y-6">
						<p class="text-sm text-gray-400 mb-4">
							Note: For security, API tokens are stored as environment variables on the server.
							These fields are read-only placeholders.
						</p>

						<div class="space-y-4 opacity-60">
							<div>
								<label class="block text-sm font-semibold text-gray-300 mb-2">
									GROQ API Key
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
									ElevenLabs API Key
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
						
						<div class="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4 mt-4">
							<p class="text-sm text-purple-300">
								🎨 <strong>Video settings removed!</strong> Voice, background, and text position are now configured per-video in the "Drafts" tab when you click "Create Video".
							</p>
						</div>
					</div>
				{/if}
			</div>
		</div>
	</main>
</div>

