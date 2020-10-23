<template>
    <div class="tab-container">
        <van-tabs type="card" color="green" animated class="tabs">
            <van-tab title="Original">
                <van-image :src="image.content" class="img"></van-image>
            </van-tab>
            <van-tab title="Background Removed">
                <van-image :src="image_url" class="img"></van-image>
            </van-tab>
        </van-tabs>

        <van-button type="primary" class="downloadBtn">
            İndir
        </van-button>
    </div>
</template>

<script lang="ts">
// eslint-disable-next-line no-unused-vars
import { defineComponent, PropType } from "vue";

import axios from "axios";

export default defineComponent({
    props: {
        image: {
            type: Object as PropType<VanFile>,
            required: true
        }
    },

    async setup(props) {
        const formData = new FormData();
        formData.append("image_file", props.image.file);

        const result = await axios.post<Blob>(
            "http://localhost:8000/api/removebg",
            formData,
            {
                responseType: "blob",
                headers: {
                    "Content-Type": "multipart/form-data",
                    accept: "image/*"
                }
            }
        );

        const image_url = URL.createObjectURL(result.data);

        return {
            image_url
        };
    }
});
</script>

<style scoped>
.tab-container {
    display: flex;
    flex-wrap: wrap;
    width: 100%;
    padding: 2rem;
    margin: 2rem;
    justify-content: center;
    align-items: center;
    box-shadow: 1px 2px 8px 8px whitesmoke;
    background-color: azure;
}

.tabs {
    width: 100%;
}

.downloadBtn {
    border-radius: 5px;
    padding: 5px;
    margin: 1rem;
    width: 10rem;
}

.img {
    width: 100%;
    height: 20%;
    padding: 32px 0;
}

@media only screen and (min-width: 768px) {
    .tab-container {
        width: 50%;
    }

    
}
</style>
