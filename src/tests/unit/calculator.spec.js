import { createLocalVue, mount } from "@vue/test-utils";
import BootstrapVue from "bootstrap-vue";
import Vuex from "vuex";

import Calculator from "@/components/Calculator";
import store from "@/store";

// create an extended `Vue` constructor
const localVue = createLocalVue();

// install plugins as normal
localVue.use(BootstrapVue);
localVue.use(Vuex);

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve({
        value: "125",
        responseTime: "5",
        processingTime: "10"
      })
  })
);

let wrapper;

describe("Calculator", () => {
  beforeAll(() => {
    fetch.mockClear();

    wrapper = mount(Calculator, {
      localVue,
      store,
      propsData: {
        funcLabel: "n!",
        paramKeys: ["n"],
        prefix: "factorial",
        url: "/api/factorial",
        warningLimit: 1000000
      }
    });
  });

  it("mounts with basic text", () => {
    // Assert the rendered text of the component
    expect(wrapper.text()).toContain("Calculate");
    expect(wrapper.text()).toContain("n:");
  });

  it("shows warning text if input is > warningLimit", async () => {
    await wrapper.setData({ params: { n: 10000000 } });
    expect(wrapper.text()).toContain(
      "Warning: values this large may calculate slowly"
    );
  });

  it("resolves with mock data on click", async done => {
    await wrapper.setData({ params: { n: 1 } });

    const button = wrapper.find("button");

    await button.trigger("click");
    expect(wrapper.text()).toContain("Loading...");

    expect(global.fetch).toHaveBeenCalledWith("/api/factorial?n=1");

    wrapper.vm.$nextTick(() => {
      wrapper.vm.$nextTick(() => {
        wrapper.vm.$nextTick(() => {
          wrapper.vm.$nextTick(() => {
            expect(wrapper.text()).toContain("Calculation time: 10");
            expect(wrapper.text()).toContain("Total response time: 5");

            done();
          });
        });
      });
    });
  });
});
