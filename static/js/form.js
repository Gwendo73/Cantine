const form = document.querySelector('form');
const phone = document.querySelector('input[name="phone"]');
const button = document.querySelector('button')

phone.addEventListener("keyup", function (event) {
    if (event.keyCode > 0) {
        console.log(phone.value)
        event.preventDefault();
        if (phone.value.length == 10) {
            button.disabled = false
        } else {
            button.disabled = true
        }
    }
});