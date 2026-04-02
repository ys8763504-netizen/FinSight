const toggle = document.getElementById("menu-toggle");
const navLinks = document.getElementById("navLinks");

toggle.addEventListener("click", () => {
    navLinks.classList.toggle("active");
});
document.querySelectorAll("#navLinks a").forEach(link => {
    link.addEventListener("click", () => {
        navLinks.classList.remove("active");
    });
});