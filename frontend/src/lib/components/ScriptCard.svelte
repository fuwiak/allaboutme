<script lang="ts">
	import { api } from '$lib/api';
	import ProgressModal from './ProgressModal.svelte';
	import { videoSettings } from '$lib/videoSettings';
	import { onMount } from 'svelte';

	export let script: any;
	export let onUpdate: () => void;

	let isEditing = false;
	let editedScript = script.script;
	let editedPostText = script.post_text || '';
	let showPostTextModal = false;
	let generatingPostText = false;
	let showProgressModal = false;
	let currentTaskId = '';
	let showVideoSettings = false;
	let generatingBackground = false;
	let playingVoiceSample = false;
	
	// Load settings from global store on mount
	onMount(() => {
		console.log('[ScriptCard] Current global settings:', $videoSettings);
	});
	
	// ElevenLabs voices - using pre-generated samples
	const voices = [
		{
			id: 'pNInz6obpgDQGcFmaJgB',
			name: 'Adam',
			description: 'Deep male - Warm, narrative',
			sampleFile: '/voice-samples/adam.mp3',
			icon: '🎙️'
		},
		{
			id: 'EXAVITQu4vr4xnSDxMaL',
			name: 'Bella',
			description: 'Female - Soft, friendly',
			sampleFile: '/voice-samples/bella.mp3',
			icon: '🎤'
		},
		{
			id: 'TxGEqnHWrfWFTfGW9XjX',
			name: 'Josh',
			description: 'Young male - Energetic',
			sampleFile: '/voice-samples/josh.mp3',
			icon: '🔊'
		}
	];
	
	let currentAudio: HTMLAudioElement | null = null;
	
	async function playVoiceSample(voiceId: string) {
		try {
			// Stop any currently playing audio
			if (currentAudio) {
				currentAudio.pause();
				currentAudio.currentTime = 0;
				currentAudio = null;
			}
			
			const voice = voices.find(v => v.id === voiceId);
			if (!voice) return;
			
			playingVoiceSample = true;
			
			// Play pre-generated ElevenLabs sample
			currentAudio = new Audio(voice.sampleFile);
			currentAudio.volume = 0.9;
			
			currentAudio.onended = () => {
				playingVoiceSample = false;
				currentAudio = null;
			};
			
			currentAudio.onerror = (e) => {
				console.error('Error playing sample:', e);
				playingVoiceSample = false;
				currentAudio = null;
				alert(`Failed to load ${voice.name} sample. Try regenerating voice samples.`);
			};
			
			await currentAudio.play();
			
		} catch (error) {
			console.error('Error playing sample:', error);
			playingVoiceSample = false;
			currentAudio = null;
		}
	}

	async function handleSave() {
		try {
			await api.updateScript(script.id, {
				script: editedScript,
				post_text: editedPostText
			});
			isEditing = false;
			onUpdate();
		} catch (error) {
			alert(`Error saving script: ${error}`);
		}
	}

	async function handleGeneratePostText() {
		generatingPostText = true;
		try {
			const result = await api.generatePostText(script.id);
			editedPostText = result.post_text;
			script.post_text = result.post_text;
			showPostTextModal = true;
		} catch (error) {
			alert(`Error generating post text: ${error}`);
		} finally {
			generatingPostText = false;
		}
	}

	async function handleCreateVideo() {
		if (!editedPostText) {
			const confirm = window.confirm(
				'Post text is empty. Generate it first or use the scenario text?'
			);
			if (!confirm) return;
		}

		// Show video settings first
		showVideoSettings = true;
	}

	async function startVideoGeneration() {
		// Save first
		await handleSave();

		// Use global settings from store
		const settings = $videoSettings;
		
		// Start video generation with ALL settings from store
		try {
			const result = await api.generateVideo(
				script.id, 
				settings.textPosition,
				settings.backgroundUrl || undefined,
				settings.voiceId
			);
			currentTaskId = result.task_id;
			
			console.log('[ScriptCard] Video generation started with GLOBAL settings:', {
				textPosition: settings.textPosition,
				background: settings.backgroundUrl ? 'custom' : 'default',
				voiceId: settings.voiceId,
				taskId: result.task_id
			});
			
			// Close settings modal and show progress modal
			showVideoSettings = false;
			showProgressModal = true;
		} catch (error) {
			alert(`Error creating video: ${error}`);
			showVideoSettings = false;
		}
	}

	async function handleStopVideo() {
		if (!currentTaskId) return;
		
		try {
			await api.cancelTask(currentTaskId);
			showProgressModal = false;
			alert('Video generation stopped');
		} catch (error) {
			alert(`Error stopping video: ${error}`);
		}
	}

	async function generateBackground() {
		generatingBackground = true;
		try {
			// Use theme from global store
			const theme = $videoSettings.backgroundTheme;
			const imageUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(getPromptForTheme(theme))}?width=1920&height=1080&nologo=true`;
			
			console.log('[ScriptCard] Generating background:', theme);
			
			const response = await fetch(imageUrl, { method: 'GET' });
			
			if (!response.ok) throw new Error('Failed to generate image');
			
			const blob = await response.blob();
			const file = new File([blob], `${theme}_background.png`, { type: 'image/png' });
			
			console.log('[ScriptCard] Uploading to backend...');
			
			// Upload to backend FIRST, then use server path
			const result = await api.uploadBackground(file);
			console.log('[ScriptCard] Background uploaded:', result.filename);
			
			// Use server path (this will persist in localStorage)
			const serverPath = `/storage/backgrounds/${result.filename}`;
			
			// Update GLOBAL store with server path
			videoSettings.update(s => ({ 
				...s, 
				backgroundUrl: serverPath
			}));
			
			console.log('[ScriptCard] Background URL saved to store:', serverPath);
			
			alert(`✅ Background generated and saved globally: ${theme}`);
		} catch (error) {
			console.error('[ScriptCard] Background generation error:', error);
			alert(`Error generating background: ${error}`);
		} finally {
			generatingBackground = false;
		}
	}

	function getPromptForTheme(theme: string): string {
		const prompts: Record<string, string> = {
			cosmic: 'Deep space cosmos, nebula colors, spiritual universe, infinite energy, celestial beauty, mystical stars, high quality',
			astrology: 'Mystical zodiac wheel with all 12 signs, cosmic background, stars, planets, ethereal glow, spiritual art, high quality',
			numerology: 'Sacred numerology symbols, golden numbers 1-9 in mystical circle, divine geometry, spiritual energy, cosmic background',
			matrix: 'Destiny matrix energy map, sacred geometry, chakra colors, spiritual pathways, mystical symbols, glowing mandala',
			human_design: 'Human Design body graph, energy centers, spiritual diagram, colorful chakras, cosmic consciousness, mystical blueprint',
			motivation: 'Inspiring cosmic energy, spiritual awakening, golden light, universe connection, meditation vibes, peaceful atmosphere',
			moon: 'Mystical moon phases, intuitive wisdom, celestial magic, spiritual feminine energy, night sky, stars, ethereal glow',
			tarot: 'Mystical tarot cards spread, divine symbols, spiritual guidance, cosmic wisdom, ethereal art, magical atmosphere',
			chakras: 'Seven colorful chakras energy centers, spiritual alignment, cosmic healing, rainbow aura, divine light'
		};
		return prompts[theme] || prompts.cosmic;
	}

	async function handleDelete() {
		if (!confirm('Delete this script?')) return;

		try {
			await api.deleteScript(script.id);
			onUpdate();
		} catch (error) {
			alert(`Error deleting script: ${error}`);
		}
	}
</script>

<div class="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700 hover:border-purple-500/50 transition-all">
	<!-- Header -->
	<div class="flex items-start justify-between mb-4">
		<div class="flex-1">
			<div class="flex items-center gap-2 mb-2">
				<span class="text-xs px-2 py-1 bg-purple-500/20 text-purple-300 rounded">
					{script.theme || 'No theme'}
				</span>
				<span
					class="text-xs px-2 py-1 rounded {script.status === 'approved' 
						? 'bg-green-500/20 text-green-300' 
						: script.status === 'draft' 
						? 'bg-yellow-500/20 text-yellow-300'
						: 'bg-gray-500/20 text-gray-300'}"
				>
					{script.status}
				</span>
			</div>
			<p class="text-sm text-gray-400">ID: {script.id}</p>
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

	<!-- Scenario -->
	<div class="space-y-3">
		<label class="block text-sm font-semibold text-gray-300">📝 Сценарий / Контекст</label>
		{#if isEditing}
			<textarea
				bind:value={editedScript}
				class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
				rows="4"
			/>
		{:else}
			<p class="text-gray-200 whitespace-pre-wrap">{script.script}</p>
		{/if}
	</div>

	<!-- Post Text -->
	<div class="mt-4 space-y-3">
		<div class="flex items-center justify-between">
			<label class="block text-sm font-semibold text-gray-300">🎤 Текст для озвучки</label>
			<button
				on:click={handleGeneratePostText}
				disabled={generatingPostText}
				class="text-xs px-3 py-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded transition-colors"
			>
				{generatingPostText ? 'Generating...' : '✨ Generate'}
			</button>
		</div>
		{#if isEditing}
			<textarea
				bind:value={editedPostText}
				class="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
				rows="4"
				placeholder="Generate clean text for voiceover..."
			/>
		{:else if editedPostText}
			<p class="text-gray-200 whitespace-pre-wrap">{editedPostText}</p>
		{:else}
			<p class="text-gray-500 italic">Not generated yet</p>
		{/if}
	</div>

	<!-- Actions -->
	<div class="flex gap-3 mt-6">
		{#if isEditing}
			<button
				on:click={handleSave}
				class="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors"
			>
				💾 Save
			</button>
			<button
				on:click={() => {
					isEditing = false;
					editedScript = script.script;
					editedPostText = script.post_text || '';
				}}
				class="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white font-semibold rounded-lg transition-colors"
			>
				Cancel
			</button>
		{:else}
			<button
				on:click={() => (isEditing = true)}
				class="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
			>
				✏️ Edit
			</button>
			<button
				on:click={handleCreateVideo}
				class="flex-1 px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold rounded-lg transition-all"
			>
				🎬 Create Video
			</button>
		{/if}
	</div>
</div>

<!-- Video Settings Modal -->
{#if showVideoSettings}
	<div
		class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-start justify-center z-40 pt-20 overflow-y-auto"
		on:click={() => (showVideoSettings = false)}
	>
		<div
			class="bg-gray-800 rounded-lg shadow-2xl w-full max-w-md mx-4 p-6 my-4"
			on:click|stopPropagation
		>
			<h3 class="text-xl font-bold text-white mb-4">🎬 Video Settings</h3>
			
			<!-- Global Settings Banner -->
			<div class="bg-gradient-to-r from-purple-500/20 to-blue-500/20 border border-purple-500/30 rounded-lg p-3 mb-4">
				<p class="text-xs text-purple-200">
					🌐 <strong>Global Settings</strong> - These settings apply to all videos and are saved automatically
				</p>
			</div>

			<div class="space-y-4 mb-6">
				<!-- Text Position -->
				<div>
					<label class="block text-sm font-semibold text-gray-300 mb-2">
						📐 Text Position
					</label>
					<div class="flex gap-2">
						<button
							on:click={() => videoSettings.update(s => ({ ...s, textPosition: 'top' }))}
							class="flex-1 px-4 py-3 rounded-lg border-2 transition-all {$videoSettings.textPosition === 'top'
								? 'border-purple-500 bg-purple-500/20 text-white'
								: 'border-gray-600 bg-gray-900 text-gray-300'}"
						>
							⬆️ Top
						</button>
						<button
							on:click={() => videoSettings.update(s => ({ ...s, textPosition: 'center' }))}
							class="flex-1 px-4 py-3 rounded-lg border-2 transition-all {$videoSettings.textPosition === 'center'
								? 'border-purple-500 bg-purple-500/20 text-white'
								: 'border-gray-600 bg-gray-900 text-gray-300'}"
						>
							⏺️ Center
						</button>
						<button
							on:click={() => videoSettings.update(s => ({ ...s, textPosition: 'bottom' }))}
							class="flex-1 px-4 py-3 rounded-lg border-2 transition-all {$videoSettings.textPosition === 'bottom'
								? 'border-purple-500 bg-purple-500/20 text-white'
								: 'border-gray-600 bg-gray-900 text-gray-300'}"
						>
							⬇️ Bottom
						</button>
					</div>
				</div>

				<!-- Voice Selection -->
				<div>
					<label class="block text-sm font-semibold text-gray-300 mb-2">
						🎤 Voice Selection
					</label>
					<div class="space-y-2">
						{#each voices as voice}
							<div class="flex items-center gap-2 p-3 bg-gray-900 border rounded-lg transition-all {$videoSettings.voiceId === voice.id
								? 'border-purple-500 bg-purple-500/10'
								: 'border-gray-600 hover:border-gray-500'}">
								<input
									type="radio"
									id="voice-{voice.id}"
									name="voice"
									value={voice.id}
									checked={$videoSettings.voiceId === voice.id}
									on:change={() => videoSettings.update(s => ({ ...s, voiceId: voice.id }))}
									class="w-4 h-4 text-purple-600"
								/>
								<label for="voice-{voice.id}" class="flex-1 cursor-pointer">
									<div class="flex items-center gap-2">
										<span class="text-lg">{voice.icon}</span>
										<div class="flex-1">
											<div class="text-sm font-semibold text-white">{voice.name}</div>
											<div class="text-xs text-gray-400">{voice.description}</div>
										</div>
									</div>
								</label>
								<button
									on:click={() => playVoiceSample(voice.id)}
									disabled={playingVoiceSample}
									class="px-3 py-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white text-xs font-semibold rounded transition-colors"
									title="Play sample"
								>
									{#if playingVoiceSample}
										⏸️
									{:else}
										▶️
									{/if}
								</button>
							</div>
						{/each}
					</div>
					<p class="text-xs text-gray-400 mt-2">Click ▶️ to preview voice before generating</p>
				</div>

			<!-- Custom Background -->
			<div>
				<label class="block text-sm font-semibold text-gray-300 mb-2">
					🖼️ Custom Background (Optional)
				</label>
				<p class="text-xs text-gray-400 mb-3">
					⚠️ If empty, background will be auto-detected from script content. Generate custom to override.
				</p>
				
				<!-- Theme Selector -->
				<div class="mb-3">
					<label class="block text-xs text-gray-400 mb-2">✨ Generate AI Background:</label>
					<div class="flex gap-2">
						<select
							value={$videoSettings.backgroundTheme}
							on:change={(e) => videoSettings.update(s => ({ ...s, backgroundTheme: e.currentTarget.value }))}
							class="flex-1 px-3 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white text-sm"
						>
							<option value="cosmic">🌌 Cosmic</option>
							<option value="astrology">🔮 Astrology</option>
							<option value="numerology">🔢 Numerology</option>
							<option value="matrix">💎 Destiny Matrix</option>
							<option value="human_design">🎨 Human Design</option>
							<option value="motivation">✨ Motivation</option>
							<option value="moon">🌙 Moon</option>
							<option value="tarot">🃏 Tarot</option>
							<option value="chakras">⚡ Chakras</option>
						</select>
						<button
							on:click={generateBackground}
							disabled={generatingBackground}
							class="px-4 py-2 bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold rounded-lg transition-all text-sm"
						>
							{#if generatingBackground}
								<span class="flex items-center gap-2">
									<div class="animate-spin rounded-full h-3 w-3 border-2 border-white/30 border-t-white"></div>
									Generating...
								</span>
							{:else}
								🎨 Generate
							{/if}
						</button>
					</div>
					<p class="text-xs text-gray-400 mt-1">Free AI generation via Pollinations.ai</p>
				</div>
				
				<!-- Upload File -->
				<div>
					<label class="block text-xs text-gray-400 mb-2">📁 Or Upload Your Own:</label>
					<input
						type="file"
						accept="image/*"
						on:change={async (e) => {
							const file = e.currentTarget.files?.[0];
							if (file) {
								generatingBackground = true;
								try {
									console.log('[ScriptCard] Uploading custom background...');
									const result = await api.uploadBackground(file);
									console.log('[ScriptCard] Upload result:', result);
									
									// Save to GLOBAL store with server path
									const serverPath = `/storage/backgrounds/${result.filename}`;
									videoSettings.update(s => ({ 
										...s, 
										backgroundUrl: serverPath 
									}));
									
									console.log('[ScriptCard] Background URL saved to store:', serverPath);
									alert(`✅ Background uploaded: ${result.filename}`);
								} catch (error) {
									console.error('[ScriptCard] Upload error:', error);
									alert(`Upload error: ${error}`);
								} finally {
									generatingBackground = false;
								}
							}
						}}
						class="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white text-sm file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-purple-600 file:text-white hover:file:bg-purple-700"
					/>
					<p class="text-xs text-gray-400 mt-1">JPG, PNG, GIF, WebP (max 10MB)</p>
				</div>
				
			<!-- Preview Generated Background -->
			{#if $videoSettings.backgroundUrl}
				<div class="mt-3">
					<div class="relative">
						<img src={$videoSettings.backgroundUrl} alt="Generated background" class="w-full h-32 object-cover rounded-lg border-2 border-green-500" />
						<button
							on:click={() => {
								// Revoke the blob URL to free memory
								if ($videoSettings.backgroundUrl?.startsWith('blob:')) {
									URL.revokeObjectURL($videoSettings.backgroundUrl);
								}
								videoSettings.update(s => ({ ...s, backgroundUrl: null }));
							}}
							class="absolute top-2 right-2 px-2 py-1 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded shadow-lg transition-colors"
							title="Clear background"
						>
							✕
						</button>
					</div>
					<p class="text-xs text-green-400 mt-1">✅ Background ready (global)</p>
				</div>
			{/if}
			</div>
			</div>

			<div class="flex gap-3">
				<button
					on:click={startVideoGeneration}
					class="flex-1 px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold rounded-lg transition-all"
				>
					🎬 Generate Video
				</button>
				<button
					on:click={() => (showVideoSettings = false)}
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
		title="Creating Video"
		onStop={handleStopVideo}
		onClose={() => {
			showProgressModal = false;
			onUpdate();
		}}
	/>
{/if}

<!-- Post Text Modal -->
{#if showPostTextModal}
	<div
		class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-40"
		on:click={() => (showPostTextModal = false)}
	>
		<div
			class="bg-gray-800 rounded-lg shadow-2xl w-full max-w-2xl mx-4 p-6"
			on:click|stopPropagation
		>
			<h3 class="text-xl font-bold text-white mb-4">✨ Generated Post Text</h3>
			<div class="bg-gray-900 p-4 rounded-lg mb-4">
				<p class="text-gray-200 whitespace-pre-wrap">{editedPostText}</p>
			</div>
			<div class="flex justify-end gap-3">
				<button
					on:click={() => {
						isEditing = true;
						showPostTextModal = false;
					}}
					class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
				>
					Edit
				</button>
				<button
					on:click={() => (showPostTextModal = false)}
					class="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
				>
					Close
				</button>
			</div>
		</div>
	</div>
{/if}

