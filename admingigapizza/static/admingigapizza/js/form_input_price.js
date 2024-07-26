document.addEventListener("DOMContentLoaded", function() {
    const priceInput = document.querySelector("#id_price");

    priceInput.addEventListener("input", function(event) {
        let value = event.target.value;
        
        value = value.replace(/[^\d]/g, "");

        let intValue = parseInt(value, 10);

        if (!isNaN(intValue)) {
            value = (intValue / 100).toFixed(2);
            console.log(value)
        } else {
            value = "0.00";
        }

        event.target.value = value;
    });
});