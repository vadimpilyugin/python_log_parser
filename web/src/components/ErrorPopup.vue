<template>
  <transition name="fade">
    <div v-if="visible" :class="classes">
        <p><strong>{{preface}}: </strong>{{message}}</p>
    </div>
  </transition>
</template>

<script>
  export default {
    props: ['level', 'preface', 'message'],
    data () {
      return {
        visible: true
      }
    },
    computed: {
      classes () {
        return 'alert alert-'+this.level;
      }
    },
    created () {
      window.setTimeout(
        () => {
          this.visible = false;
        },
        7000
      );
    }
  }
</script>

<style scoped>
  .alert {
    display: flex;
    justify-content: space-between;
  }
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }
</style>