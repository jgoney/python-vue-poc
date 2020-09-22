<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">Home programming assignment</b-navbar-brand>
    </b-navbar>
    <b-alert v-model="showAlert" :variant="alertVariant" dismissible>
      {{ alertMessage }}
    </b-alert>
    <b-container>
      <b-row>
        <b-col>
          <b-tabs content-class="mt-3">
            <b-tab title="Fibonacci">
              <Fibonacci />
            </b-tab>
            <b-tab title="Ackermann">
              <Ackermann />
            </b-tab>
            <b-tab title="Factorial">
              <Factorial />
            </b-tab>
          </b-tabs>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { mapState } from "vuex";

import Ackermann from "@/components/Ackermann";
import Factorial from "@/components/Factorial";
import Fibonacci from "@/components/Fibonacci";

export default {
  name: "App",
  components: {
    Ackermann,
    Factorial,
    Fibonacci
  },
  computed: {
    ...mapState(["alertMessage", "alertVariant"]),
    showAlert: {
      get() {
        return this.$store.state.showAlert;
      },
      set() {
        this.$store.commit("clearAlert");
      }
    }
  }
};
</script>

<style></style>
