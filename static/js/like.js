function f()
{
    let scripts = document.getElementsByTagName('script');
    let lastScript = scripts[scripts.length-1];
    let scriptName = lastScript;
    let post_ids = scriptName.getAttribute('post_ids').split(",");
    let user_login = scriptName.getAttribute('user_login');
    let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    document.addEventListener("click", switchLike);
    let likes = Array.from(document.querySelectorAll("div.block.post div.photo_block div.action div.like"));
    let checkboxes = Array.from(document.querySelectorAll("div.block.post div.photo_block div.action div.like input"));
    let url = `${ws_scheme}://${window.location.host}/ws/like/`;
    let websocket = new WebSocket(url);
    function switchLike(event) {
        if (event.target.closest("div.block.post div.photo_block div.action div.like")) {
            let likeId = likes.indexOf(event.target.closest("div.block.post div.photo_block div.action div.like"));
            likesNow = +likes[likeId].innerHTML.split("<h4>")[1].split("</h4>")[0];
            if (checkboxes[likeId].checked) {
                checkboxes[likeId].checked = false;
                likes[likeId].setAttribute("class", "like normal");
                likes[likeId].innerHTML = `<input type="checkbox">
                                           <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M18 1l-6 4-6-4-6 5v7l12 10 12-10v-7z"></path></svg>
                                           <h4>${likesNow - 1}</h4>`;
                u = window.location.href.split("/")
                websocket.send(JSON.stringify({
                    'type': 'unlike',
                    'user_login': user_login,
                    'post_id': post_ids[likeId]
                }));
            }
            else {
                checkboxes[likeId].checked = true;
                likes[likeId].setAttribute("class", "like");
                likes[likeId].innerHTML = `<input type="checkbox">
                                           <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M18 1l-6 4-6-4-6 5v7l12 10 12-10v-7z"></path></svg>
                                           <h4>${likesNow + 1}</h4>`;
                u = window.location.href.split("/")
                websocket.send(JSON.stringify({
                    'type': 'like',
                    'user_login': user_login,
                    'post_id': post_ids[likeId]
                }));
            }
        }
    }
}
f()