import { converter } from "./util.js";

converter({
  converterForm: "#temperature-converter",
  value: "#temperature",
  fromUnit: "#from-temperature",
  toUnit: "#to-temperature",
  route: "/unit_converter/temperature",
});
