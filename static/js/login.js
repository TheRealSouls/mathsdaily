const passwordInput = document.getElementById("password");
const toggleButton = document.querySelector(".password-toggle");

toggleButton.addEventListener('click', (e) => {
    e.preventDefault();
    
    const isPassword = passwordInput.type === 'password';
    if (isPassword) {
        passwordInput.type = 'text';
        toggleButton.innerHTML = '<i class="fa fa-eye-slash"></i>';
    } else {
        passwordInput.type = 'password';
        toggleButton.innerHTML = '<i class="fa fa-eye"></i>';
    }
})