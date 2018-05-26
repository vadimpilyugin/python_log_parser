<template>
  <transition name="fade">
    <div v-if="need_to_save" :class="classes">
        <p><strong>{{preface_pr}}</strong>{{message}}</p>
        <button type="button" v-if="show_button" class="btn btn-success" @click="commit">{{button_text}}</button>
    </div>
  </transition>
</template>

<script>
  import axios from 'axios'
  export default {
    props: ['ep', 'hasButton', 'level'],
    data () {
      return {
        message: 'Нужно сохранить изменения перед выходом',
        preface: 'Message',
        need_to_save: false
      }
    },
    computed: {
      classes () {
        return 'alert alert-'+this.level;
      },
      show_button () {
        return this.hasButton && (this.level != 'success');
      },
      button_text () {
        return this.level === 'danger' ? 'Resend' : 'Save';
      },
      preface_pr () {
        return this.preface + ': ';
      }
    },
    methods: {
      commit () {
        axios(
          {
            method: 'post',
            url: this.ep
          }
        ).then(response => {
          if (response.data['__OK__']) {
            this.level = 'success';
            this.preface = 'Success!'
            this.message = 'Files have been updated'
            this.$emit('success');
          } else {
            this.level = 'danger'
            this.preface = `Error (${response.data['__DESCR__']})`
            this.message = response.data['__REASON__'];
          }
        }).catch(error => {
          this.level = 'danger';
          this.preface = 'Network error!';
          if (error.response) {
            this.message = "Not 2xx";
          } else if (error.request) {
            this.message = "No response";
          } else {
            this.message = error.message;
          }
        });
      }
    },
    created () {
      window.setInterval(
        () => {
          axios(
            {
              method: 'get',
              url: this.ep
            }
          ).then(response => {
            console.log(response.data);
            this.need_to_save = response.data['__PAYLOAD__'];
          })
        },
        3000
      );
    }
  }
</script>

<style scoped>
  .alert {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }
</style>