<template>
  <div>
    <div class="modal-header">
      <h3 class="modal-title">Редактор шаблонов</h3>
      <button type="button" class="close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="modal-body">
      <form method="post" action="#" role="form" >
          <!-- <div class="messages"></div> -->
          <div class="controls">
            <div id="messages">
              <div :class="message_classes">
                <strong>{{message_head}}</strong> {{message_text}}
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <!-- выдвижной список выбора сервиса -->
                <div class="form-group">
                  <label for="service_group"> Выбор сервиса </label>
                  <select class="form-control" name="service_group" id="service_group" v-model="current_service_group">
                    <option v-for="service_group in service_groups" :value="service_group">{{service_group}}</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <!-- выдвижной список выбор категории -->
                <div class="form-group">
                  <label for="category"> Выбор категории </label>
                  <select class="form-control" name="category" id="category" v-model="current_category">
                    <option :value="ADD_NEW_CATEGORY">{{ADD_NEW_CATEGORY}}</option>
                    <!-- <option :value="IGNORE_CATEGORY">{{IGNORE_CATEGORY}}</option> -->
                    <option v-for="category in categories" :value="category">{{category}}</option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <!-- форма ввода новой категории -->
                <div class="form-group" v-if="current_category === ADD_NEW_CATEGORY">
                  <label for="new_category"> Название категории </label>
                  <input type="text" id="new_category" class="form-control" placeholder="Введите название категории" v-model="new_category">
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12">
                <div v-bind:class="{ 'form-group':true, 'has-error': is_regex_wrong, 'has-feedback': is_regex_wrong }">
                  <label for="regexp"> Регулярное выражение </label>
                  <span :class="label_classes"> {{label_text}} </span>
                  <textarea class="form-control" rows="4" id="regexp" name="regexp" placeholder="Введите регулярное выражение" v-model="regexp" ></textarea>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-1">
                  <label for="colorselector" id="type"> Тип:</label>
              </div>
              <div class="col-md-4">
                  <select id="colorselector" v-model="colorselector">
                    <option data-color="#5cb85c" value="Debug" selected="selected">Debug</option>
                    <option data-color="#5bc0de" value="Info">Info</option>
                    <option data-color="#f0ad4e" value="Warning">Warning</option>
                    <option data-color="#d9534f" value="Error">Error</option>
                  </select>
              </div>
            </div>
            <div class="row" id="button">
              <div class="col-md-12">
                  <button class="btn btn-success btn-send" @click.prevent="postTemplate">{{button_text}}</button>
              </div>
            </div>
          </div>
        </form>
    </div>
  </div>
</template>

