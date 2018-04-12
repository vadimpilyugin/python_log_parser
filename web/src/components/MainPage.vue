<template>
  <div>
  <aggregation 
    style="margin-bottom: 20px;margin-top: 20px;"
    endpoint='http://localhost:5000/distribution'
    stat-id="0"
    :danger="false">
    
  </aggregation>

  <aggregation 
    style="margin-bottom: 20px;margin-top: 20px;"
    endpoint='http://localhost:5000/distribution'
    stat-id="1"
    :danger="false">
    
  </aggregation>
  <aggregation 
    endpoint='http://localhost:5000/distribution'
    stat-id="2"
    :danger="true"
    v-if="failed_services"
    >
    
  </aggregation>
  <aggregation 
    endpoint='http://localhost:5000/distribution'
    stat-id="3"
    :danger="true"
    v-if="failed_templates"
    >
    
  </aggregation>
  <aggregation 
    endpoint='http://localhost:5000/distribution'
    stat-id="4"
    :danger="true"
    v-if="failed_formats"
    >
    
  </aggregation>
</div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      failed_services_ep: 'http://localhost:5000/distribution/failed/services',
      failed_templates_ep: 'http://localhost:5000/distribution/failed/templates',
      failed_formats_ep: 'http://localhost:5000/distribution/failed/formats',
      failed_services:false,
      failed_templates:false,
      failed_formats:false
    }
  },
  methods: {
    check_ep(ep, field) {
      axios(
        {
          method: 'get',
          url: ep
        }
      ).then(response => {
        this[field] = response.data['__PAYLOAD__']
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
    }
  },
  created() {
    this.check_ep (this.failed_services_ep, 'failed_services')
    this.check_ep (this.failed_templates_ep, 'failed_templates')
    this.check_ep (this.failed_formats_ep, 'failed_formats')
  }
}
</script>

<style>

</style>
