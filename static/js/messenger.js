var chats = []
function load_data()
{
    let scripts = document.getElementsByTagName('script');
    let lastScript = scripts[scripts.length-1];
    let scriptName = lastScript;
    chats = scriptName.getAttribute('chats').split(",");
    chats.pop();
}
var arr = [];
var idBtn = 0
var unreadmessages = []

function connect_to_socket()
{
    let my_url = window.location.href.split("/");
    login = my_url[my_url.length - 1];
    let url = `ws://${window.location.host}/ws/socket-server/${login}`;
    let urls = []
    for (i of arr)
    {
        urls.push(i.url)
    }
    for(i of Array(chats.length).keys())
    {
        url = `ws://${window.location.host}/ws/socket-server/${login}/${chats[i].split("'")[1]}`;
        if (!(urls.includes(url)))
        {
           arr.push(new WebSocket(url));
        }
        arr[i].onmessage = function(e)
        {
            let data = JSON.parse(e.data);
            let id = data.chat
            if(data.type === 'message')
            {
                let messages = document.getElementById(`messeges_${id}`);
                let last_message = document.getElementById(`last_message_of_chatid_${id}`);
                let chat_time = document.getElementById(`last_message_of_chatidu_${id}`);
                let my_class = window.location.href.split("/");
                my_class = my_class[my_class.length - 1] == data.login ? "message sent" : "message received";
                messages.insertAdjacentHTML('beforeend', `
                <div class="${my_class}">
                    <a href="/profile/${data.login}">${data.chat_users[data.user_id]}</a>
                    <h4>${data.message}</h4>
                    <h5 class="transparent">${data.time_sent}</h5>
                </div>`);
                last_message.innerHTML = `<h5>${data.message}</h5><h5 class="transparent">${data.time_sent}</h5>`;
                chat_time.innerHTML = `${data.time_sent}`
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
                'url': u
            }))
            form.reset();
        }
        form.addEventListener('submit', s)
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
                'url': window.location.href
            }))
            }
        }