<template>
<v-app id="inspire">
  <router-view />

  </v-app>
</template>

<script>

export default {
  methods:{
    tosearch:function(){
      this.$router.push({
        path:'/search'
        });
    },
    toresault:function(){
      this.$router.push({
        path:'/resault'
        });
    },
    tomember:function(){
      this.$router.push({
        path:'/member'
      })
    }
  }
}
</script>

<style>

</style>