<script>
function getUrl (webhook, params) {
s = webhook;
s += '?';
for (param in params) {
  if (param.length === 0) {
    return false;
  }
  s += `${param}=${encodeURIComponent(params[param])}&`;
}
if (s.length != 0)
  s = s.substr(0,s.length - 1);
return s;
}
// проверка на содержание в массиве элемента
// var myArray = [0,1,2],
//     needle = 1,
//     index = contains.call(myArray, needle); // true
var contains = function(needle) {
    // Per spec, the way to identify NaN is that it is not equal to itself
    var findNaN = needle !== needle;
    var indexOf;

    if(!findNaN && typeof Array.prototype.indexOf === 'function') {
        indexOf = Array.prototype.indexOf;
    } else {
        indexOf = function(needle) {
            var i = -1, index = -1;

            for(i = 0; i < this.length; i++) {
                var item = this[i];

                if((findNaN && item !== item) || item === needle) {
                    index = i;
                    break;
                }
            }

            return index;
        };
    }

    return indexOf.call(this, needle) > -1;
};
export default {
  data () {
    return {
      regexp: '',
      service_groups: [],
      current_service_group: '',
      categories: [],
      current_category: '',
      loglines: [],
      new_category: '',
      is_regex_wrong: false,
      button_text: 'Добавить шаблон', // текст на кнопке
      message_text: '', // текст сообщения 
      message_head: '', // заголовок
      message_classes: {
        'alert': true,
        'alert-success':true,
        'alert-danger':false,
        'alert-dismissable':true,
        'hidden':true
      },
      // выбор цвета
      colorselector: '',
      // количество строк
      logline_count: 0,
      // константы
      DEFAULT_REGEX: '.*',
      ADD_NEW_CATEGORY: "Add new",
      IGNORE_CATEGORY: "Ignore",
    }
  },
  computed: {
    label_classes () {
      return {
        'label':true,
        'label-success':this.colorselector === 'Debug',
        'label-info':this.colorselector === 'Info',
        'label-warning':this.colorselector === 'Warning',
        'label-danger':this.colorselector === 'Error',
      }
    },
    label_text () {
      if (this.colorselector === 'Debug')
        return 'Debug info';
      else if (this.colorselector === 'Info')
        return 'Useful info';
      else if (this.colorselector === 'Warning')
        return 'Warning';
      else
        return 'Error';
    },
  },
  watch: {
    // whenever regexp changes, this function will run
    regexp: function (new_regexp) {
      console.log(`watch: regexp(new_regexp = ${new_regexp})`);
      // не нужно, иначе проблемы со вводом
      // this.escapeAndChange ();
      this.regexp = new_regexp;
      this.loadLines ();
    },
    current_service_group: function (new_service_group) {
      console.log(`watch: regexp(new_service_group = ${new_service_group})`);
      this.current_service_group = new_service_group;
      this.regexp = '';
      this.loadCategories ();
      this.loadLines ();
    },
  },
  methods: {
    loadLines () {
      _.debounce(() => {
          var vm = this
          var regexp = vm.regexp.length === 0 ? this.DEFAULT_REGEX : vm.regexp;
          axios.get('http://localhost:4567/loglines/no_template_found?regexp='+
            encodeURIComponent(regexp)+'&service_group='+vm.current_service_group)
          .then(function (response) {
            if (response.data["ok"] === true) {
              console.log("loadLines[data].ok", response.data);
              vm.loglines = response.data["data"]["lines"];
              vm.is_regex_wrong = false;
              vm.logline_count = response.data["data"]["rec_size"];
            }
            else {
              console.log("loadLines[data].error");
              vm.is_regex_wrong = true;
            }
          })
          .catch(function (error) {
            console.log(`loadLines: could not reach the API. ${error}`);
          })
        }, 500);
    },
    escapeAndChange (logline) {
      var vm = this;
      var logline = encodeURIComponent (logline);
      axios.get(`http://localhost:4567/string/escape?string=${logline}`)
        .then((response) => {
          if (response.data["ok"] === true) {
            console.log("escapeAndChange[data].ok", response.data);
            vm.regexp = response.data["data"];
          }
          else {
            console.log("escapeAndChange[data].error");
          }
          // vm.check_regexp = response.data;
        })
        .catch((error) => {
          console.log(`escapeAndChange: could not reach the API. ${error}`);
        })
    },
    // загружает сервисы, у которых есть не подошедшие к шаблонам строки
    loadServiceGroups () {
      var vm = this
      axios.get(`http://localhost:4567/services/no_template_found`)
        .then(function (response) {
          if (response.data["ok"] === true) {
            console.log("loadServiceGroups[data].ok", response.data);
            vm.service_groups = response.data["data"];
          }
          else {
            console.log("loadServiceGroups[data].error");
          }
          // vm.check_regexp = response.data;
        })
        .catch(function (error) {
          console.log(`loadServiceGroups: could not reach the API. ${error}`);
        })
    },
    loadCategories () {
      var vm = this;
      var service_group = encodeURIComponent (this.current_service_group)
      axios.get(`http://localhost:4567/service/categories?service_group=${service_group}`)
        .then(function (response) {
          if (response.data["ok"] === true) {
            console.log("loadCategories[data].ok", response.data);
            vm.categories = response.data["data"];
            if (vm.categories.length === 0) {
              vm.categories.push(vm.IGNORE_CATEGORY);
              // vm.current_category = vm.ADD_NEW_CATEGORY;
            }
            // else {
              // vm.current_category = vm.IGNORE_CATEGORY;
            // }
          }
          else {
            console.log("loadCategories[data].error");
          }
          // vm.check_regexp = response.data;
        })
        .catch(function (error) {
          console.log(`loadCategories: could not reach the API. ${error}`);
        })
    },
    getCategory () {
      if (this.current_category === this.ADD_NEW_CATEGORY) {
        return this.new_category;
      }
      else {
        return this.current_category;
      }
    },
    displayMessage (params) {
      if (params.ok) {
        // message success
        this.message_text = params.data;
        this.message_head = 'Success!';
        this.message_classes['alert-danger'] = false;
        this.message_classes['alert-success'] = true;
      }
      else {
        // message failure
        this.message_text = `${params.what}: ${params.descr}`;
        this.message_head = 'Error!';
        this.message_classes['alert-danger'] = true;
        this.message_classes['alert-success'] = false;
      }
      this.message_classes.hidden = false;
      vm = this;
      // setInterval(function () { vm.message_classes.hidden = true}, 5000);
    },
    postTemplate () {
      // debug
      console.log(this.colorselector);
      // ссылка на приложение
      var vm = this;
      // путь доступа к api
      var url;
      // hook
      var webhook = '/add/template';
      // проверяем параметры и конструируем url
      console.log(this.current_service_group, this.getCategory (),this.regexp)
      if (this.getCategory () === 0) {
        return false;
      }
      url = getUrl(webhook, {
        'service_group': this.current_service_group,
        'service_category': this.getCategory (),
        'logline_type': this.colorselector,
        'regexp': this.regexp
      });
      // если параметры отсутствуют
      if (url === false) {
        console.log("Один из параметров пуст");
        return true;
      }
      // делаем запрос
      axios.post(url)
        .then(function (response) {
          if (response.data["ok"] === true) {
            // получили сервис в response.data.data
            console.log("postTemplate[data].ok", response.data.data);
            vm.displayMessage({ok:true, data:response.data.data});
            vm.loadCategories ();
            vm.loadServiceGroups ();
            vm.regexp = '';
            vm.new_category = '';
          }
          else {
            // некорректный запрос к API
            console.log(`postTemplate.err(${response.data.what}): ${response.data.descr}`);
            vm.displayMessage({ok:false, what: response.data.what, descr:response.data.descr});
          }
        })
        .catch(function (error) {
          console.log(`postTemplate: could not reach the API. ${error}`);
          vm.displayMessage({ok:false, what: "exception", descr:error});
        });
    },
    callFoo () {
      console.log("Pressed on list");
    }
  },
  created () {
    $.urlParam = function(name) {
      var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
      var ret = results[1] || 0;
      return decodeURIComponent(ret);
    }
    console.log($.urlParam("service_group"));
    console.log($.urlParam("logline"));
    this.current_service_group = $.urlParam("service_group");
    this.escapeAndChange ($.urlParam("logline"));
    this.loadServiceGroups ();

    $(function() {

      window.prettyPrint && prettyPrint();

      $('#colorselector').colorselector();

    });
    this.colorselector = 'Debug';
  }



}
</script>

<style scoped>
label {
  display: inline-block;
  max-width: 100%;
  margin-bottom: 5px;
  font-weight: 700;
  font-size: 14px;
  font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
}
</style>
