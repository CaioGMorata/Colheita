<template>
  <div id="app" v-if="info == empty">
    <h1>Colheita de maçãs</h1>
    <div id="Vetor_A" v-text="Vetor_A"></div>
    <input type="text" v-model="vetor_pomar" placeholder="vetor_pomar">
    <div id="Vetor_A" v-text="Arvores_Carla"></div>
    <input type="text" v-model="numero_carla" placeholder="numero_carla">
    <div id="Vetor_A" v-text="Arvores_Marcelo"></div>
    <input type="text" v-model="numero_marcelo" placeholder="numero_marcelo">
    <div id="Vetor_A"></div>
    <button @click="enviar_dados">Enviar dados</button>
  </div>
  <div id="app" v-else>
    <table border="1px">
      <tr>
        <td>Posições das árvores escolhidas pelo Marcelo</td>
        <td>Número de maçãs por árvores escolhidas pelo Marcelo</td>
        <td>Posições das árvores escolhidas pela Carla</td>
        <td>Número de maçãs por árvores escolhidas pela Carla</td>
        <td>Quantidade total de maçãs coletadas</td>
      </tr>
      <tr v-for="item in info" v-bind:key="item">
        <td>{{item[0].Indices_K}}</td>
        <td>{{item[0].Qtd_por_Arvore_K}}</td>
        <td>{{item[0].Indices_L}}</td>
        <td>{{item[0].Qtd_por_Arvore_L}}</td>
        <td>{{item[0].Numero_total_de_macas_coletadas}}</td>
      </tr>
    </table>
  </div>
</template>

<!-- <tr v-for="item in info" v-bind:key="item">
        <td>{{item[0].Indices_K}}</td>
        <td>{{item[0].Indices_L}}</td>
        <td>{{item[0].Numero_total_de_macas_coletadas}}</td>
      </tr> -->
<script>
import axios from 'axios';
export default {
  data(){
    return {
      title_app: 'Colheita de maçãs',
      Vetor_A: 'Disposição das maçãs nas árvores',
      Arvores_Carla: 'Número de árvores coletadas pela Carla',
      Arvores_Marcelo: 'Número de árvores coletadas pelo Marcelo',
      vetor_pomar: '',
      numero_carla: '',
      numero_marcelo: '',
      info: undefined
    }
  },
  methods: {
    enviar_dados: function() {
        axios.get('http://127.0.0.1:8080/hello/api/v1.0/tasks/' + this.numero_marcelo + '/' + this.numero_carla + '/' + this.vetor_pomar)
      .then(resposta => { 
        (this.info = resposta.data)
        console.log(resposta)
    }).catch(error => console.log(error))
      
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: rgb(255, 0, 64);
  margin-top: 60px;
}
#Vetor_A {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: rgb(255, 0, 64);
  margin-top: 60px;
  height: 100px;
}
</style>
