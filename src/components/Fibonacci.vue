<template>
  <div>
    <h5 class="mb-3">
      Calculates the <em>nth</em> number in the Fibonacci sequence
    </h5>
    <b-form @submit="onSubmit" inline>
      <b-form-group id="input-group-n" label="n:" label-for="input-n">
        <b-form-input
          :disabled="loading"
          class="ml-2"
          id="input-n"
          min="1"
          required
          type="number"
          v-model="n"
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

    <span v-if="n >= 500000 && loading" class="mt-3 smaller text-danger">
      Please wait, this could take a while...</span
    >

    <span v-if="processing_time" class="mt-3 smaller text-secondary">
      Calculation time: {{ processing_time }} </span
    ><br />
    <span v-if="response_time" class="smaller text-secondary">
      Total response time: {{ response_time }} </span
    ><br />
    <p v-if="value" class="mt-3 wrap-value">
      <strong>F(n)</strong> = {{ value }}
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      n: 1,
      value: null,
      processing_time: "",
      response_time: "",
      loading: false,
      error: ""
    };
  },
  methods: {
    clearData() {
      this.value = null;
      this.response_time = "";
      this.processing_time = "";
      this.error = "";
    },
    calculate() {
      this.clearData();
      this.loading = true;
      const resp = fetch(`/api/fibonacci?n=${this.n}`)
        .then(response => response.json())
        .then(data => {
          this.value = data.value;
          this.response_time = data.response_time;
          this.processing_time = data.processing_time;
          this.error = data.error;
        })
        .catch(error => {
          console.error("Error:", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onSubmit(e) {
      e.preventDefault();
      this.calculate();
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

.wrap-value {
  overflow-wrap: anywhere;
}
</style>
