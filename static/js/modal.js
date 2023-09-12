document.getElementById("open-modal-btn").addEventListener("click", function() {
    document.getElementById("user-agreement-modal").classList.add("open")
})

document.getElementById("close-user-agreement-modal").addEventListener("click", function() {
    document.getElementById("user-agreement-modal").classList.remove("open")
})

window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
        document.getElementById("user-agreement-modal").classList.remove("open")
    }
});

document.querySelector("#user-agreement-modal .modal__box").addEventListener('click', event => {
    event._isClickWithModal = true;
});
document.getElementById("user-agreement-modal").addEventListener('click', event => {
    if (event._isClickWithModal) return;
    event.currentTarget.classList.remove("open");
});
