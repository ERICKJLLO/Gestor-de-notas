// Variables globales para usuario y contraseña (simulación de sesión simple)
let usuario = localStorage.getItem("usuario") || "";
let contrasena = localStorage.getItem("contrasena") || "";

// Redirección automática si ya está logueado
if (window.location.pathname.endsWith("index.html") && usuario && contrasena) {
    window.location.href = "notas.html";
}

// -------------------- LOGIN Y REGISTRO --------------------
function login() {
    const user = document.getElementById("login-usuario").value;
    const pass = document.getElementById("login-contrasena").value;
    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario: user, contrasena: pass })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            mostrarMensaje(data.error);
        } else {
            localStorage.setItem("usuario", user);
            localStorage.setItem("contrasena", pass);
            window.location.href = "notas.html";
        }
    });
}

function register() {
    const user = document.getElementById("register-usuario").value;
    const pass = document.getElementById("register-contrasena").value;
    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario: user, contrasena: pass })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            mostrarMensaje(data.error);
        } else {
            mostrarMensaje("Usuario registrado correctamente. Ahora puedes iniciar sesión.");
        }
    });
}

function mostrarMensaje(msg) {
    document.getElementById("mensaje").innerText = msg;
}

// -------------------- NOTAS --------------------
if (window.location.pathname.endsWith("notas.html")) {
    if (!usuario || !contrasena) {
        window.location.href = "index.html";
    }
    cargarNotas();
}

function cargarNotas() {
    fetch("/notas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, contrasena })
    })
    .then(r => r.json())
    .then(data => {
        const lista = document.getElementById("notas-lista");
        lista.innerHTML = "";
        if (data.error) {
            mostrarMensaje(data.error);
            return;
        }
        if (Array.isArray(data.notas)) {
            data.notas.forEach((nota, i) => {
                const div = document.createElement("div");
                div.className = "nota";
                div.innerHTML = `
                    <div>${nota.replace(/\n/g, "<br>")}</div>
                    <div class="acciones">
                        <button onclick="editarNota(${i})">Editar</button>
                        <button onclick="eliminarNota(${i})">Eliminar</button>
                    </div>
                `;
                lista.appendChild(div);
            });
        } else {
            lista.innerText = data.notas || "No hay notas.";
        }
    });
}

function mostrarFormularioNota(indice = null) {
    document.getElementById("form-nota").style.display = "block";
    document.getElementById("form-nota-titulo").innerText = indice === null ? "Crear Nota" : "Editar Nota";
    document.getElementById("nota-titulo").value = "";
    document.getElementById("nota-contenido").value = "";
    document.getElementById("nota-categoria").value = "";
    document.getElementById("nota-enlaces").value = "";
    document.getElementById("form-nota").dataset.indice = indice !== null ? indice : "";
}

function cancelarNota() {
    document.getElementById("form-nota").style.display = "none";
}

function guardarNota() {
    const titulo = document.getElementById("nota-titulo").value;
    const contenido = document.getElementById("nota-contenido").value;
    const categoria = document.getElementById("nota-categoria").value;
    const enlaces = document.getElementById("nota-enlaces").value.split(",").map(e => e.trim()).filter(e => e);
    const indice = document.getElementById("form-nota").dataset.indice;

    if (indice === "") {
        // Crear nota
        fetch("/nota", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario, contrasena, titulo, contenido, categoria, enlaces })
        })
        .then(r => r.json())
        .then(data => {
            if (data.error) mostrarMensaje(data.error);
            else {
                cancelarNota();
                cargarNotas();
            }
        });
    } else {
        // Editar nota
        fetch(`/nota/${indice}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario, contrasena, titulo, contenido, categoria })
        })
        .then(r => r.json())
        .then(data => {
            if (data.error) mostrarMensaje(data.error);
            else {
                cancelarNota();
                cargarNotas();
            }
        });
    }
}

function editarNota(indice) {
    // Obtener datos de la nota actual para editar (requiere recargar las notas)
    fetch("/notas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, contrasena })
    })
    .then(r => r.json())
    .then(data => {
        if (Array.isArray(data.notas) && data.notas[indice]) {
            // Extraer campos de la nota (asumiendo formato de string)
            const nota = data.notas[indice];
            const titulo = extraerCampo(nota, "Título");
            const contenido = extraerCampo(nota, "Contenido");
            const categoria = extraerCampo(nota, "Categoría");
            const enlaces = extraerCampo(nota, "Enlaces");
            mostrarFormularioNota(indice);
            document.getElementById("nota-titulo").value = titulo;
            document.getElementById("nota-contenido").value = contenido;
            document.getElementById("nota-categoria").value = categoria;
            document.getElementById("nota-enlaces").value = enlaces;
        }
    });
}

function extraerCampo(texto, campo) {
    // Extrae el valor de un campo de la nota (formato: "Campo: valor")
    const regex = new RegExp(`${campo}: ([^\\n]*)`);
    const match = texto.match(regex);
    return match ? match[1].trim() : "";
}

function eliminarNota(indice) {
    if (!confirm("¿Seguro que deseas eliminar esta nota?")) return;
    fetch(`/nota/${indice}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, contrasena })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) mostrarMensaje(data.error);
        else cargarNotas();
    });
}

// -------------------- CAMBIO DE CONTRASEÑA --------------------
function mostrarFormularioPassword() {
    document.getElementById("form-password").style.display = "block";
}
function cancelarPassword() {
    document.getElementById("form-password").style.display = "none";
}
function cambiarPassword() {
    const nueva_contrasena = document.getElementById("nueva-contrasena").value;
    fetch("/usuario/password", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, contrasena, nueva_contrasena })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) mostrarMensaje(data.error);
        else {
            mostrarMensaje("Contraseña cambiada correctamente.");
            localStorage.setItem("contrasena", nueva_contrasena);
            contrasena = nueva_contrasena;
            cancelarPassword();
        }
    });
}

// -------------------- ELIMINAR USUARIO --------------------
function eliminarUsuario() {
    if (!confirm("¿Seguro que deseas eliminar tu usuario y todas tus notas?")) return;
    fetch("/usuario", {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, contrasena })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) mostrarMensaje(data.error);
        else {
            localStorage.removeItem("usuario");
            localStorage.removeItem("contrasena");
            window.location.href = "index.html";
        }
    });
}

// -------------------- LOGOUT --------------------
function logout() {
    localStorage.removeItem("usuario");
    localStorage.removeItem("contrasena");
    window.location.href = "index.html";
}
