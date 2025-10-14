/**
 * WebSocket client for real-time progress updates
 */

export interface ProgressUpdate {
	video_id?: number;
	status: string;
	elapsed: number;
	task_id: string;
	progress?: number;
}

export function connectProgress(
	taskId: string,
	onUpdate: (data: ProgressUpdate) => void,
	onError?: (error: Event) => void
): WebSocket {
	const wsUrl = `ws://localhost:8000/ws/progress/${taskId}`;
	const ws = new WebSocket(wsUrl);

	ws.onopen = () => {
		console.log(`WebSocket connected for task: ${taskId}`);
	};

	ws.onmessage = (event) => {
		try {
			const data = JSON.parse(event.data);
			onUpdate(data);

			// Auto-close on completion or failure
			if (data.status === 'completed' || data.status === 'failed') {
				setTimeout(() => ws.close(), 1000);
			}
		} catch (error) {
			console.error('Error parsing WebSocket message:', error);
		}
	};

	ws.onerror = (error) => {
		console.error('WebSocket error:', error);
		if (onError) onError(error);
	};

	ws.onclose = () => {
		console.log(`WebSocket closed for task: ${taskId}`);
	};

	return ws;
}

