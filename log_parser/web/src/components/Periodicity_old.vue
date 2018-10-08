<template>
  <div class="card border-light">
    <div class="card-header">
      <h5 class="mb-0">
        <a data-toggle="collapse" :href="'#'+main_anchor">
          Найденные периодичности
        </a>

      </h5>
    </div>
    <div :id="main_anchor" class="collapse">
      <div class="card-body">
        <div class="card mb-3">
          <div class="card-header">
            <h5 class="mb-0">
              <a data-toggle="collapse" :href="'#'+first_anchor">
                Большой период, малая активность
              </a>
              <span class="badge badge-secondary">{{interesting.length}}</span>
            </h5>
          </div>
          <div :id="first_anchor" class="collapse">
            <div class="card-body" >
              <div class="card mb-3" v-for="item in interesting">
                <div class="card-header">
                  <h5 class="mb-0">
                    <a data-toggle="collapse" :href="'#'+item.anchor_id">
                      {{item.name}}
                    </a>
                    <span class="badge badge-secondary">{{item.n_lines}}</span>
                  </h5>
                </div>
                <div :id="item.anchor_id" class="collapse card-body" style="padding-top: 1.25rem;padding-bottom: 0;">
                  <h5 class="card-title"> Характеристики </h5>
                  <p>Тип события: "user_ip": "109.86.247.183", "__CATEGORY__": "New connection"<br>
                  Период: {{item.period}} секунд<br>
                  Отношение mean/std: {{item.mean_std}}</p>
                  <div class="choice">
                    <button class="btn btn-success" style="margin-right: 1rem;"> Сохранить </button>
                    <button class="btn btn-secondary"> Не уведомлять </button>
                  </div>
                  <h5 class="card-title"> Сообщения </h5>
                  <table class="table table-sm">
                    <caption><a href="#"> Показать еще... </a></caption>
                    <thead>
                      <tr>
                        <th scope="col">Дата</th>
                        <th scope="col">Сообщение</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="row in item.lines">
                        <td>{{row.date}}</td>
                        <td>{{row.msg}}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card mb-3">
          <div class="card-header">
            <h5 class="mb-0">
              <a data-toggle="collapse" :href="'#'+second_anchor">
                Большой период, высокая активность
              </a>
              <span class="badge badge-secondary">{{autocheck.length}}</span>
            </h5>
          </div>
          <div :id="second_anchor" class="collapse">
            <div class="card-body">
              
            </div>
          </div>
        </div>
        <div class="card mb-3">
          <div class="card-header">
            <h5 class="mb-0">
              <a data-toggle="collapse" :href="'#'+third_anchor">
                Малый период, высокая активность
              </a>
              <span class="badge badge-secondary">{{bots.length}}</span>
            </h5>
          </div>
          <div :id="third_anchor" class="collapse">
            <div class="card-body">
              
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      main_anchor : "periodicity",
      first_anchor : "periodicity0",
      second_anchor : "periodicity1",
      third_anchor : "periodicity2",
      interesting: [
        {
          name : '109.86.247.183, New connection',
          anchor_id : 'n1',
          n_lines : 5,
          keys : {
            user_ip : '109.86.247.183',
            __CATEGORY__ : 'New connection'
          },
          period : '5740',
          mean_std : '24',
          lines : []
        },
        {
          name : '109.86.247.183, 93.180.9.8',
          anchor_id : 'n2',
          n_lines : 5,
          keys : {
            user_ip : '109.86.247.183',
            server_ip : '93.180.9.8'
          },
          period : '5740',
          mean_std : '24',
          lines : []
        },
        {
          name : '143.107.220.201, New connection',
          n_lines : 10,
          anchor_id : 'n3',
          keys : {
            user_ip : '143.107.220.201',
            __CATEGORY__ : 'New connection'
          },
          period : '1201',
          mean_std : '19',
          lines : []
        },
        {
          name : '143.107.220.201, 93.180.9.8',
          n_lines : 10,
          anchor_id : 'n4',
          keys : {
            user_ip : '109.86.247.183',
            server_ip : '93.180.9.8'
          },
          period : '5740',
          mean_std : '24',
          lines : []
        },
        {
          name : '104.192.3.34, New connection',
          n_lines : 6,
          anchor_id : 'n5',
          keys : {
            user_ip : '104.192.3.34',
            __CATEGORY__ : 'New connection'
          },
          period : '14357',
          mean_std : '310',
          lines : [
            {date:'Dec 10 11:07:23',msg:'Connection from 104.192.3.34 port 53029 on 93.180.9.8 port 22'},
            {date:'Dec 10 15:07:37',msg:'Connection from 104.192.3.34 port 58830 on 93.180.9.8 port 22'},
            {date:'Dec 10 19:07:26',msg:'Connection from 104.192.3.34 port 44194 on 93.180.9.8 port 22'},
          ]
        },
        {
          name : '104.192.3.34, 93.180.9.8',
          n_lines : 6,
          anchor_id : 'n6',
          keys : {
            user_ip : '104.192.3.34',
            server_ip : '93.180.9.8'
          },
          period : '14357',
          mean_std : '310',
          lines : []
        },
      ],
      autocheck:[
        {
          name : 'autocheck',
          n_lines : 262,
          anchor_id : 'n7',
          keys : {
            username : 'username',
          },
          period : '329',
          mean_std : '20',
          lines : []
        },
        {
          name : '93.180.9.182',
          n_lines : 262,
          anchor_id : 'n8',
          keys : {
            user_ip : '93.180.9.182',
          },
          period : '0',
          mean_std : '0',
          lines : []
        },
        // (('autocheck',), (329.1, 20.2, 262)),
        // (('93.180.9.182',), (327.6, 15.3, 262)),
      ],
      bots:[
        // (('103.99.0.205', 'New connection'), (8.0, 10.4, 30)),
        // (('103.99.0.205', '93.180.9.8'), (8.0, 10.4, 30)),
        {
          name : '103.99.0.205, New connection',
          n_lines : 30,
          anchor_id : 'n9',
          keys : {
            user_ip : '103.99.0.205',
          },
          period : '0',
          mean_std : '0',
          lines : []
        },
        {
          name : '103.99.0.205, 93.180.9.8',
          n_lines : 262,
          anchor_id : 'n10',
          keys : {
            user_ip : '93.180.9.182',
          },
          period : '0',
          mean_std : '0',
          lines : []
        },
      ]
    }
  },
  created() {
    
  }
}
</script>

<style>
.card {
  max-width: 800px;
  width: 100%;
}
h5 {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.no-padding {
  padding: 0;
}
.choice {
  display: flex;
  flex-direction: row;
  margin-bottom: 2rem;
}
</style>
