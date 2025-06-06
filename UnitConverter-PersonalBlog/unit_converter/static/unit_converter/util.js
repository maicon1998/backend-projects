export function converter(params) {
  document.addEventListener("DOMContentLoaded", () => {
    const CONVERTER_FORM = document.querySelector(params.converterForm);
    const RESULT = document.querySelector("#result");
    CONVERTER_FORM.addEventListener("submit", (event) => {
      event.preventDefault();
      const VALUE = document.querySelector(params.value).value;
      const FROM_UNIT = document.querySelector(params.fromUnit).value;
      const TO_UNIT = document.querySelector(params.toUnit).value;

      fetch(params.route, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body: JSON.stringify({
          value: VALUE,
          from_unit: FROM_UNIT,
          to_unit: TO_UNIT,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          CONVERTER_FORM.style.display = "none";
          document.querySelector("#description").innerText =
            `Result of your calculation: ${data.result}`;
          RESULT.style.display = "flex";
        })
        .catch((error) => console.error("Fetch error:", error));
    });
    document.querySelector("#reset").addEventListener("click", () => {
      document.querySelector(params.value).value = "";
      RESULT.style.display = "none";
      CONVERTER_FORM.style.display = "block";
    });
  });
}
