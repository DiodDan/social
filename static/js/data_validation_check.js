function EmailCheck(email){
    let re = /^[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,}$/i;
    return (re.test(email));
};

function PasswordChecker(password){
    let res = [1, 0, 0, 0, 0];

    /*
    0 - длина >= 8
    1 - есть маленькая буква
    2 - есть большая буква
    3 - есть цифра
    4 - есть символ
    */

    if (password.length < 8) {
        res[0] = 0;
    }
    symbols_tir_1 = "qwertyuiopasdfghjklzxcvbnm";
    symbols_tir_2 = "QWERTYUIOPASDFGHJKLZXCVBNM";
    symbols_tir_3 = "0123456789";
    symbols_tir_4 = " !\"#$%&'\\()*+,-./:;<=>?@[]^_`{|}~";
    for (i of Array(password.length).keys()){
        if (symbols_tir_1.includes(password[i])){
            res[1] = 1;
            break;
        }
    }
    for (let i = 0; i < password.length; i += 1){
        if (symbols_tir_2.includes(password[i])){
            res[2] = 1;
            break;
        }
    }
    for (let i = 0; i < password.length; i += 1){
        if (symbols_tir_3.includes(password[i])){
            res[3] = 1;
            break;
        }
    }
    for (let i = 0; i < password.length; i += 1){
        if (symbols_tir_4.includes(password[i])){
            res[4] = 1;
            break;
        }
    }

    /*

    */
    let hardness = "";
    if (res[2] == 1 && res[1] == 1 && res[3] == 1 && res[0] == 1 && res[4] == 1){
        hardness = "hard";
    }
    else if (res[2] == 1 && res[1] == 1 && (res[3] == 1 || res[4] == 1) && res[0] == 1){
        hardness = "medium";
    }
    else{
        hardness = "bad";
    }
    return [res, hardness];
}
console.log(EmailCheck("danilaprig@gmail.com"))
console.log(PasswordChecker("xfdvxD1v@"))