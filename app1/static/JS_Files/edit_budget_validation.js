function validateForm(){

let title = document.getElementById("title").value;
let amount = document.getElementById("amount").value;
let category = document.getElementById("category").value;
let date = document.getElementById("date").value;

let error = document.getElementById("error");

if(title === "" || amount === "" || category === "" || date === ""){
    
    error.innerText = "Please fill all fields";

    return false;
}

if(amount <= 0){

    error.innerText = "Amount must be greater than 0";

    return false;
}

return true;

}
