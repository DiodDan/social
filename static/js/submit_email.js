document.addEventListener("input", submitForm);
function submitForm(event) {
    if (event.target.closest("input[type=text]")) {
        if (document.querySelector("input[type=text]").value.length == 6) {
            document.querySelector("form").submit();
        }
    }
}