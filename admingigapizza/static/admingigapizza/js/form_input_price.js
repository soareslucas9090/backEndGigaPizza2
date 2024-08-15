document.addEventListener("DOMContentLoaded", function() {
    const priceInputs = document.querySelectorAll(".price-input");
    const priceInput = document.querySelector("#id_price");

    function formatPriceInput(inputElement) {
        inputElement.addEventListener("input", function(event) {
            let value = event.target.value;
            
            value = value.replace(/[^\d]/g, "");

            let intValue = parseInt(value, 10);

            if (!isNaN(intValue)) {
                value = (intValue / 100).toFixed(2);
            } else {
                value = "0.00";
            }

            event.target.value = value;
        });
    }

    if (priceInput) {
        formatPriceInput(priceInput);
    }

    priceInputs.forEach(function(inputElement) {
        formatPriceInput(inputElement);
    });
});
