function validateFilter(){

let month = document.getElementById("month").value
let category = document.getElementById("category").value
let error = document.getElementById("filter_error")

if(month === "" && category === ""){

error.innerText = "Please select at least one filter option"

return false
}

return true

}

//Report Download
function downloadTable(tableId, formatSelect){

let format = document.getElementById(formatSelect).value

if(format === ""){
alert("Please select download format")
return
}

let table = document.getElementById(tableId)

if(format === "csv"){
downloadCSV(table)
}

if(format === "excel"){
downloadExcel(table)
}

if(format === "pdf"){
exportPDF(tableId)

}

if(format === "png"){

exportPNG(tableId)
}

}

function downloadCSV(table){

let csv = []

let rows = table.querySelectorAll("tr")

rows.forEach(row => {

let cols = row.querySelectorAll("td,th")

let data = []

cols.forEach(col => data.push(col.innerText))

csv.push(data.join(","))

})

let csvFile = new Blob([csv.join("\n")], {type:"text/csv"})

let link = document.createElement("a")

link.href = URL.createObjectURL(csvFile)

link.download = "report.csv"

link.click()

}

function downloadExcel(table){

let wb = XLSX.utils.table_to_book(table)

XLSX.writeFile(wb,"report.xlsx")

}

function exportPDF(tableId){

let table = document.getElementById(tableId)

table.style.boxShadow = "none"
table.style.transform = "none"

html2canvas(table,{
scale:2,
backgroundColor:"#0f0f0f"
}).then(canvas=>{

const { jsPDF } = window.jspdf

let pdf = new jsPDF("p","mm","a4")

let img = canvas.toDataURL("image/png")

let width = 190
let height = canvas.height * width / canvas.width

pdf.addImage(img,"PNG",10,10,width,height)

pdf.save("report.pdf")

})

}

function exportPNG(tableId){

let table = document.getElementById(tableId)

/* remove problematic styles temporarily */

table.style.boxShadow = "none"
table.style.transform = "none"
table.style.overflow = "visible"

html2canvas(table,{
scale:2,
backgroundColor:"#0e0c0c"
}).then(canvas=>{

let link = document.createElement("a")

link.download = "report.png"
link.href = canvas.toDataURL()

link.click()

})

}