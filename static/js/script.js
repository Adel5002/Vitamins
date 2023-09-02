let cards = document.querySelectorAll('.cart-btn');

$(document).on('mouseover', '.cart-btn', function() {
    this.classList.add('is-hover');
});

$(document).on('mouseleave', '.cart-btn', function() {
    this.classList.remove('is-hover');
});


const icon = document.querySelector('.icon');
const search = document.querySelector('.search');
const clear = document.querySelector('.clear');

icon.onclick = function() {
    search.classList.toggle('active');
};

clear.onclick = function() {
    document.getElementById('mySearch').value = ''
};