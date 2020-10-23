import { createApp } from "vue";
import App from "./App.vue";

import {
    Button,
    Col,
    Row,
    Uploader,
    Empty,
    Image,
    Tab,
    Tabs,
    Skeleton,
    Loading
} from "vant";

const app = createApp(App);

app.use(Button);
app.use(Uploader);
app.use(Row);
app.use(Col);
app.use(Empty);
app.use(Image);
app.use(Tab);
app.use(Tabs);
app.use(Skeleton);
app.use(Loading);
app.mount("#app");
