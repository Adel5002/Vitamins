document.addEventListener('DOMContentLoaded', function() {
    const descriptionBtn = document.getElementById('descr-btn');
    const specificationsBtn = document.getElementById('specifications-btn');
    const commentBtn = document.getElementById('comments-btn');
    const descriptionBlock = document.getElementById('descr-block');
    const specificationsBlock = document.getElementById('struc-block');
    const commentBlock = document.getElementById('comments-block');

    descriptionBtn.addEventListener('click', function() {
        descriptionBlock.style.display = 'block';
        specificationsBlock.style.display = 'none';
        commentBlock.style.display = 'none';
    });

    specificationsBtn.addEventListener('click', function() {
        descriptionBlock.style.display = 'none';
        specificationsBlock.style.display = 'block';
        commentBlock.style.display = 'none';
    });

    commentBtn.addEventListener('click', function() {
        descriptionBlock.style.display = 'none';
        specificationsBlock.style.display = 'none';
        commentBlock.style.display = 'block';
    });

});