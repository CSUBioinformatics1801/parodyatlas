<template>
<v-app id="inspire">
    <v-app-bar
      app
      color="white"
      flat
    >
      <v-container class="py-0 fill-height">
        <v-btn
          @click="tomember"
        >
          member
        </v-btn>
      </v-container>
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <v-row>
          <v-col cols="auto" class="q-search">
            <p >疾病名：</p>
          </v-col>
          <v-col cols="4" class="search">
            <img height="100px" width="130px" class="search-tu" src="../assets/search.png">
            <v-text-field
              label="请输入search"
              dense
              persistent-hint
              rounded
              solo-inverted
              background-color="grey"
              append-outer-icon="mdi-arrow-right-box"
              @click:append-outer="toresault"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
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
  .q-search{
    margin-top:36vh;
    margin-left: 20vw;
  }
  .search-tu{
    margin-left: 5vw;
  }
  .search{
    margin-top:20vh;
    margin-left: 3vh;
  }
</style>
