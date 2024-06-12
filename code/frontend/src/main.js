import App from './App.vue'
import { createApp } from 'vue'
import { store } from './store'
import {router} from './router'
import FlashMessage from './custom_modules/FlashMessagePlugin.js';

import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
import enUS from '@kangc/v-md-editor/lib/lang/en-US';

import Prism from 'prismjs';



VueMarkdownEditor.use(vuepressTheme, {
  Prism,
});
VueMarkdownEditor.lang.use('en-US', enUS);
// import VueLogger from 'vuejs-logger';


// const isProduction = process.env.NODE_ENV === 'production';
// const options = {
//     isEnabled: true,
//     logLevel: isProduction ? 'error' : 'debug',
//     stringifyArguments: true,
//     showLogLevel: false,
//     showMethodName: false,
//     separator: '|',
//     showConsoleColors: true,
//   };


const app = createApp(App)

app.use(FlashMessage);
app.use(store)
app.use(router)
app.use(VueMarkdownEditor)
// app.use(VueLogger,options)

app.mount('#app')