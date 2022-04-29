var chats = []
var user_id = ''
var user_login = ''
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
function print(arg)
{
    console.log(arg);
}
function load_data()
{
    let scripts = document.getElementsByTagName('script');
    let lastScript = scripts[scripts.length-1];
    let scriptName = lastScript;
    chats = scriptName.getAttribute('chats').split(",");
    user_id = scriptName.getAttribute('user_id');
    user_login = scriptName.getAttribute('user_login');
    chats.pop();
}
var arr = [];
var idBtn = -1
var unreadmessages = []
var sliders = Array.from(document.querySelectorAll("div.dialog"));

function connect_to_socket()
{
    let url = `${ws_scheme}://${window.location.host}/ws/messenger/${user_login}`;
    let urls = []
    for (i of arr)
    {
        urls.push(i.url)
    }
    for(i of Array(chats.length).keys())
    {
        url = `${ws_scheme}://${window.location.host}/ws/messenger/${user_login}/${chats[i].split("'")[1]}`;
        if (!(urls.includes(url)))
        {
           arr.push(new WebSocket(url));
        }
        arr[i].onmessage = function(e)
        {
            let data = JSON.parse(e.data);
            var id = chats.indexOf("'" + String(data.chat) + "'");
            if(data.type === 'message')
            {
                let messages = document.getElementById(`messeges_${id}`);
                let last_message = document.getElementById(`last_message_of_chatid_${id}`);
                let chat_time = document.getElementById(`last_message_of_chatidu_${id}`);
                my_class = user_login == data.login ? "message sent" : "message received";
                messages.insertAdjacentHTML('beforeend', `
                <div class="${my_class}">
                    <a href="/profile/${data.login}">${data.chat_users[data.user_id]}</a>
                    <h4>${data.message}</h4>
                    <h5 class="transparent">${data.time_sent}</h5>
                </div>`);
                last_message.innerHTML = `<h5>${data.message}</h5><h5 class="transparent">${data.time_sent}</h5>`;
                chat_time.innerHTML = `${data.time_sent}`
                let unread_messages_html = document.getElementById(`unread_messages_${id}`);
                let unread_messages = data.unread_messages;
                let ans = 0;
                ans = unread_messages[user_id];
                unread_messages_html.innerHTML = ans;
                if(!(idBtn == -1))
                {
                    unread_messages_html = document.getElementById(`unread_messages_${idBtn}`);
                    unread_messages_html.innerHTML = "";
                    sliders[idBtn].scrollTop = sliders[idBtn].scrollHeight;
                    arr[idBtn].send(JSON.stringify({
                        'type': 'messages_read',
                        'login': user_login
                        }))
                }
            }
        }
        var form = document.getElementById(`form_${i}`)
        let s = function(e)
        {
            form = document.getElementById(`form_${idBtn}`)
            e.preventDefault();
            let message = e.target.message.value;
            let u = window.location.href;
            arr[idBtn].send(JSON.stringify({
                'type': 'message',
                'message':message,
                'login': user_login
            }))
            form.reset();
        }
        form.addEventListener('submit', s);
    }
}



load_data();
connect_to_socket();
var radios = Array.from(document.querySelectorAll("input[type=radio][name=chat]"));
var btns = Array.from(document.querySelectorAll("button.chat"));
document.addEventListener("click", changeRadio);
function changeRadio(event)
{
    if (event.target.closest("button.chat"))
    {
        for (radio of radios)
        {
            radio.checked = false;
        }
        idBtn = btns.indexOf(event.target.closest("button.chat"));
        radios[idBtn].checked = true;
        arr[idBtn].send(JSON.stringify({
        'type': 'messages_read',
        'login': user_login
        }))
        let unread_messages = document.getElementById(`unread_messages_${idBtn}`)
        unread_messages.innerHTML = ""


        sliders[idBtn].scrollTop = sliders[idBtn].scrollHeight;
    }
}