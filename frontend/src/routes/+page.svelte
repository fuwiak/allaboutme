<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import { authStore } from '$lib/stores';

	let username = '';
	let password = '';
	let error = '';
	let loading = false;

	async function handleLogin() {
		error = '';
		loading = true;

		try {
			const result = await api.login(username, password);
			console.log('Login successful, token:', result.access_token.substring(0, 20) + '...');
			
			// Verify token is saved
			const savedToken = localStorage.getItem('auth_token');
			console.log('Token saved in localStorage:', savedToken ? 'YES' : 'NO');
			
			authStore.set({ isAuthenticated: true, username });
			goto('/dashboard');
		} catch (e: any) {
			error = e.message || 'Login failed';
			console.error('Login error:', e);
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		// Check if already logged in
		const token = localStorage.getItem('auth_token');
		if (token) {
			goto('/dashboard');
		}
	});
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-blue-900 to-black">
	<div class="bg-white/10 backdrop-blur-md p-8 rounded-lg shadow-2xl w-full max-w-md">
		<h1 class="text-4xl font-bold text-white mb-2 text-center">AllAboutMe</h1>
		<p class="text-gray-300 text-center mb-8">Video Generation Platform</p>

		<form on:submit|preventDefault={handleLogin} class="space-y-6">
			<div>
				<label for="username" class="block text-sm font-medium text-gray-200 mb-2">
					Username
				</label>
				<input
					type="text"
					id="username"
					bind:value={username}
					required
					class="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
					placeholder="Enter username"
				/>
			</div>

			<div>
				<label for="password" class="block text-sm font-medium text-gray-200 mb-2">
					Password
				</label>
				<input
					type="password"
					id="password"
					bind:value={password}
					required
					class="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
					placeholder="Enter password"
				/>
			</div>

			{#if error}
				<div class="bg-red-500/20 border border-red-500 text-red-200 px-4 py-3 rounded-lg">
					{error}
				</div>
			{/if}

			<button
				type="submit"
				disabled={loading}
				class="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
			>
				{loading ? 'Logging in...' : 'Login'}
			</button>
		</form>

		<p class="text-gray-400 text-sm text-center mt-6">
			Default: admin / admin123
		</p>
	</div>
</div>

