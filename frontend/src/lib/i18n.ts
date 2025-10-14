import { writable, derived } from 'svelte/store';

export type Language = 'en' | 'ru';

// Translation dictionaries
const translations = {
  en: {
    // Navigation
    nav: {
      dashboard: 'Dashboard',
      drafts: 'Drafts',
      publish: 'Publish',
      settings: 'Settings',
      automation: 'Automation'
    },
    
    // Dashboard
    dashboard: {
      title: 'Generate Scripts',
      theme: 'Theme',
      selectTheme: 'Select a theme',
      count: 'Number of scripts',
      generate: 'Generate Scripts',
      generatingScripts: 'Generating Scripts',
      scriptsGenerated: 'Scripts generated successfully!'
    },
    
    // Drafts
    drafts: {
      title: 'Script Drafts',
      noScripts: 'No scripts yet. Generate some!',
      edit: 'Edit',
      save: 'Save',
      cancel: 'Cancel',
      delete: 'Delete',
      createVideo: 'Create Video',
      videoSettings: 'Video Settings',
      textPosition: 'Text Position',
      top: 'Top',
      center: 'Center',
      bottom: 'Bottom',
      customBackground: 'Custom Background',
      uploadBackground: 'Upload Background',
      start: 'Start',
      generatingVideo: 'Generating Video',
      videoGenerated: 'Video generated successfully!'
    },
    
    // Publish
    publish: {
      title: 'Ready to Publish',
      noVideos: 'No videos yet. Create some from drafts!',
      videoPreview: 'Video Preview',
      audioPreview: 'Audio Preview',
      download: 'Download',
      publishTo: 'Publish to',
      publishing: 'Publishing',
      published: 'Published successfully!',
      delete: 'Delete'
    },
    
    // Settings
    settings: {
      title: 'Settings',
      telegram: 'Telegram Settings',
      botToken: 'Bot Token',
      chatId: 'Chat ID',
      youtube: 'YouTube Settings',
      clientId: 'Client ID',
      clientSecret: 'Client Secret',
      tiktok: 'TikTok Settings',
      sessionId: 'Session ID',
      heygen: 'HeyGen Settings',
      apiKey: 'API Key',
      avatarId: 'Avatar ID',
      voiceId: 'Voice ID',
      saveSettings: 'Save Settings',
      savingSettings: 'Saving Settings',
      settingsSaved: 'Settings saved successfully!'
    },
    
    // Automation
    automation: {
      title: 'Automation',
      status: 'Status',
      active: 'Active',
      inactive: 'Inactive',
      enable: 'Enable Automation',
      disable: 'Disable Automation',
      schedule: 'Schedule Settings',
      postInterval: 'Post Interval (minutes)',
      startHour: 'Start Hour',
      endHour: 'End Hour',
      minPosts: 'Min Posts/Day',
      maxPosts: 'Max Posts/Day',
      willPost: 'Will post',
      times: 'times',
      perDay: 'per day',
      between: 'between',
      and: 'and',
      pending: 'Pending Posts',
      published: 'Published Today',
      languages: 'Languages',
      logs: 'Activity Logs',
      noLogs: 'No logs yet',
      saveSchedule: 'Save Schedule',
      savingSchedule: 'Saving Schedule',
      scheduleSaved: 'Schedule saved successfully!'
    },
    
    // Common
    common: {
      loading: 'Loading...',
      error: 'Error',
      success: 'Success',
      stop: 'Stop',
      cancelling: 'Cancelling...',
      restart: 'Restart App',
      confirmDelete: 'Are you sure?',
      yes: 'Yes',
      no: 'No'
    }
  },
  
  ru: {
    // Навигация
    nav: {
      dashboard: 'Главная',
      drafts: 'Черновики',
      publish: 'Публикация',
      settings: 'Настройки',
      automation: 'Автоматизация'
    },
    
    // Главная
    dashboard: {
      title: 'Генерация Скриптов',
      theme: 'Тема',
      selectTheme: 'Выберите тему',
      count: 'Количество скриптов',
      generate: 'Генерировать',
      generatingScripts: 'Генерация скриптов',
      scriptsGenerated: 'Скрипты успешно сгенерированы!'
    },
    
    // Черновики
    drafts: {
      title: 'Черновики Скриптов',
      noScripts: 'Нет скриптов. Создайте их!',
      edit: 'Изменить',
      save: 'Сохранить',
      cancel: 'Отмена',
      delete: 'Удалить',
      createVideo: 'Создать Видео',
      videoSettings: 'Настройки Видео',
      textPosition: 'Позиция Текста',
      top: 'Сверху',
      center: 'По центру',
      bottom: 'Снизу',
      customBackground: 'Свой Фон',
      uploadBackground: 'Загрузить Фон',
      start: 'Начать',
      generatingVideo: 'Генерация видео',
      videoGenerated: 'Видео успешно сгенерировано!'
    },
    
    // Публикация
    publish: {
      title: 'Готовые к Публикации',
      noVideos: 'Нет видео. Создайте их из черновиков!',
      videoPreview: 'Предпросмотр Видео',
      audioPreview: 'Предпросмотр Аудио',
      download: 'Скачать',
      publishTo: 'Опубликовать в',
      publishing: 'Публикация',
      published: 'Успешно опубликовано!',
      delete: 'Удалить'
    },
    
    // Настройки
    settings: {
      title: 'Настройки',
      telegram: 'Настройки Telegram',
      botToken: 'Токен Бота',
      chatId: 'ID Чата',
      youtube: 'Настройки YouTube',
      clientId: 'Client ID',
      clientSecret: 'Client Secret',
      tiktok: 'Настройки TikTok',
      sessionId: 'ID Сессии',
      heygen: 'Настройки HeyGen',
      apiKey: 'API Ключ',
      avatarId: 'ID Аватара',
      voiceId: 'ID Голоса',
      saveSettings: 'Сохранить',
      savingSettings: 'Сохранение',
      settingsSaved: 'Настройки сохранены!'
    },
    
    // Автоматизация
    automation: {
      title: 'Автоматизация',
      status: 'Статус',
      active: 'Активна',
      inactive: 'Неактивна',
      enable: 'Включить',
      disable: 'Выключить',
      schedule: 'Настройки Расписания',
      postInterval: 'Интервал (минуты)',
      startHour: 'Начало (час)',
      endHour: 'Конец (час)',
      minPosts: 'Мин постов/день',
      maxPosts: 'Макс постов/день',
      willPost: 'Будет',
      times: 'раз',
      perDay: 'в день',
      between: 'с',
      and: 'до',
      pending: 'В Очереди',
      published: 'Опубликовано Сегодня',
      languages: 'Языки',
      logs: 'Журнал',
      noLogs: 'Нет записей',
      saveSchedule: 'Сохранить',
      savingSchedule: 'Сохранение',
      scheduleSaved: 'Расписание сохранено!'
    },
    
    // Общее
    common: {
      loading: 'Загрузка...',
      error: 'Ошибка',
      success: 'Успешно',
      stop: 'Стоп',
      cancelling: 'Отмена...',
      restart: 'Перезапуск',
      confirmDelete: 'Вы уверены?',
      yes: 'Да',
      no: 'Нет'
    }
  }
};

// Create language store
const createLanguageStore = () => {
  const { subscribe, set } = writable<Language>('en');
  
  // Load from localStorage on init
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('language') as Language;
    if (saved && (saved === 'en' || saved === 'ru')) {
      set(saved);
    }
  }
  
  return {
    subscribe,
    set: (lang: Language) => {
      if (typeof window !== 'undefined') {
        localStorage.setItem('language', lang);
      }
      set(lang);
    }
  };
};

export const language = createLanguageStore();

// Create translation store
export const t = derived(language, ($language) => {
  return (key: string): string => {
    const keys = key.split('.');
    let value: any = translations[$language];
    
    for (const k of keys) {
      if (value && typeof value === 'object') {
        value = value[k];
      } else {
        return key; // Return key if translation not found
      }
    }
    
    return typeof value === 'string' ? value : key;
  };
});

