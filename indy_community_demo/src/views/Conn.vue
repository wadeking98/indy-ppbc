<template>
    <div class ="container">
        
        <b-button v-on:click="adminLogin()">
            Create connection
        </b-button>
        
    </div>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            content: '',
            username: 'admin%40mail.com',
            password: ''
        }
    },
    methods:{
        loadConn(){
            var vm = this;
            axios.get('http://localhost:8000/indy/list_connections/')
            .then(function(response){
                vm.content = response.data;
                console.log(response.data.head);
            })
        },
        adminLogin(){
            var vm = this;
            var dataStr = "username=admin%40mail.com&password=pass1234&next=%2Fadmin%2F"
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            //login as admin
            axios.post('http://localhost:8000/admin/login/', dataStr)
            .then(function(response){
                var connStrIn = 'wallet=i_wade_mail_com&partner_name=bcgov%40mail.com&invitation=&token=&status=Active&connection_type=InBound&connection_data=&_save=Save';
                var connStrOut = 'wallet=o_bcgov&partner_name=wade%40mail.com&invitation=&token=&status=Active&connection_type=OutBound&connection_data=&_save=Save';
                //add a connection in one direction through django admin
                axios.post('http://localhost:8000/admin/indy_community/agentconnection/add/', connStrIn)
                .then(function(response){
                    console.log('inbound connection success!')
                })
                .catch(function(err){
                    console.log(err);
                });

                //add a connection in the other direction, this can be done synchroneously
                axios.post('http://localhost:8000/admin/indy_community/agentconnection/add/', connStrOut)
                .then(function(response){
                    console.log('outbound connection success!')
                })
                .catch(function(err){
                    console.log(err);
                });
            })
            .catch(function(err){
                console.log(err);
            });
        }
    },
    
}
</script>
