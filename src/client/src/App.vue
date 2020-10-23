<template>
    <van-row justify="center" tag="h1" class="title"
        >Resimden arka planı kaldırın</van-row
    >

    <van-row justify="center">
        <van-empty v-if="!image"> </van-empty>
        <Suspense v-else>
            <template #default>
                <image-converter :image="image" />
            </template>

            <template #fallback>
                <van-loading type="spinner">
                    Loading...
                </van-loading>
            </template>
        </Suspense>
    </van-row>

    <van-row justify="center">
        <van-uploader description="Upload Image" :after-read="uploadImage">
            <van-button type="success" class="upload-btn">
                <i class="fas fa-upload"></i>
                Resmi Yükle
            </van-button>
        </van-uploader>
    </van-row>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

import ImageConverter from "./components/ImageConverter.vue";

// import axios from "axios";

export default defineComponent({
    name: "App",
    components: {
        ImageConverter
    },
    setup() {
        const image = ref<VanFile | null>(null);

        const uploadImage = (file: VanFile) => {
            image.value = null;
            setTimeout(() => (image.value = file), 200);
        };

        // const removebg = async () => {

        // }

        return {
            uploadImage,
            image
        };
    }
});
</script>

<style scoped>
.title {
    text-align: center;
}

.container {
    height: 10rem;
}
.upload-btn {
    margin: 10px;
    font-size: 17px;
    font-weight: bold;
}
</style>

<style>
* {
    box-sizing: border-box;
}
</style>
