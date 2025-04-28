<template>
  <div class="min-h-screen bg-gray-50">
    <router-view />
    <ChatWidget />
  </div>
</template>

<script>
import ChatWidget from './components/ChatWidget.vue';

export default {
  name: 'App',
  components: {
    ChatWidget
  }
}
</script>

<style>
/* Reset box sizing for consistency */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Ensure the app takes full height */
html, body, #app {
  height: 100%;
  width: 100%;
}
</style>
