// toggle-password.js
document.addEventListener('click', function(e){
  if (e.target && e.target.classList.contains('show-btn')) {
    const targetId = e.target.getAttribute('data-target');
    const input = document.getElementById(targetId);
    if (!input) return;
    if (input.type === 'password') {
      input.type = 'text';
      e.target.textContent = 'HIDE';
    } else {
      input.type = 'password';
      e.target.textContent = 'SHOW';
    }
  }
});
