<template>
  <div class="card border-light">
    <div class="card-header">
      <h5 class="mb-0">
        <a data-toggle="collapse" :href="'#'+main_anchor">
          Найденные блоки
        </a>

      </h5>
    </div>
    <div :id="main_anchor" class="collapse">
      <div class="card-body">
        <div class="card mb-3" v-for="(block,i) in blocks">
          <div class="card-header">
            <h5 class="mb-0">
              <a data-toggle="collapse" :href="'#block'+i">
                {{block.name}}
              </a>
              <span class="badge badge-secondary">{{block.count}}</span>
            </h5>
          </div>
          <div :id="'block'+i" class="collapse">
            <div class="card-body">
              <div class="block-body">
                <h5 class="card-title"> Информация о блоке </h5>
                <p> 
                  Число совпадений: {{block.count}}<br>
                  Число вариантов блока: {{block.seqs.length}}
                </p>
                <form class="mb-3">
                  <div class="form-group">
                    <label for="exampleInputEmail1">Название блока</label>
                    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" >
                  </div>
                  <div class="form-group">
                    <label for="exampleInputEmail1">Последовательность</label>
                    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" >
                  </div>
                  <button type="submit" class="btn btn-success">Сохранить</button>
                </form>
                <div class="sequences">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th scope="col">Последовательность</th>
                        <th scope="col">Число совпадений</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="row in block.seqs" data-toggle="tooltip" data-placement="right" title="Tooltip on right">
                        <td>{{ar_to_tuple(row.seq)}}</td>
                        <td>{{row.count}}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                    <pre> {{block.seqs[block.selected].lines}} </pre>
              </div>
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
      main_anchor : "blocks",
      blocks : [
        {
          name : 'Блок 1',
          count : 1926,
          selected : 0,
          seqs : [
            {
              seq : [375, 387, 389, 395, 403, 376, 378, 389],
              count : 987,
              lines : [
                '375 # Connection from 93.180.9.182 port 42850 on 93.180.9.8 port 22',
                '387 # Accepted publickey for autocheck from 93.180.9.182 port 42850 ssh2: RSA SHA256:EMJlgs25cBdZgixd0cGU31Uc1SoASY4IM2NLVq8LqlQ',
                '389 # pam_unix(sshd:session): session opened for user autocheck by (uid=0)',
                '395 # User child is on pid 13935',
                '403 # Starting session: command for autocheck from 93.180.9.182 port 42850 id 0',
                '376 # Received disconnect from 93.180.9.182 port 42850:11: disconnected by user',
                '378 # Disconnected from user autocheck 93.180.9.182 port 42850',
                '389 # pam_unix(sshd:session): session closed for user autocheck'
              ]
            },
            {
              seq : [375, 387, 389, 395, 403, 381, 376, 378, 389],
              count : 271,
              lines : [
                '375 # Connection from 93.180.9.182 port 44952 on 93.180.9.8 port 22',
                '387 # Accepted publickey for autocheck from 93.180.9.182 port 44952 ssh2: RSA SHA256:EMJlgs25cBdZgixd0cGU31Uc1SoASY4IM2NLVq8LqlQ',
                '389 # pam_unix(sshd:session): session opened for user autocheck by (uid=0)',
                '395 # User child is on pid 29212',
                '403 # Starting session: command for autocheck from 93.180.9.182 port 44952 id 0',
                '381 # Close session: user autocheck from 93.180.9.182 port 44952 id 0',
                '376 # Received disconnect from 93.180.9.182 port 44952:11: disconnected by user',
                '378 # Disconnected from user autocheck 93.180.9.182 port 44952',
                '389 # pam_unix(sshd:session): session closed for user autocheck',
              ]
            },
            {
              seq : [375,387,389,395,403,376,378,389,406],
              count : 79,
              lines : [
                '375 # Connection from 93.180.9.182 port 47408 on 93.180.9.8 port 22',
                '387 # Accepted publickey for autocheck from 93.180.9.182 port 47408 ssh2: RSA SHA256:EMJlgs25cBdZgixd0cGU31Uc1SoASY4IM2NLVq8LqlQ',
                '389 # pam_unix(sshd:session): session opened for user autocheck by (uid=0)',
                '395 # User child is on pid 29388',
                '403 # Starting session: command for autocheck from 93.180.9.182 port 47408 id 0',
                '376 # Received disconnect from 93.180.9.182 port 47408:11: disconnected by user',
                '378 # Disconnected from user autocheck 93.180.9.182 port 47408',
                '389 # pam_unix(sshd:session): session closed for user autocheck',
                '406 # Failed password for root from 42.7.26.60 port 54745 ssh2',
              ]
            },
            {
              seq : [375,387,389,395,403,378,389],
              count : 1,
              lines : [
                '375 # Connection from 93.180.9.182 port 47408 on 93.180.9.8 port 22',
                '387 # Accepted publickey for autocheck from 93.180.9.182 port 47408 ssh2: RSA SHA256:EMJlgs25cBdZgixd0cGU31Uc1SoASY4IM2NLVq8LqlQ',
                '389 # pam_unix(sshd:session): session opened for user autocheck by (uid=0)',
                '395 # User child is on pid 29388',
                '403 # Starting session: command for autocheck from 93.180.9.182 port 47408 id 0',
                '376 # Received disconnect from 93.180.9.182 port 47408:11: disconnected by user',
                '378 # Disconnected from user autocheck 93.180.9.182 port 47408',
                '389 # pam_unix(sshd:session): session closed for user autocheck',
                '406 # Failed password for root from 42.7.26.60 port 54745 ssh2',
              ]
            },
            // {
            //   seq : [],
            //   count : 0,
            //   lines : [

            //   ]
            // },
          ]
        }
      ]
    }
  },
  methods : {
    ar_to_tuple (ar) {
      return ar.join(', ')
    }
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
.example-messages {
  height: 70vh;
  overflow-y: scroll;
}
</style>
