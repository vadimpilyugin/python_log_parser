<template>
  <div>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#" @click.prevent="0 === 0">
      <img src="static/pie-chart.svg" width="30" height="30" alt="">
      Log Parser
    </a>
  </nav>
  <div class="central-col">
    <h5 class="card-title report-descr"> Выбор файлов </h5>
    <p class="card-text report-descr"> Выберите файлы для разбора. Текущая папка ../../log_parser/logs/ </p>
    <div>
      <button class="btn btn-primary" @click="parseFiles" v-if="!clicked"> Parse! </button>
      <button class="btn btn-success" @click="showReport" v-else> Show results! </button>
    </div>
    <div class="card">
      <div class="card-header">
        <div class="header-link">
          <a class="card_link_style" data-toggle="collapse" href="#fileSelect">
            Выбор файлов
          </a>
        </div>
      </div>
      <div class="card-body collapse show" id="fileSelect">
    <ul class="list-unstyled">
      <li v-for="(item,i) in files">
        <div class="list-dir">
          <div>
            <input type="checkbox" :disabled="clicked" style="margin-right: 1rem;" v-model="item.checked" @click="onServerCheck(i)">
            <a :href="'#'+item.server" data-toggle="collapse">{{item.server}}</a>
          </div>
          <span class="counter" v-show="item.checked && clicked">
            <span class="green-counter">OK: {{item.ok}}</span> / <span class="red-counter">FAIL: {{item.fail}}</span>
          </span>
        </div>
        <div :id="item.server" class="collapse show">
          <ul class="list-unstyled" style="padding-left: 40px;">
            <li v-for="(file,j) in item.files">
              <div class="list-dir-item">
                <div>
                  <input type="checkbox" :disabled="clicked" style="margin-right: 1rem;" v-model="file.checked" @click="onFileCheck(i,j)">{{file.filename}}
                </div>
                <span class="counter" v-if="file.visible">
                  <span class="green-counter">{{file.ok}}</span> / 
                  <span class="red-counter">{{file.fail}}</span>
                </span>
              </div>
            </li>
          </ul>
        </div>
      </li>
    </ul>
      </div>
    </div>  

  </div>
  </div>
</template>

<script>
import { apiRequest } from './request_lib.js';
export default {
  props: ['errors'],
  data () {
    return {
      files : [],
      servers_ep : '/logs/servers',
      files_ep : '/logs/filenames',
      parse_ep : '/parse/single',
      config_ep: '/config',
      log_folder: '',
      clicked : false,
    }
  },
  methods : {
    onFileCheck (server_no, i) {
      let flag = this.files[server_no].files[i].checked;
      if (flag) {
        this.files[server_no].files[i].checked = false;
        this.files[server_no].checked_no -= 1;
        if (this.files[server_no].checked_no === 0) {
          this.files[server_no].checked = false;
        }
      } else {
        this.files[server_no].files[i].checked = true;
        if (this.files[server_no].checked_no === 0) {
          this.files[server_no].checked = true;
        }
        this.files[server_no].checked_no += 1;
      }
    },
    onServerCheck (server_no) {
      let flag = this.files[server_no].checked;
      if (flag) {
        this.files[server_no].checked = false;
        this.files[server_no].checked_no = 0;
        for (let i = 0; i < this.files[server_no].files.length; i++) {
          this.files[server_no].files[i].checked = false;
        }
      } else {
        this.files[server_no].checked = true;
        this.files[server_no].checked_no = this.files[server_no].files.length;
        for (let i = 0; i < this.files[server_no].files.length; i++) {
          this.files[server_no].files[i].checked = true;
        }
      }
    },
    getDirectory () {
      apiRequest({
        method: 'get',
        url: this.config_ep
      }, (config) => {
        this.log_folder = config.log_folder;
      }, this.errors);
    },
    getFiles () {
      apiRequest({
        method: 'get',
        url: this.servers_ep
      }, (servers) => {
        for (let i = 0; i < servers.length; i++) {
          servers[i] = {
            server : servers[i],
            checked : true,
            files : [],
            checked_no : 0,
            visible:false,
            ok:0,
            fail:0
          };
          apiRequest({
            method: 'get',
            url: this.files_ep,
            params : {
              server : servers[i].server
            }
          }, (files) => {
            for (let j = 0; j < files.length; j++) {
              files[j] = {filename:files[j], checked:true, ok:0, fail:0,visible:false};
            }
            servers[i].files = files;
            servers[i].checked_no = files.length;
          }, this.errors);
        }
        this.files = servers;
      }, this.errors);
    },
    parseFiles () {
      for (let i = 0; i < this.files.length; i++) {
        if (this.files[i].checked) {
          this.files[i].visible = true;
          for (let j = 0; j < this.files[i].files.length; j++) {
            if (this.files[i].files[j].checked) {
              apiRequest({
                method: 'post',
                url: this.parse_ep,
                params : {
                  server : this.files[i].server,
                  filename : this.files[i].files[j].filename
                }
              }, (result) => {
                this.files[i].files[j].visible = true;
                this.files[i].files[j].ok = result.ok;
                this.files[i].files[j].fail = result.fail;
                this.files[i].ok += result.ok;
                this.files[i].fail += result.fail;
              }, this.errors);
            }
          }
        }
      }
      this.clicked = true;
    },
    showReport () {
      this.$emit('success');
    }
  },
  created () {
    this.getFiles();
    this.getDirectory();
  }
}
</script>

<style scoped>
.central-col {
  display: flex;
  flex-direction: column;
  max-width: 800px;
  padding: 1rem 1rem;
}
ul {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 500px;
}
li {
  display: flex;
  flex-direction: column;
}
.list-dir {
  display: flex;
  justify-content: space-between;
}
.list-dir-item {
  display: flex;
  justify-content: space-between;
}
.counter {
  margin-left: 1rem;
}
.green-counter {
  color: green;
}
.red-counter {
  color: red;
}
.control-btn {
  display: flex;
  justify-content: space-around;
  max-width: 300px;
  width: 100%;
}
button {
  margin-bottom: 1rem;
}
</style>
