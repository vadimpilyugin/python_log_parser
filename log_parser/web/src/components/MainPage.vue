<template>
    <div v-if="layout.length > 0">
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#" @click.prevent="current_server = 0">
          <img src="static/pie-chart.svg" width="30" height="30" alt="">
          Log Parser
        </a>
        <div>
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <span>{{mapName(layout[current_server].__NAME__)}}</span>
              </a>
              <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                <a class="dropdown-item" href="#" @click.prevent="gotoPage(i)" v-for="(server_el, i) in layout" v-show="(currentServer != MAP_ALL_SERVERS_NAME) || (i != current_server)">{{mapName(server_el.__NAME__)}}</a>
              </div>
            </li>
          </ul>
        </div>
      </nav>
      <!-- <div class="modal fade bd-example-modal-lg" id="exampleModal">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <TemplateEditor></TemplateEditor>
          </div>
        </div>
      </div> -->
      <h5 class="card-title report-descr"> {{currentHeader}} </h5>
      <p class="card-text report-descr">Для сервера заданы {{layout[current_server].__COUNTERS__.length}} счетчика и {{layout[current_server].__DISTRIBUTIONS__.length}} распределений</p>
      <div class="counters" v-for="(server_el, i) in layout">
        <counter 
          :endpoint='counters_ep'
          :server="server_el.__NAME__"
          :errors="errors"
          v-show="i == current_server"
        ></counter>
      </div>
      <div class="distributions" v-for="(server_el, i) in layout">
        <aggregation 
          :errors="errors"
          :endpoint='distribs_ep'
          :server="server_el.__NAME__"
          :danger="false"
          v-show="i == current_server"
        ></aggregation>
      </div>
      <div class="failed-stats" v-show="layout[current_server].__NAME__ == ALL_SERVERS">
        <aggregation
          :errors="errors"
          :endpoint="failed_ep"
          :danger="true"

        ></aggregation>
          <!-- @addTemplate="templateEditor"
          @addService="serviceEditor" -->
      </div>
      <!-- <div v-if="layout[current_server].__NAME__ == '__ALL_SERVERS__'">
        <periodicity></periodicity>
        <blocks></blocks>
      </div> -->
    </div>
</template>

<script>
import { apiRequest } from './request_lib.js';
// import $ from "jquery";
export default {
  props: ['errors'],
  data () {
    return {
      layout_ep: '/layout',
      counters_ep: '/layout/counters',
      distribs_ep: '/layout/distributions',
      failed_ep: '/layout/failed',
      layout: [],
      current_server: 0,
      ALL_SERVERS: '__ALL_SERVERS__',
      MAP_ALL_SERVERS_NAME: 'All servers',
      HEADER_ALL_SERVERS: 'Статистика по всем серверам',
      HEADER_OTHER_SERVERS: 'Статистика по серверу '
    }
  },
  methods: {
    gotoPage (i) {
      this.current_server = i;
    },
    getAggregations () {
      apiRequest(
        {
          method: 'get',
          url: this.layout_ep
        },
        (data) => {
          this.layout = data;
        },
        this.errors
      )
    },
    nav_link_class (i) {
      if (i == this.current_server)
        return 'nav-link active';
      else
        return 'nav-link';
    },
    mapName (server_name) {
      if (server_name == this.ALL_SERVERS)
        return this.MAP_ALL_SERVERS_NAME;
      else
        return server_name;
    },
    // templateEditor (service, msg) {
    //   $('#exampleModal').modal('show')
    // },
    // serviceEditor (service) {

    // }
  },
  computed : {
    currentServer () {
      return this.mapName(this.layout[this.current_server].__NAME__);
    },
    currentHeader () {
      if (this.layout.length > 0) {
        if (this.layout[this.current_server].__NAME__ == this.ALL_SERVERS)
          return this.HEADER_ALL_SERVERS;
        else
          return this.HEADER_OTHER_SERVERS + this.currentServer;
      } else {
        return '';
      }
    }
  },
  created () {
    this.getAggregations();
  }
}
</script>

<style scoped>
.distributions {
  margin-bottom: 1rem;
}
.counters {
  margin-bottom: 1rem;
}
.failed-stats {
  margin-bottom: 1rem;
}
.report-descr {
  margin-left: 1rem;
}
.navbar {
  margin-bottom: 1rem;
}
</style>
