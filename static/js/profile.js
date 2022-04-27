let scripts = document.getElementsByTagName('script');
let lastScript = scripts[scripts.length-1];
let scriptName = lastScript;
var user_id = scriptName.getAttribute('user_id');

let my_url = window.location.href.split("/");
login = my_url[my_url.length - 1];
let url = `ws://${window.location.host}/ws/profile/${user_id}/${login}`;
var websocket = new WebSocket(url);
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
    console.log("Your's profile");
}

websocket.onmessage = function(e)
    {
        let data = JSON.parse(e.data);
        let followers = document.getElementById('amount_of_followers');
        let button = document.getElementById('subscribe_button');
        followers.innerHTML = data.followers;
        followers.innerHTML = data.button_text;
    }