const btnMenu = document.getElementById('btn-menu');

function mudarMenu() {
    const nav = document.getElementById('nav');
    nav.classList.toggle('active')
}

btnMenu.addEventListener('click', mudarMenu);