const tooltip = document.getElementById("tooltip");

document.querySelectorAll(".info-btn").forEach(button => {
    button.addEventListener("click", () => {
        const infoText = button.getAttribute("data-info");

        tooltip.textContent = infoText;
        tooltip.classList.remove("hidden");

        const rect = button.getBoundingClientRect();
        tooltip.style.top = `${rect.bottom + window.scrollY + 8}px`;
        tooltip.style.left = `${rect.left + window.scrollX}px`;

        // Hide after 3 seconds
        setTimeout(() => {
            tooltip.classList.add("hidden");
        }, 3000);
    });
});
