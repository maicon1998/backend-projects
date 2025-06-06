import { converter } from "./util.js";

converter({
  converterForm: "#length-converter",
  value: "#length",
  fromUnit: "#from-length",
  toUnit: "#to-length",
  route: "/unit_converter/length",
});
