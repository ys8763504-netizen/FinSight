function searchExpense() {

    let input = document.getElementById("search").value.toLowerCase();

    let table = document.querySelector("table");

    let rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {

        let title = rows[i].getElementsByTagName("td")[0];
        let category = rows[i].getElementsByTagName("td")[2];

        if (title || category) {

            let titleText = title.textContent.toLowerCase();
            let categoryText = category.textContent.toLowerCase();

            if (titleText.includes(input) || categoryText.includes(input)) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}
function checkBudget(){

    let category = document.getElementById("category").value
    let amount = document.getElementById("amount").value
    let date = document.getElementById("date").value
    let box = document.getElementById("budgetStatus")

    if(category === "" || amount === "" || date === ""){
        box.innerHTML = ""
        return
    }

    // Convert date → YYYY-MM
    let monthYear = date.substring(0,7)

    // 🔥 Call Django API
    fetch(`/check_budget?category=${category}&month=${monthYear}`)
    .then(res => res.json())
    .then(data => {

        if(!data.budget){
            box.className = "budget-box budget-warning"
            box.innerHTML = "⚠ No budget set for this category/month"
            return
        }

        let remaining = data.remaining - amount

        if(remaining >= 0){
            box.className = "budget-box budget-ok"
            box.innerHTML = `✅ Remaining Budget: ₹${remaining}`
        }else{
            box.className = "budget-box budget-danger"
            box.innerHTML = `🚨 Budget Exceeded by ₹${Math.abs(remaining)}`
        }

    })

}
setTimeout(()=>{
    let popup = document.getElementById("popup")
    if(popup){
        popup.style.display="none"
    }
},3000)
window.onload = function() {
    let today = new Date().toISOString().split("T")[0]
    document.getElementById("date").setAttribute("min", today)
}
function confirmDelete(){
    return confirm("Are you sure you want to delete this ?");
}