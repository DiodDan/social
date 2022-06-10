var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
let script = document.getElementById('profile_script');
var user_id = script.getAttribute('user_id');
var user_login = script.getAttribute('user_login');

let my_url = window.location.href.split("/");
let login = my_url[my_url.length - 1];
let url = `${ws_scheme}://${window.location.host}/ws/profile/${user_login}/${login}`;
var websocket = new WebSocket(url);
function print(arg)
{
    console.log(arg);
}
try
{
    var button = document.getElementById('subscribe_button')
    button.addEventListener('click', function()
        {
            websocket.send(JSON.stringify({
                'type': 'subscribe',
                'url': window.location.href
            }));
        })
}catch(err)
{
    // console.log("Your's profile");
}

websocket.onmessage = function(e)
    {
        let data = JSON.parse(e.data);
        if(data.type == "follow")
        {
            let followers = document.getElementById('amount_of_followers');
            let button = document.getElementById('subscribe_button');
            followers.innerHTML = data.followers;
            button.innerHTML = data.follows ? "Отписаться" : "Подписаться";

        }
        if(data.type == "error")
        {
            let error_handler = document.getElementById('error_handler');
            error_handler.innerHTML = data.msg;
        }
    }

const imgs = Array.from(document.querySelectorAll("div.block.post div.photo_block div.photo img"));
for (img of imgs) {
    console.log(img.src);
    let splImg = img.src.split(".");
    let type = splImg[splImg.length - 1];
    if (type == "mp4") {
        img.outerHTML = `<video preload="auto" controls src="${img.src}"></video>`;
    }
}

document.addEventListener("click", openChangeProfile);
function openChangeProfile(event) {
    if (event.target.closest("button#change_data")) {
        document.querySelector("div.change_data").style.display = "block";
        document.querySelector("div.main").setAttribute("class", "main disabled");
    }
    else if (!event.target.closest("div.change_data") && document.querySelector("div.change_data").style.display == "block") {
        document.querySelector("div.change_data").style.display = "none";
        document.querySelector("div.main").setAttribute("class", "main");
    }
}

const followers = document.querySelector("div.followers div.number#followers");
const follows = document.querySelector("div.followers div.number#follows");

document.addEventListener("click", openFollowers);
function openFollowers(event) {
    if (event.target.closest("div.followers div.number#followers")) {
        document.querySelector("div.followers_menu").style.display = "flex";
        document.querySelector("div.main").setAttribute("class", "main disabled");
    }
    else if (!event.target.closest("div.followers div.number#followers") && document.querySelector("div.followers_menu").style.display == "flex") {
        document.querySelector("div.followers_menu").style.display = "none";
        document.querySelector("div.main").setAttribute("class", "main");
    }
}

document.addEventListener("click", openFollows);
function openFollows(event) {
    if (event.target.closest("div.followers div.number#follows")) {
        document.querySelector("div.follows_menu").style.display = "flex";
        document.querySelector("div.main").setAttribute("class", "main disabled");
    }
    else if (!event.target.closest("div.followers div.number#follows") && document.querySelector("div.follows_menu").style.display == "flex") {
        document.querySelector("div.follows_menu").style.display = "none";
        document.querySelector("div.main").setAttribute("class", "main");
    }
}

document.querySelector("div.change_data div.show_email div.toggle").addEventListener("click", changeToggle);
function changeToggle(event) {
    document.querySelector("div.change_data div.show_email input[type=checkbox]").checked = (document.querySelector("div.change_data div.show_email input[type=checkbox]").checked + 1) % 2;
}

function LoginCheck(login) {
    let res = {
        "length": false,
        "symbols": false
    };

    if (login.length <= 36 && login.length >= 4) {
        res["length"] = true;
    }

    let check = true;
    alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.@";

    for (symbol of login) {
        if (!alph.includes(symbol)) {
            check = false
        }
    }

    res["symbols"] = check;

    return res;
}

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
    if (password == "")
        hardness = "hard"
    return [res, hardness];
}

const inputs = document.querySelectorAll("div.change_data div.input input[name=login], div.change_data div.input input[name=password], div.change_data div.input input[name=profile_photo]");
const loginInput = inputs[0];
const passInput = inputs[1];
const photoInput = inputs[2];

const marks = document.querySelectorAll("div.change_data div.addition");
const loginMark = marks[0];
const passMark = marks[1];
const photoMark = marks[2];

document.addEventListener("input", checkLogin);
function checkLogin(event) {
    if (event == "check" || event.target.closest("div.change_data div.input input[name=login]")) {
        let ans = "";
        let res = LoginCheck(loginInput.value)
        if (!res["length"]) {
            ans += `<h5>login must contain <span style="font-weight: 500;">from 4 to 36</span> symbols</h5>`;
        }
        if (!res["symbols"]) {
            ans += `<h5>login must contain only <span style="font-weight: 500;">letters, numbers and special symbols: «_ - . @»</span></h5>`;
        }
        if (!ans) {
            loginMark.children[0].children[1].children[0].style.fill = "#3ED252";
            loginMark.children[2].innerHTML = "<h5>your login satisfies the requirements!</h5>";
        }
        else {
            loginMark.children[0].children[1].children[0].style.fill = "#D23E3E";
            loginMark.children[2].innerHTML = ans;
        }
    }
}

document.addEventListener("input", checkPassword);
function checkPassword(event) {
    if (event == "check" || event.target.closest("div.change_data div.input input[name=password]")) {
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

document.addEventListener("input", checkPhoto);
function checkPhoto(event) {
    if (event == "check" || event.target.closest("div.change_data div.input input[name=profile_photo]")) {
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

checkLogin("check");
checkPassword("check");
checkPhoto("check");

const err = document.querySelector("div.change_data form > h4");
const submitButton = document.querySelector("div.change_data form > button[type=submit]");
const form = document.querySelector("div.change_data form");
form.addEventListener("submit", submitForm);
function submitForm(event) {
    event.preventDefault();
    let loginRes = LoginCheck(loginInput.value);
    let name_format = photoInput.value.split(".");
    let format = name_format[name_format.length - 1];
    if (loginRes["length"] && loginRes["symbols"] && PasswordChecker(passInput.value)[1] != "bad" && ((format == "jpg" || format == "jpeg" || format == "png" || format == "gif") && (name_format.length > 1) || photoInput.value == "")) {
        form.submit();
    }
    else {
        if (err != null) {
            err.innerHTML = "make sure all the fields are not red!";
        }
        else {
            submitButton.insertAdjacentHTML('afterend', '<h4 class="err">make sure all the fields are not red!</h4>');
        }
    }
}