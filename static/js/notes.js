const createBtn = document.getElementById('createBtn');

createBtn.addEventListener('click', () => {
    let title = prompt('Name of note: ')
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/notes/create', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ title: title, content: '' }));
    setTimeout(() => {
        location.reload()
    }, 100)
})
