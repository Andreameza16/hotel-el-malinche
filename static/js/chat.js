
	import { createChat } from 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/chat.bundle.es.js';

	createChat({
	webhookUrl: 'https://andreameza16.app.n8n.cloud/webhook/3fba594f-70f7-4322-be9b-126f4cd30faf/chat',
	webhookConfig: {
		method: 'POST',
		headers: {}
	},
	target: '#n8n-chat',
	mode: 'window',
	chatInputKey: 'chatInput',
	chatSessionKey: 'sessionId',
	loadPreviousSession: true,
	metadata: {},
	showWelcomeScreen: false,
	defaultLanguage: 'en',
	initialMessages: [
		"🌿 ¡Hola! Soy **MalinBot**, tu asistente del Hotel El Malinche.",
      "¿Deseas conocer nuestras promociones, habitaciones o actividades ecológicas?"
	],
	i18n: {
		en: {
			title: 'MalinBot 🌿',
			subtitle: "Asistente Virtual del Hotel El Malinche",
			footer: '',
			getStarted: 'New Conversation',
			inputPlaceholder: 'Escribe tu pregunta..',
		},
	},
	enableStreaming: false,
});
