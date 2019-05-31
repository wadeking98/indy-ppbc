<template>
  <div id="app">
    <div id="nav">
      <b-navbar toggleable="md" type="dark" variant="dark" v-if="this.$router.currentRoute.name != 'login'">
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand>
          <router-link to="/home">Health Gateway</router-link>
        </b-navbar-brand>
        <b-collapse is-nav id="nav_collapse">
          <b-navbar-nav class="ml-auto">
            <b-nav-item>
              <router-link to="/medications">Medications</router-link>
            </b-nav-item>
            <b-nav-item>
              <router-link to="/immunizations">Immunizations</router-link>
            </b-nav-item>
            <b-nav-item>
              <router-link to="/lab-results">Lab Results</router-link>
            </b-nav-item>
            <b-nav-item>
              <router-link to="/profile">Profile</router-link>
            </b-nav-item>
            <b-nav-item>
              <router-link to="/connections">Connections</router-link>
            </b-nav-item>
            <b-nav-item>
              <div v-on:click="logout()" >Logout</div>
            </b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
      <b-navbar v-else toggleable="md" type="dark" variant="dark">
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand>
          <router-link to="/home">Health Gateway</router-link>
        </b-navbar-brand>
      </b-navbar>
    </div>

    <router-view/>
  </div>
</template>
<script>
import axios from 'axios'
import Vue from 'vue'
export default {
  methods:{
    redirect(path) {
        this.$router.push('/' + path);
    },
    logout(){
      var vm = this;
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
      axios.get('http://localhost:8000/indy/accounts/logout/')
        .then(function(response){
          vm.redirect('');
      })
        .catch(function(error){

        });
    },
  }
}
</script>


<style>
/* Global styles go here */
#app {
  font-family: "Arial";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
}

#nav a {
  color: #ffffff;
}

#nav a.router-link-exact-active {
  color: #ffffff;
}
</style>
