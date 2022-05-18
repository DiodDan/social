const usersHTML = document.querySelectorAll("div.block.search div.results a");
var users = [];
for (user of usersHTML) {
    var name = user.querySelector("div.info h3").innerHTML;
    var login = user.querySelector("div.info h4").innerHTML;
    users.push([name.toLowerCase(), login.toLowerCase()]);
}

const input = document.querySelector("input");
input.addEventListener("input", resultUsers);

function resultUsers(event) {
    newUserIds = [];
    text = input.value.toLowerCase();
    for (user of users) {
        if (user[0].includes(text) || user[1].includes(text)) {
            newUserIds.push(users.indexOf(user));
        }
    }

    newUsersHTML = [];
    for (var i = 0; i < usersHTML.length; i++) {
        if (newUserIds.includes(i)) {
            newUsersHTML.push(usersHTML[i].outerHTML);
        }
    }

    document.querySelector("div.block.search div.results").innerHTML = newUsersHTML.join("\n");
}
