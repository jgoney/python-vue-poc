<template functional>
  <b-form-textarea
    id="textarea"
    v-model="props.value"
    readonly
    plaintext
    max-rows="24"
  ></b-form-textarea>
</template>

<script>
export default {
  name: "Results",
  props: {
    value: String
  }
};
</script>

<style scoped></style>
