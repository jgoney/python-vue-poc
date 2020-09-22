import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    showAlert: false,
    alertMessage: "",
    alertVariant: ""
  },
  mutations: {
    setAlert(state, alert) {
      state.alertMessage = alert.message;
      state.alertVariant = alert.variant || "warning";
      state.showAlert = true;
    },
    clearAlert(state) {
      state.showAlert = false;
      state.alertMessage = "";
      state.alertVariant = "";
    }
  },
  strict: process.env.NODE_ENV !== "production"
});
