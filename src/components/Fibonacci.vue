<template>
  <div>
    <h5 class="mb-3">
      Calculates the <em>nth</em> number in the Fibonacci sequence
    </h5>
    <Calculator
      :paramKeys="params"
      :warningLimit="500000"
      funcLabel="f(n)"
      prefix="fibonacci"
      url="/api/fibonacci"
    />
  </div>
</template>

<script>
import Calculator from "@/components/Calculator";
export default {
  name: "Fibonacci",
  components: {
    Calculator
  },
  data() {
    return {
      params: ["n"]
    };
  }
};
</script>

<style scoped></style>
