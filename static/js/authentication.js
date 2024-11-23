const signInBtn = document.getElementById('signInBtn');
const signUpBtn = document.getElementById('signUpBtn');
const containers = document.querySelectorAll('.login-form, .register-form, .switch-container,\
                                            .sign-in-container, .sign-up-container');

signInBtn.addEventListener('click', () => {
    containers.forEach(container => {
        container.classList.remove('register');
        container.classList.add('login');
    });
});

signUpBtn.addEventListener('click', () => {
    containers.forEach(container => {
        container.classList.remove('login');
        container.classList.add('register');
    });
});