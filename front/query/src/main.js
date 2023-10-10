import ViewUI from "view-ui-plus/dist/viewuiplus.min.esm";
import {createApp} from 'vue'
import App from './App.vue'
import 'view-ui-plus/dist/styles/viewuiplus.css'

const app = createApp(App)
app.use(ViewUI)
app.mount('#app')
