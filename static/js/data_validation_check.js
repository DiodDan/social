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