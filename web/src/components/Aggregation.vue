<template>
  <div class="my-container">
    
    <div :class="is_danger_card">
      <div :class="is_danger_card_header">
        <h5 class="mb-0">
          <a :class="is_danger_a" data-toggle="collapse" :href="'#'+id">
            {{name}}
            <span class="badge badge-secondary">{{elements.length}}</span>
          </a>
        </h5>
      </div>
      <div :id="id" class="collapse">
        <div class="card-body">
          <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
              <li class="breadcrumb-item" v-for="(key,i) in page_names.slice(0,-1)">
                <a 
                  :data-index="i"
                  href="#" 
                  @click.prevent="return_to_page"
                >
                  {{key}}
                </a>
              </li>
              <li class="breadcrumb-item active">{{page_names[page_names.length-1]}}</li>
            </ol>
          </nav>
          <ul class="list-group">
            <li 
              v-for="(item, i) in current_list" 
              class="list-group-item d-flex justify-content-between align-items-center"
              @click.prevent="goto_page"
              :data-index="i"
              :class="is_clickable"
            >
              {{item[0]}}
              <span class="badge badge-secondary">{{item[1].length ? item[1].length : item[1]}}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- <div class="card mb-3">
      <div class="card-header text-white bg-danger">
        <h5 class="mb-0">
          <a class="danger" data-toggle="collapse" href="#collapse1">
            Не разобранные строки
            <span class="badge badge-secondary" style="float:right">16</span>
          </a>
        </h5>
      </div>
      <div id="collapse1" class="collapse">
        <div class="card-body">
          <p> Foobar! </p>
        </div>
      </div>
    </div> -->
    <div class="card border-light" v-if="insides.len > 0">
      {{insides}}
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    props: ['endpoint', 'statId', 'danger'],
    data () {
      return {
        name: 'Stat\'s name',
        weight: 0,
        keys: [],
        index_seq: [],
        elements:[
          ['apache', 
            [
              ['192.168.1.1', 2]
            ]
          ], 
          ['sshd', 
            [
              ['8.8.8.8', 1], 
              ['1.1.1.1', 2]
            ]
          ], 
          ['systemd', 
            [
              ['logind', 1], 
              ['systemd-logind', 2], 
              ['systemd', 3]
            ]
          ]
        ],
        id: '0',
        insides: ''
      }
    },
    computed: {
      current_list () {
        let ar = this.elements;
        for (let i = 0; i < this.index_seq.length; i++) {
          ar = ar[this.index_seq[i]][1];
        }
        return ar;
      },
      page_names () {
        let page_names = ['#'];
        let ar = this.elements;
        for (let i = 0; i < this.index_seq.length; i++) {
          page_names.push(ar[this.index_seq[i]][0]);
          ar = ar[this.index_seq[i]][1];
        }
        return page_names;
      },
      is_max_depth () {
        if (this.index_seq.length < this.keys.length-1) {
          return false;
        } else {
          return true;
        }
      },
      is_clickable () {
        return this.is_max_depth ? '' : 'is-clickable';
      },
      is_danger_card () {
        return this.danger === true ? 'card mb-3' : 'card border-light';
      },
      is_danger_card_header () {
        return this.danger === true ? 'card-header text-white bg-danger' : 'card-header';
      },
      is_danger_a () {
        return this.danger === true ? 'danger' : '';
      }
    },
    methods: {
      return_to_page(ev) {
        let index = ev.target.dataset.index;
        console.log("Switch page to",index);
        while (this.index_seq.length > index) {
          this.index_seq.pop();
        }
      },
      goto_page(ev) {
        if (this.index_seq.length < this.keys.length-1) {
          this.index_seq.push(ev.target.dataset.index);
        }
      }
    },
    created () {
      console.log("Created Aggregation with parameters: ",this.endpoint);
      // Axios get request
      axios(
        {
          method: 'get',
          url: this.endpoint,
          params: {
            id:this.statId
          }
        }
      ).then(response => {
        // this.insides = response.data;
        this.name = response.data['__PAYLOAD__']['__NAME__']
        this.weight = response.data['__PAYLOAD__']['__WEIGHT__']
        this.keys = response.data['__PAYLOAD__']['__KEYS__']
        this.elements = response.data['__PAYLOAD__']['__ARRAY__']
      }).catch(error => {
        if (error.response) {
          // not 2xx
          console.log("Not 2xx");
        } else if (error.request) {
          console.log("No answer");
        } else {
          console.log(error.message);
        }
      });
      this.id = makeid();
    }
  }

  function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 5; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
  }

</script>

<style scoped>

  .my-container {
    max-width: 600px;
    margin: 0 auto;
  }
  li.is-clickable:hover {
    background-color: #ececec;
    cursor: pointer;
  }
  .alert-secondary {
    margin-bottom: 0px;
    background-color: #e9ecef;
    border: none;
    border-radius: 0px;

    border-top-right-radius: .25rem;
    border-top-left-radius: .25rem;

    padding-left: 16px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
    text-align: center;
  }
  .breadcrumb {
    margin-bottom: 0px;
    border: none;
    border-radius: 0px;
    padding: 5px 20px;
    background-color: #f7f7f7;
  }
  li:first-child {
    border-radius: 0px;
  }
  ul li {
    padding: 5px 20px;
  }
  div.card-body {
    padding: 0;
  }
  a {
    outline: 0;
  }
  .badge {
    float:right;
  }
  a.danger {
    color: white;
  }
</style>