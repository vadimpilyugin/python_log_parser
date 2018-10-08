<template>
  <div class="card">
    <h5 class="card-header">Featured</h5>
    <div class="card-body">
      <h5 class="card-title">Special title treatment</h5>
        <div class="form-group">
          <label for="exampleFormControlSelect1">Select server</label>
          <select class="form-control" id="exampleFormControlSelect1" v-model="current_server">
            <option v-for="server in servers">{{server}}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="exampleFormControlSelect2">Select file</label>
          <select class="form-control" id="exampleFormControlSelect2" v-model="current_filename">
            <option v-for="filename in filenames">{{filename}}</option>
          </select>
        </div>
      <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
      <ul class="list-unstyled">
        <li v-for="item in fields">
          <input type="checkbox" style="margin-right: 1rem;" v-model="item.checked">
          <span> {{item.field}} </span>
        </li>
      </ul>
      <!-- <aggregation 
          v-if="current_server !== '' && current_filename !== ''"
          :errors="errors"
          :params="{method: 'get', url: ep, params:{server:current_server, filename: current_filename}}"
          :danger="false"
          
        ></aggregation> -->
      <a href="#" class="btn btn-primary" @click.prevent="analyzePeriods()"> Reload </a>
      <pre>{{data}}</pre>
    </div>
  </div>
</template>

<script>
import { apiRequest } from './request_lib.js';
export default {
  props: ['errors'],
  data () {
    return {
      data: '',
      ep: '/analyze',
      servers_ep: '/logs/servers',
      filenames_ep: '/logs/filenames',
      periodicity_ep: '/periodicity',
      servers: [],
      current_server: '',
      current_filename: '',
      filenames: [],
      fields: []
    }
  },
  watch: {
    current_server (new_serv, old_serv) {
      apiRequest({
        url: this.filenames_ep,
        params: {
          server: new_serv
        }
      }, (data) => {
        this.filenames = data;
        this.current_filename = data[0];
      }, this.errors);
    },
    current_filename (new_fn, old_fn) {
      apiRequest({
        url: this.ep,
        params: {
          server: this.current_server,
          filename: new_fn
        }
      }, (data) => {
        this.fields = data.fields;
      }, this.errors);
    }
  },
  computed: {
    selectedFields () {
      let ar = [];
      for (let i = 0; i < this.fields.length; i++) {
        if (this.fields[i].checked)
          ar.push(this.fields[i].field)
      }
      return ar
    }
  },
  methods: {
    loadServers () {
      apiRequest({
        url: this.servers_ep,
      }, (data) => {
        this.servers = data;
        this.current_server = data[0];
      }, this.errors);
    },
    analyzePeriods () {
      apiRequest({
        url: this.periodicity_ep,
        params: {
          server: this.current_server,
          filename: this.current_filename,
          flds: this.selectedFields.join(','),
          k: 3
        }
      }, (data) => {
        this.data = data;
      }, this.errors);
    }
  },
  created () {
    // this.reload();
    this.loadServers();
  }
}
</script>

<style scoped>
</style>
