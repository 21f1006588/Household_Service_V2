<template>
  <div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* Global styles */
html, body {
  margin: 0;
  padding: 0;
  /* If you want no scrolling at all, keep overflow: hidden */
  /* But if you might have more content, remove the overflow: hidden; */
  /* overflow: hidden; */
}

#app {
  text-align: center;
}
</style>
