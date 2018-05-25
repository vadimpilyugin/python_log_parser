<template>
  <div class="full-frame">
    <div class="main-content">
      <error-popup
        v-for="(error,i) in errors"
        :key="i"
        :level="error.level"
        :preface="error.preface"
        :message="error.message"

      ></error-popup>
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
  max-width: 800px;
  width: 100%;
  margin-bottom: 1rem;
}
a {
  outline: 0;
}
</style>
