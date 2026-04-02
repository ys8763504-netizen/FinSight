function openEdit(){
    document.getElementById("popup").style.display="flex"
}
function closeEdit(){
    document.getElementById("popup").style.display="none"
}

// Validation
function validateForm(){
    let name = document.getElementById("name").value.trim()
    let email = document.getElementById("email").value.trim()
    let mobile = document.getElementById("mobile").value.trim()
    let error = document.getElementById("error")

    if(name==="" || email==="" || mobile===""){
        error.innerText="All fields required"
        return false
    }

    if(!email.includes("@")){
        error.innerText="Invalid email"
        return false
    }

    if(isNaN(mobile) || mobile.length<10){
        error.innerText="Invalid mobile"
        return false
    }

    return true
}
function openPassword(){
    document.getElementById("passwordPopup").style.display="flex"
}

function closePassword(){
    document.getElementById("passwordPopup").style.display="none"
}

// ✅ Validation
function validatePassword(){

    let oldPass = document.getElementById("old_password").value
    let newPass = document.getElementById("new_password").value
    let confirmPass = document.getElementById("confirm_password").value
    let error = document.getElementById("pass_error")

    if(oldPass === "" || newPass === "" || confirmPass === ""){
        error.innerText = "All fields required"
        return false
    }

    if(newPass.length < 6){
        error.innerText = "Password must be at least 6 characters"
        return false
    }

    if(newPass !== confirmPass){
        error.innerText = "Passwords do not match"
        return false
    }

    return true
}