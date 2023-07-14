let cards = document.querySelectorAll('.cart-btn');


cards.forEach((card)=>{
  card.addEventListener('mouseover', function(){
    card.classList.add('is-hover');
  })
  card.addEventListener('mouseleave', function(){
    card.classList.remove('is-hover');
  })
})


const icon = document.querySelector('.icon');
const search = document.querySelector('.search');
const clear = document.querySelector('.clear');

icon.onclick = function() {
    search.classList.toggle('active');
};

clear.onclick = function() {
    document.getElementById('mySearch').value = ''
};