<template>
  <div>
    <h5 class="mb-3">Calculates <em>n!</em> (the factorial of <em>n</em>)</h5>
    <Calculator
      :paramKeys="params"
      :warningLimit="100000"
      funcLabel="n!"
      prefix="factorial"
      url="/api/factorial"
    />
  </div>
</template>

<script>
import Calculator from "@/components/Calculator";

export default {
  name: "Factorial",
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
