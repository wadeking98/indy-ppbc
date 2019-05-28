<template>
    <div class = "container">
        <p>hello world! 2</p>
        <b-form v-on:submit.prevent="submit()">
            <b-form-group id="signup" label="Sign Up">
                <b-form-input 
                    id="signup-fname"
                    v-model="first_name"
                    placeholder="First Name"
                ></b-form-input>

                <b-form-input 
                    id="signup-lname"
                    v-model="last_name"
                    placeholder="Last Name"
                ></b-form-input>

                <b-form-input 
                    id="signup-email"
                    v-model="email"
                    placeholder="Email"
                    type="email"
                    required
                ></b-form-input>

                <b-form-input 
                    id="signup-password1"
                    v-model="password1"
                    placeholder="Password"
                    required
                    type="password"
                ></b-form-input>

                <b-form-input 
                    id="signup-password2"
                    v-model="password2"
                    placeholder="Confirm Password"
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
import { setTimeout } from 'timers';
export default {
    
    data:{
        first_name:'',
        last_name:'',
        email:'',
        password1:'',
        password2:'',
    },
    
    methods: {
        redirect(path) {
            this.$router.push('/' + path);
        },
        submit(){
            
            var vm = this;
            var dataStr = 'first_name='+vm.first_name+'&last_name='+vm.last_name+'&email='+vm.email+'&password1='+vm.password1+'&password2='+vm.password2

            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
            axios.post('http://localhost:8000/indy/signup/', dataStr)
                .then(function (response) {
                    console.log(response.status +": "+JSON.stringify(response));
                    vm.redirect('home');
                })
                .catch(function (error) {
                    //currentObj.output = error;
                });
            
        },
        
        
    }
}
</script>

