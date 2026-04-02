function validateBudget(){

let title = document.getElementById("title").value;
let category = document.getElementById("category").value;
let amount = document.getElementById("amount").value;
let month = document.getElementById("month").value;

let error = document.getElementById("error");

if(title === "" || category === "" || amount === "" || month === ""){

error.innerText = "Please fill all fields";

return false;
}

if(amount <= 0){

error.innerText = "Budget amount must be greater than 0";

return false;
}

return true;

}
window.onload = function(){
    let today = new Date()

    let year = today.getFullYear()
    let month = String(today.getMonth() + 1).padStart(2, '0')

    let currentMonth = year + "-" + month

    document.getElementById("month").setAttribute("min", currentMonth)
}
function confirmDelete(){
    return confirm("Are you sure you want to delete this ?");
}