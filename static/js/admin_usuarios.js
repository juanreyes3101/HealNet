// CAMBIAR PESTAÑAS
function switchTab(tabName) {
    // Ocultar todos los contenidos
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Desactivar todos los botones
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Activar la pestaña seleccionada
    document.getElementById('tab-' + tabName).classList.add('active');
    event.target.classList.add('active');
}
// MOSTRAR/OCULTAR CAMPOS DE DOCTOR
function toggleDoctorFields() {
    const rol = document.getElementById('rolSelect').value;
    const doctorFields = document.getElementById('doctorFields');
    
    if (rol === 'doctor') {
        doctorFields.classList.add('active');
    } else {
        doctorFields.classList.remove('active');
    }
}
function toggleEditDoctorFields() {
    const rol = document.getElementById('edit_rol').value;
    const doctorFields = document.getElementById('editDoctorFields');
    
    if (rol === 'doctor') {
        doctorFields.classList.add('active');
    } else {
        doctorFields.classList.remove('active');
    }
}
// FILTRAR TABLA
function filterTable() {
    const searchText = document.getElementById('searchInput').value.toLowerCase();
    const roleFilter = document.getElementById('roleFilter').value;
    const rows = document.querySelectorAll('#usersTable tbody tr');
    
    rows.forEach(row => {
        const name = row.cells[0].textContent.toLowerCase();
        const email = row.cells[1].textContent.toLowerCase();
        const role = row.getAttribute('data-role');
        
        const matchesSearch = name.includes(searchText) || email.includes(searchText);
        const matchesRole = roleFilter === 'todos' || role === roleFilter;
        
        if (matchesSearch && matchesRole) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}
// EDITAR USUARIO
function editarUsuario(id, nombre, correo, rol, numero, especialidad, licencia, activo) {
    document.getElementById('edit_user_id').value = id;
    document.getElementById('edit_nombre').value = nombre;
    document.getElementById('edit_correo').value = correo;
    document.getElementById('edit_rol').value = rol;
    document.getElementById('edit_numero').value = numero;
    document.getElementById('edit_especialidad').value = especialidad;
    document.getElementById('edit_licencia').value = licencia;
    document.getElementById('edit_activo').checked = activo;
    
    document.getElementById('editForm').action = `/admin/usuario/${id}/editar`;
    
    toggleEditDoctorFields();
    document.getElementById('editModal').classList.add('active');
}
function cerrarModal() {
    document.getElementById('editModal').classList.remove('active');
}
// ELIMINAR USUARIO
function confirmarEliminar(id, nombre) {
    document.getElementById('deleteUserName').textContent = nombre;
    document.getElementById('deleteForm').action = `/admin/usuario/${id}/eliminar`;
    document.getElementById('deleteModal').classList.add('active');
}
function cerrarModalDelete() {
    document.getElementById('deleteModal').classList.remove('active');
}
// Cerrar modales al hacer clic fuera
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
}