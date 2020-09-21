<template>
  <div>
    <h5 class="mb-3">
      Calculates the Ackermann function =>
      <em>A(m,n)</em>
    </h5>
    <Calculator
      :paramKeys="params"
      :warningLimit="4"
      funcLabel="A(m,n)"
      url="/api/ackermann"
    />
  </div>
</template>

<script>
import Calculator from "@/components/Calculator";
export default {
  name: "Ackermann",
  components: {
    Calculator
  },
  data() {
    return {
      params: ["m", "n"]
    };
  }
};
</script>

<style scoped></style>
