window.onload = function(){
    const parentSelect = document.querySelector('#id_parent');
    const pages = document.querySelector('.field-pages');

    if (parentSelect.value !== '') {
        pages.style.display = 'none';
    };

    parentSelect.onchange = function(elem){
        if(elem.target.value === '') {
            pages.style.display = 'block';
        }
        else {
            pages.style.display = 'none';
        }
    }
}
