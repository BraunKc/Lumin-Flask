const password = document.getElementById('password');

password.addEventListener('click', () => {
    let password = prompt('New password: ');
    if (password.length > 3) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/account', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ password: password }));
    } else {
        alert('Пароль слишком короткий')
    }
});
