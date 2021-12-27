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

        <v-spacer></v-spacer>
        <p >疾病名：</p>
        <v-responsive max-width="260">
          <v-text-field
            dense
            flat
            hide-details
            rounded
            solo-inverted
          ></v-text-field>
        </v-responsive>
      </v-container>
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <v-row>
          <v-col cols="2">
            <v-sheet rounded="lg">
              <v-list color="transparent">
                <v-list-item
                  v-for="n in 5"
                  :key="n"
                  link
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      疾病 {{ n }}
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>

                <v-divider class="my-2"></v-divider>

              </v-list>
            </v-sheet>
          </v-col>

          <v-col>
            <v-sheet
              min-height="70vh"
              rounded="lg"
            >
              <div v-for="data in jsonData" :key="data.title">{{ data.title }}</div>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
// import HelloWorld from './components/HelloWorld';
// import JsonViewer from 'vue-json-viewer'
import test from '../data/test.json'

export default {
  name: 'App',

  components: {
    //JsonViewer
  },

  data(){
    return {
      jsonData:test
    }
  },
};
</script>

<style>
  .q-search{
    margin-top: 5vh;
    margin-left: 20vw;
  }
  .search{
    margin-top: 5vh;
    margin-left: 3vh;
  }
</style>
