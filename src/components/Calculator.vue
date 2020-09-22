<template>
  <div>
    <b-form @submit="onSubmit" :inline="paramKeys.length < 2">
      <b-form-group
        :id="`input-group-${prefix}-${pk}`"
        :key="i"
        :label-for="`input-${prefix}-${pk}`"
        label-cols="1"
        v-for="(pk, i) in paramKeys"
      >
        <template v-slot:label>
          <strong>{{ pk + ":" }}</strong>
        </template>
        <b-form-input
          :disabled="loading"
          :id="`input-${prefix}-${pk}`"
          class="ml-2"
          min="0"
          required
          type="number"
          v-model="params[pk]"
        />
      </b-form-group>
      <b-button
        @click="calculate"
        :disabled="loading"
        :variant="loading ? 'secondary' : 'primary'"
      >
        <span v-if="loading"> <b-spinner small /> Loading...</span>
        <span v-else>Calculate</span>
      </b-button>
    </b-form>

    <span v-if="showWarning" class="mt-3 smaller text-danger">
      Warning: values this large may calculate slowly </span
    ><br />

    <span v-if="processingTime" class="mt-3 smaller text-secondary">
      Calculation time: {{ processingTime }} </span
    ><br />
    <span v-if="responseTime" class="smaller text-secondary">
      Total response time: {{ responseTime }} </span
    ><br />
    <p v-if="value" class="mt-3 wrap-value">
      <strong>{{ funcLabel }}</strong> = <Results :value="value" />
    </p>
  </div>
</template>

<script>
import Results from "@/components/Results.vue";

export default {
  name: "Calculator",
  components: {
    Results
  },
  props: {
    funcLabel: String,
    paramKeys: Array,
    prefix: String,
    url: String,
    warningLimit: Number
  },
  data() {
    return {
      error: "",
      loading: false,
      params: {},
      processingTime: "",
      responseTime: "",
      value: null
    };
  },

  computed: {
    showWarning() {
      for (const val of Object.values(this.params)) {
        if (parseInt(val, 10) >= this.warningLimit) {
          return true;
        }
      }
      return false;
    }
  },
  methods: {
    clearData() {
      this.value = null;
      this.responseTime = "";
      this.processingTime = "";
      this.error = "";
    },
    calculate() {
      this.$store.commit("clearAlert");
      this.clearData();
      this.loading = true;

      const qp = Object.entries(this.params)
        .map(([k, v]) => {
          return `${k}=${v}`;
        })
        .join("&");

      const resp = fetch(`${this.url}?${qp}`)
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            this.$store.commit("setAlert", {
              message: data.error,
              variant: "danger"
            });
          } else {
            this.value = data.value;
            this.processingTime = data.processingTime;
          }
          this.responseTime = data.responseTime;
        })
        .catch(error => {
          this.$store.commit("setAlert", {
            message: error,
            variant: "danger"
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onSubmit(e) {
      e.preventDefault();
      this.calculate();
    }
  },
  mounted() {
    // Dynamically setup our params based on the parameter keys passed as an array
    for (const key of this.paramKeys) {
      this.$set(this.params, key, 1);
    }
  }
};
</script>

<style scoped>
#input-group-n {
  font-weight: bold;
  font-size: 1.2rem;
}

.smaller {
  font-size: 0.9rem;
}

.stats {
  color: grey;
}
</style>
