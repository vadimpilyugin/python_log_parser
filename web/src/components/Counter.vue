<template>
  <div class="card">
    <div class="card-header">
      <a data-toggle="collapse" :href="'#'+id">
        {{name}}
      </a>
    </div>
    <div class="card-body collapse show" :id="id">
      <p class="card-text" v-for="el in elements"> 
        <span :class="counter_classes(el)">{{el.__NAME__}}</span> <span class="badge badge-secondary">{{el.__WEIGHT__}}</span>
      </p>
    </div>
  </div>
</template>

<script>
import { apiRequest, makeId } from './request_lib.js';
export default {
  props: ['endpoint', 'server', 'errors'],
  data () {
    return {
      name: 'Counter\'s name',
      id: '',
      elements: []
    }
  },
  methods: {
    counter_classes (el) {
      if (el.__WEIGHT__ == 0)
        return 'list-item-text disabled';
      else
        return 'list-item-text';
    }
  },
  created () {
    console.log("Created Counter with parameters: ",this.endpoint);
    this.id = makeId();
    apiRequest({
      method: 'get',
      url: this.endpoint,
      params: {
        server:this.server
      }
    }, (data) => {
      this.name = data['__NAME__'];
      this.elements = data['__ARRAY__'];
    }, this.errors);
  }
}
</script>

<style scoped>
.badge {
  font-size: 14px;
}
.list-item-text {
  width: 100%;
}
p.card-text {
  display: flex;
  align-items: center;
}
.disabled {
  color: #6c757d;
}
</style>
