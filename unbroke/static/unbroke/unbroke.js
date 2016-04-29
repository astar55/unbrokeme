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

function showDateOL(){
    document.getElementById("dateol").style.width = "100%"
}

function hideDateOL(){
    document.getElementById("dateol").style.width = "0%"
}

function showDescOL(){
    document.getElementById("descol").style.width = "100%"
}

function hideDescOL(){
    document.getElementById("descol").style.width = "0%"    
}

function showAmtOL(){
    document.getElementById("amtol").style.width = "100%"    
}

function hideAmtOL(){
    document.getElementById("amtol").style.width = "0%"    
}

function showAccOL(){
    document.getElementById("accol").style.width = "100%"    
}

function hideAccOL(){
    document.getElementById("accol").style.width = "0%"    
}

function hideeditOL(){
    document.getElementById("editol").style.width = "0%"
}

function showaddOL(){
    document.getElementById("addol").style.width = "100%"    
}

function hideaddOL(){
    document.getElementById("addol").style.width = "0%"    
}

function recclick(){
    if (document.getElementById('recurring').checked == true) {
        var x = document.getElementsByClassName('hidden')
        x[0].style.visibility = "visible"
        x[1].style.visibility = "visible"
        document.getElementById('recurring').value = "True"
    }
    else{
        var x = document.getElementsByClassName('hidden')
        x[0].style.visibility = "hidden"
        x[1].style.visibility = "hidden"
        document.getElementById('recurring').value = "False"
    }
}

function erecclick(){
    if (document.getElementById('erecurring').checked == true) {
        document.getElementsByClassName('hidden').style.visibility = "visible"
        document.getElementsById('erecurring').value = "True"
    }
    else{
        document.getElementsByClassName('hidden').style.visibility = "hidden"
        document.getElementById('erecurring').value = "False"
    }
}

function showadddesc (){
    document.getElementById("adddescol").style.width = "100%"    
}

function hideadddesc(){
    document.getElementById("adddescol").style.width = "0%"    
}

function showaddacc (){
    document.getElementById("addaccol").style.width = "100%"    
}

function hideaddacc(){
    document.getElementById("addaccol").style.width = "0%"    
}

function adddesc(){
    var x = document.getElementById("additionaldesc").value;
    var y = document.getElementById("ddesc")
    var z = document.createElement("option")
    z.text = x
    z.value = x
    y.add(z)
    hideadddesc()
}

function addacc(){
    var x = document.getElementById("additionalacc").value;
    var y = document.getElementById("dacc")
    var z = document.createElement("option")
    z.text = x
    z.value = x
    y.add(z)
    hideaddacc()
}

function showeadddesc (){
    document.getElementById("eadddescol").style.width = "100%"    
}

function hideeadddesc(){
    document.getElementById("eadddescol").style.width = "0%"    
}

function showeaddacc (){
    document.getElementById("eaddaccol").style.width = "100%"    
}

function hideeaddacc(){
    document.getElementById("eaddaccol").style.width = "0%"    
}

function eadddesc(){
    var x = document.getElementById("eadditionaldesc").value;
    var y = document.getElementById("eddesc")
    var z = document.createElement("option")
    z.text = x
    z.value = x
    y.add(z)
}

function eaddacc(){
    var x = document.getElementById("eadditionalacc").value;
    var y = document.getElementById("edacc")
    var z = document.createElement("option")
    z.text = x
    z.value = x
    y.add(z)
}
