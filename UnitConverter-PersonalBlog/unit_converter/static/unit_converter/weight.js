import { converter } from "./util.js";

converter({
  converterForm: "#weight-converter",
  value: "#weight",
  fromUnit: "#from-weight",
  toUnit: "#to-weight",
  route: "/unit_converter/weight",
});
