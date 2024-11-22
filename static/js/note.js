const title = document.getElementById('title');
const content = document.getElementById('content');

var timeout = null
document.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.which === 83) {
        event.preventDefault();
        
        if (!timeout) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', `/notes/${noteId}`, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ title: title.value, content: content.value }));

            timeout = setTimeout(() => {
                timeout = null;
            }, 1000)
        }
    }
});
