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
            v-model="message"
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
              <div class="resault" v-for="data in geojsonData" :key="data.title">
                 <a
                    target="_blank"
                    :href="'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + data.gseid" 
                    >
                    <span class="resault">{{ data.title }}</span>
                    </a>  
                </div>
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
import geo from '../data/GEO_papers.json'
import omim from '../data/OMIM_intro.json'

export default {
  name:'Vue',
  components: {
    //JsonViewer
  },

  data(){
    return {
      geojsonData:geo,
      ominjsonData:omim,
      message:this.$route.params.input,
    }
  },
  //搜索功能待定
  mounted:{
    search(quary,data){
      var resault=[];
      for(var i=0;i<data.length();i++){
        var words=data[i].title.split();
        if(words.include(quary)){
          resault.append(data[i])
        }
      }
      return resault
    }
  }
};
</script>

<style>
  .q-search{
    margin-top: 5vh;
    margin-left: 20vw;
  }
  .search{
    margin-top: 5vh;
    margin-left: 3vw;
  }
  .resault{
    margin-top: 5vh;
    margin-left: 2vw;
    margin-right: 2vw;
  }
</style>
