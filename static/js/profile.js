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