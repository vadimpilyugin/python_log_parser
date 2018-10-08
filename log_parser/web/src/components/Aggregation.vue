<template>
    <div :class="card_style" v-if="weight > 0">
      <div :class="card_style_header">
        <div class="header-link">
          <a :class="card_link_style" data-toggle="collapse" :href="anchor_id">
            {{name}}
          </a>
        </div>
      </div>
      <div :id="id" class="collapse show">
        <nav aria-label="breadcrumb" v-show="page_names.length > 1">
          <ol class="breadcrumb">
            <li class="breadcrumb-item" v-for="(key,i) in page_names.slice(0,-1)">
              <a href="#" @click.prevent.stop="return_to_page(i)">
                {{key}}
              </a>
            </li>
            <li class="breadcrumb-item active">{{page_names[page_names.length-1]}}</li>
          </ol>
        </nav>
        <ul class="list-group">
          <li 
            v-for="(item, i) in current_list" 
            @click.stop="goto_page(i)"
            :data-index="i"
            :class="list_item_class(i)"
          >
            <span class="list-item-text">{{item['__NAME__']}}</span>
            <!-- <a href="#" v-if="is_link(i)" @click.prevent="triggerEditor(i)"> Добавить </a> -->
            <span class="badge badge-secondary">{{item[sort_field]}}</span>
          </li>
        </ul>
      </div>
    </div>
</template>

<script>
  import { apiRequest, makeId } from './request_lib.js';
  export default {
    props: ['params', 'danger', 'errors'], // 'endpoint', 'server', 'no',
    data () {
      return {
        name: 'Stat\'s name',
        weight: 0,
        keys: [],
        index_seq: [],
        elements:[],
        id: '',
        visible: false,
        no_format: "Не нашлось формата",
        no_service: "Какие сервисы не определены",
        no_template: "Для каких строк не нашлось шаблона",
        sort_field: ''
      }
    },
    computed: {
      current_list () {
        let ar = this.elements;
        for (let i = 0; i < this.index_seq.length; i++) {
          ar = ar[this.index_seq[i]]['__ARRAY__'];
        }
        return ar;
      },
      page_names () {
        let page_names = ['#'];
        let ar = this.elements;
        for (let i = 0; i < this.index_seq.length; i++) {
          page_names.push(ar[this.index_seq[i]]['__NAME__']);
          ar = ar[this.index_seq[i]]['__ARRAY__'];
        }
        return page_names;
      },
      card_style () {
        return this.danger === true ? 'card' : 'card border-light';
      },
      card_style_header () {
        return this.danger === true ? 'card-header text-white bg-danger' : 'card-header';
      },
      card_link_style () {
        return this.danger === true ? 'danger' : '';
      },
      anchor_id () {
        return '#'+this.id;
      }
    },
    methods: {
      list_item_class (i) {
        if (this.current_list[i].__WEIGHT__ == 0)
          return 'list-group-item disabled';
        else if (this.is_clickable(i))
          return 'list-group-item is-clickable';
        else 
          return 'list-group-item';
      },
      is_clickable (i) {
        return this.current_list[i].__ARRAY__.length > 0;
      },
      return_to_page(index) {
        while (this.index_seq.length > index) {
          this.index_seq.pop();
        }
      },
      goto_page(i) {
        if (this.is_clickable(i)) {
          this.index_seq.push(i);
        }
      },
      getDistrib () {
        apiRequest(this.params, (data) => {
          this.name = data['__NAME__'];
          if (data['__SORT_FIELD__'] === 'total')
            this.sort_field = '__WEIGHT__';
          else
            this.sort_field = '__DISTINCT__';
          this.weight = data['__WEIGHT__'];
          this.elements = data['__ARRAY__'];
          this.visible = this.weight > 0;
        }, this.errors);
      }
      // is_link (i) {
      //   if (this.danger && !this.is_clickable(i) && this.page_names[1] != this.no_format)
      //     return true;
      //   else
      //     return false;
      // },
      // triggerEditor (i) {
      //   if (this.page_names[1] === this.no_service)
      //     this.$emit('addService', this.current_list[i].__NAME__)
      //   else if (this.page_names[1] === this.no_template)
      //     this.$emit('addTemplate', this.page_names[2], this.current_list[i].__NAME__)
      // }
    },
    watch : {
      params (new_params, old_params) {
        console.log("Updated Aggregation with parameters: ", new_params);
        this.getDistrib();
      }
    },
    created () {
      console.log("Created Aggregation with parameters: ",this.params);
      this.getDistrib();
      this.id = makeId();
    }
  }

</script>

<style scoped>
li.is-clickable:hover {
  background-color: #ececec;
  cursor: pointer;
}
.breadcrumb {
  margin-bottom: 0;
  border: none;
  border-radius: 0;
  padding: 5px 20px;
  background-color: #f7f7f7;
}
li:first-child {
  border-radius: 0;
  border-top: 0;
}
div.card-body {
  padding: 0;
}
a {
  outline: 0;
}
a.danger {
  color: white;
}
.list-group-item {
  display: flex;
  align-items: flex-start;
}
.list-item-text {
  width: 100%;
}
.badge {
  font-size: 14px;
}
</style>