<template>
    <div class ="container">
        <b-form id="connection" v-on:submit.prevent="sendConn()">
            <b-form-input 
                id="connection_request"
                v-model="partner"
                placeholder="Partner Email or Organization Name"
            ></b-form-input>
            <b-form-select v-model="partner">
                <optgroup label="Organizations">
                    <option :value="org" v-for="org in orgs" v-bind:key="org">{{ org }}</option>
                </optgroup>
                <optgroup label="Users">
                    <option :value="usr" v-for="usr in users" v-bind:key="usr">{{ usr }}</option>
                </optgroup>

            </b-form-select>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button variant="primary" @click="loadConn()">Refresh</b-button>
        </b-form>

        <connection 
        v-for="conn in conenctions" 
        v-bind:wallet="conn.wallet" 
        v-bind:partner="conn.partner_name"
        v-bind:status="conn.status" 
        v-bind:type="conn.type"
        v-bind:key="conn.wallet"
        ></connection>
      
        
    </div>
</template>
<script>
import axios from 'axios'
import Vue from 'vue'
export default {
    data() {
        return {
            partner: '',
            conenctions: [],
            users: [],
            orgs: []
        }
    },
    methods:{
        
        loadConn(){
            var vm = this;
            axios.get('http://localhost:8000/ext/list_conn/')
            .then(function(response){
                vm.conenctions = response.data;
                console.log(vm.conenctions);
            })
        },

        loadOrgs(){
            var vm = this;
            axios.get('http://localhost:8000/ext/list_org/')
            .then(function(response){
                vm.orgs = response.data;
            })
        },

        loadUsrs(){
            var vm = this;
            axios.get('http://localhost:8000/ext/list_usr/')
            .then(function(response){
                vm.users = response.data;
            })
        },
        
        sendConn(){
            var vm = this;

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.get('http://localhost:8000/ext/wallet')
            .then(function(res){
                var testStr = 'wallet_name='+res.data.wallet+'&partner_name='+vm.partner
                axios.post('http://localhost:8000/ext/conn/', testStr)
                .then(function(res){
                    console.log(res.data);
                })
                .catch(function(err){

                });
            })
            
        },

        
    },
    created() {
        this.loadConn();
        this.loadOrgs();
        this.loadUsrs();
    },
    
}

Vue.component('connection', {
    props:['wallet', 'partner', 'status', 'type'],
    template:'<b-card bg-variant="info" text-variant="white">\
    <h3>{{ partner }}</h3>\
    <h5>Status: {{ status }}    Type: {{ type }}</h5>\
    <div id="req">\
    <a class = pfReq href="#" v-if=\'status === "Active"\'><h5>Send proof request</h5></a>\
    <a class = pfReq href="#" v-if=\'type === "Outbound" && status === "Active"\'><h5>Send Credential</h5></a>\
    </div>\
    </b-card>'
})
</script>

<style>
.pfReq{
    text-decoration: none;
    color: white;
    display: inline-block;
    margin-right: 2vh;
}
.pfReq:hover{
    color:lightgray;
}
#req{
    display: inline-block;
}
</style>

