function EmailCheck(email){
    let correct = true;
    let alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.";
    
    let splittedEmail = email.split("@");
    if (email.includes(".."))
        correct = false;
    else {
        if (splittedEmail.length != 2)
            correct = false;
        else {
            let name = splittedEmail[0];
            let address = splittedEmail[1];
            if (!name || !address)
                correct = false;
            else {
                if (name[0] == '.' || name[name.length - 1] == '.' || address[0] == '.' || address[address.length - 1] == '.')
                    correct = false;
                else {
                    let count = 0;
                    for (i of name) {
                        if (!alph.includes(i))
                            count += 1;
                    }
                    if (count != 0)
                        correct = false;
                    else {
                        count = 0;
                        for (i of address) {
                            if (!alph.includes(i))
                                count += 1
                        }
                        if (count != 0) {
                            correct = false;
                        }
                        else {
                            if (!address.includes(".")) {
                                correct = false;
                            }
                        }
                    }
                }
            }
        }
    }
    return correct;
};

function PasswordChecker(password){
    let res = {
        "length": true,
        "small_letter": false,
        "big_letter": false,
        "number": false,
        "symbol": false
    };

    /*
    0 - длина >= 8
    1 - есть маленькая буква
    2 - есть большая буква
    3 - есть цифра
    4 - есть символ
    */

    if (password.length < 8) {
        res["length"] = false;
    }
    symbols_tir_1 = "qwertyuiopasdfghjklzxcvbnm";
    symbols_tir_2 = "QWERTYUIOPASDFGHJKLZXCVBNM";
    symbols_tir_3 = "0123456789";
    symbols_tir_4 = "!\"#$%&'\\()*+,-./:;<=>?@[]^_`{|}~";
    for (i of Array(password.length).keys()){
        if (symbols_tir_1.includes(password[i])){
            res["small_letter"] = true;
            break;
        }
    }
    for (let i = 0; i < password.length; i += 1){
        if (symbols_tir_2.includes(password[i])){
            res["big_letter"] = true;
            break;
        }
    }
    for (let i = 0; i < password.length; i += 1){
        if (symbols_tir_3.includes(password[i])){
            res["number"] = true;
            break;
        }
    }
    for (let i = 0; i < password.length; i += 1){
        if (symbols_tir_4.includes(password[i])){
            res["symbol"] = true;
            break;
        }
    }

    let hardness = "";
    if (res["length"] && res["small_letter"] && res["big_letter"] && res["number"] && res["symbol"]){
        hardness = "hard";
    }
    else if (res["length"] && res["small_letter"] && res["big_letter"] && (res["number"] || res["symbol"])){
        hardness = "medium";
    }
    else {
        hardness = "bad";
    }
    return [res, hardness];
}

const inputs = document.querySelectorAll("div#two div.input div.input input[type=text], div#two div.input div.input input[type=password]");
const emailInput = inputs[0];
const passInput = inputs[1];
const repeatInput = inputs[2];

const marks = document.querySelectorAll("div#two div.addition");
const emailMark = marks[0];
const passMark = marks[1];
const repeatMark = marks[2];

document.addEventListener("input", checkEmail);
function checkEmail(event) {
    if (event == "check" || event.target.closest("div#two input[name=username]")) {
        if (EmailCheck(emailInput.value)) {
            emailMark.children[0].children[1].children[0].style.fill = "#3ED252";
            emailMark.children[2].innerHTML = `<h5>e-mail is <span style="font-weight: 500;">valid</span></h5>`;
        }
        else {
            emailMark.children[0].children[1].children[0].style.fill = "#D23E3E";
            emailMark.children[2].innerHTML = `<h5>e-mail is <span style="font-weight: 500;">not valid</span></h5>`;
        }
    }
}

document.addEventListener("input", checkPassword);
function checkPassword(event) {
    if (event == "check" || event.target.closest("div#two input[name=password]")) {
        let check = PasswordChecker(passInput.value)
        
        let toWrite = "";
        if (!check[0]["length"])
            toWrite += `<h5>password is too <span style="font-weight: 500;">short</span></h5>`;
        if (!check[0]["small_letter"])
            toWrite += `<h5>no <span style="font-weight: 500;">small</span> letter</h5>`;
        if (!check[0]["big_letter"])
            toWrite += `<h5>no <span style="font-weight: 500;">big</span> letter</h5>`;
        if (!check[0]["number"])
            toWrite += `<h5>no <span style="font-weight: 500;">number</span> in password</h5>`;
        if (!check[0]["symbol"])
            toWrite += `<h5>no <span style="font-weight: 500;">special symbol</span> in password</h5>`;
        passMark.children[2].innerHTML = toWrite;
        
        if (check[1] == "hard") {
            passMark.children[0].children[1].children[0].style.fill = "#3ED252";
            passMark.children[2].innerHTML = `<h5>your password is <span style="font-weight: 500;">perfect</span></h5>`;
        }
        else if (check[1] == "medium") {
            passMark.children[0].children[1].children[0].style.fill = "#D2653E";
        }
        else {
            passMark.children[0].children[1].children[0].style.fill = "#D23E3E";
        }
    }
}

document.addEventListener("input", checkRepeat);
function checkRepeat(event) {
    if (event == "check" || event.target.closest("div#two input[name=repit_password]") || event.target.closest("div#two input[name=password]")) {
        if (passInput.value == repeatInput.value) {
            repeatMark.children[0].children[1].children[0].style.fill = "#3ED252";
            repeatMark.children[2].innerHTML = `<h5>passwords <span style="font-weight: 500;">match</span></h5>`;
        }
        else {
            repeatMark.children[0].children[1].children[0].style.fill = "#D23E3E";
            repeatMark.children[2].innerHTML = `<h5>passwords <span style="font-weight: 500;">do not match</span></h5>`;
        }
    }
}

checkEmail("check");
checkPassword("check");
checkRepeat("check");

const err = document.querySelector("div#two form > h4");
const submitButton = document.querySelector("div#two form > button[type=submit]");
const form = document.querySelector("div#two form");
form.addEventListener("submit", submitForm);
function submitForm(event) {
    event.preventDefault();
    if (passInput.value == repeatInput.value && PasswordChecker(passInput.value)[1] != "bad" && EmailCheck(emailInput.value)) {
        form.submit();
    }
    else {
        if (err != null) {
            err.innerHTML = "make sure all the fields are not red!";
        }
        else {
            submitButton.insertAdjacentHTML('beforebegin', '<h4 class="err">make sure all the fields are not red!</h4>');
        }
    }
}