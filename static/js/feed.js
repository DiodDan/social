const imgs = Array.from(document.querySelectorAll("div.block.post div.photo_block div.photo img"));
for (img of imgs) {
    console.log(img.src);
    let splImg = img.src.split(".");
    let type = splImg[splImg.length - 1];
    if (type == "mp4") {
        img.outerHTML = `<video preload="auto" controls src="${img.src}"></video>`;
    }
}

const photoInput = document.querySelector("div.main_page.head div.input div.choose_photo input[type=file]");
const photoMark = document.querySelector("div.main_page.head div.input div.choose_photo div.addition");

document.addEventListener("input", checkPhoto);
function checkPhoto(event) {
    if (event == "check" || event.target.closest("div.main_page.head div.input div.choose_photo input[type=file]")) {
        let name_format = photoInput.value.split(".");
        let format = name_format[name_format.length - 1];
        if ((format == "jpg" || format == "jpeg" || format == "png" || format == "gif") && (name_format.length > 1) || photoInput.value == "") {
            photoMark.children[0].children[1].children[0].style.fill = "#3ED252";
            photoMark.children[2].innerHTML = "<h5>your photo satisfies the requirements!</h5>";
        }
        else {
            photoMark.children[0].children[1].children[0].style.fill = "#D23E3E";
            photoMark.children[2].innerHTML = `<h5>your photo extension should be <span style="font-weight: 500;">jpg, jpeg, png or gif</span>!</h5>`;
        }
    }
}

checkPhoto("check");

const divInput = document.querySelector("div.main_page.head div.input");
const form = document.querySelector("div.main_page.head div.input form");
form.addEventListener("submit", submitForm);
function submitForm(event) {
    event.preventDefault();
    let name_format = photoInput.value.split(".");
    let format = name_format[name_format.length - 1];
    if ((format == "jpg" || format == "jpeg" || format == "png" || format == "gif") && (name_format.length > 1) || photoInput.value == "") {
        form.submit();
    }
    else {
        divInput.insertAdjacentHTML('beforeend', '<h4 class="err">make sure you chose the correct photo!</h4>');
    }
}