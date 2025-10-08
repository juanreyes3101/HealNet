// toggle-password.js - Mostrar/Ocultar contraseñas
document.addEventListener('DOMContentLoaded', function() {
  const showButtons = document.querySelectorAll('.show-btn');
  
  showButtons.forEach(button => {
    button.addEventListener('click', function() {
      const targetId = this.getAttribute('data-target');
      const passwordInput = document.getElementById(targetId);
      
      if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        this.textContent = 'HIDE';
      } else {
        passwordInput.type = 'password';
        this.textContent = 'SHOW';
      }
    });
  });
});