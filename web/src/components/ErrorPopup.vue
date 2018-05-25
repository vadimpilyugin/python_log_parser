<template>
  <transition name="fade">
    <div v-if="visible" :class="classes">
      <strong>{{preface}}: </strong>{{message}}
      <button type="button" class="close" @click.prevent="visible = false">
        <span>&times;</span>
      </button>
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
        return 'alert alert-dismissible alert-'+this.level;
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
  /*.alert {
    display: flex;
    justify-content: space-between;
  }*/
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }
  button {
    outline: 0;
  }
</style>