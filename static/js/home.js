const togger = document.querySelector('.toggler-btn');
togger.addEventListener('click', () => {
    document.querySelector('#sidebar').classList.toggle('collapsed');
})