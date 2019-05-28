<template>
    <div class = "container">

        <b-form v-on:submit.prevent="submit()">
            <b-form-group id="signin" label="Sign In">
                

                <b-form-input 
                    id="signin-email"
                    v-model="email"
                    placeholder="Email"
                    type="email"
                    required
                ></b-form-input>

                <b-form-input 
                    id="signin-password"
                    v-model="password"
                    placeholder="Password"
                    required
                    type="password"
                ></b-form-input>

                

            </b-form-group>

            <b-button type="submit" variant="primary">Submit</b-button>
        </b-form>

        
    </div>
</template>
<script>
import axios from 'axios'
import Vue from 'vue'
export default {
    
    data:{
        username:'',
        password:'',
        next: '%2Findy%2Fprofile%2F'
    },
    created: function(){
        
    },
    methods: {
        submit(){
            var vm = this;
            var dataStr = 'username='+vm.email+'&password='+vm.password+'&next=%2Findy%2Fprofile%2F'
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
            axios.post('http://localhost:8000/indy/', dataStr)
                .then(function (response) {
                    var loginRe = /<title>Title<\/title>/g;
                    var res = response.data.match(loginRe);
                    if(!res){
                        alert('login incorrect!');
                    }else{
                        vm.redirect('home');
                    }
                    //currentObj.output = response.data;
                    // console.log(response.status +": "+JSON.stringify(response));
                    
                })
                .catch(function (error) {
                    //currentObj.output = error;
                });
        },
        redirect(path) {
            this.$router.push('/' + path);
        }
    }
}
</script>

