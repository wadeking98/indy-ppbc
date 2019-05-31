<template>
    <div class ="container">
        
        <span v-html="content"></span>
        
    </div>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            content: ''
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
        }
    },
    beforeMount() {
        this.loadConn();
    },
}
</script>
