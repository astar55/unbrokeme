function validate() {
    let namepat = '[a-zA-Z]';
    if (event.target.id == "fname"){
        let x = document.getElementById("fname");
        if (!x.value.match(namepat)){
            document.getElementById("ferror").innerHTML = "Invalid First Name";
        }
        else{
            document.getElementById("ferror").innerHTML = "";
        }
    }
    else if (event.target.id == "lname"){
        let x = document.getElementById("lname");
        if (!x.value.match(namepat)){
            document.getElementById("ferror").innerHTML = "Invalid Last Name";
        }
        else{
            document.getElementById("ferror").innerHTML = "";
        }
    }
    else if (event.target.id == "uname"){
        let x = document.getElementById("uname");
        if (!x.value.includes("@")){
            document.getElementById("ferror").innerHTML = "Invalid E-mail";
        }
        else{
            document.getElementById("ferror").innerHTML = "";
        }
        }
    else if (event.target.id == "user"){
        let x = document.getElementById("user");
        if (!x.value.includes("@")){
            document.getElementById("ferror").innerHTML = "Invalid Username";
        }
        else{
            document.getElementById("ferror").innerHTML = "";
        }
        }
    else if (event.target.id == "pword"){
        let x = document.getElementById("pword");
        if (x.value.length == 0 || x.value == ""){
            document.getElementById("ferror").innerHTML = "Invalid Password";
        }
        else{
            document.getElementById("ferror").innerHTML = "";
        }
        }
    }

function poverlay(){
    document.getElementById("pc").style.width = "100%"
}

function cpoverlay(){
    document.getElementById("pc").style.width = "0%"
}

function cpvalid(){
    let x = document.getElementById("cnpass").value
    let y = document.getElementById("npass").value
    if (x == y && x.length > 0 && y.length > 0){
        return true
    }
    document.getElementById("ferror").innerHTML = "Passwords Do Not Match!"
    return false
}

