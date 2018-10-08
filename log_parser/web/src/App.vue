<template>
  <div class="full-frame">
    <div class="main-content">
      <!-- <Periodicity
        :errors="errors"

      ></Periodicity> -->
      <FileSelect 
        @success="report = true" 
        v-if="!report"
        :errors="errors"
      >
      </FileSelect>
      <MainPage
        v-if="report"
        :errors="errors"
      >

      </MainPage>
    </div>
    <div class="error-content">
      <error-popup
        v-for="(error,i) in errors"
        :key="i"
        :level="error.level"
        :preface="error.preface"
        :message="error.message"

      ></error-popup>
      
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      report : false,
      errors: []
    }
  }
}
</script>

<style>
.full-frame {
  display: flex;
  justify-content: center;
}
.main-content {
  width: 100%;
  padding: 1rem;
  padding-top: 0;
  max-width: 800px;
}
.error-content {
  padding: 1rem;
  position: absolute;
  right: 0;
  top: 0;
  width: 500px;
}
a {
  outline: 0;
}
</style>
