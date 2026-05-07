// Configurar la URL del backend (cambiar después de desplegar en Render)
// Cambia esta línea
const BACKEND_URL = 'https://busquedas-backend.onrender.com';

// Asegúrate que NO tenga barra al final

let ciudadesDisponibles = [];

// Cargar ciudades al iniciar
async function cargarCiudades() {
    try {
        console.log("Cargando ciudades...");
        const response = await fetch(`${BACKEND_URL}/api/ciudades`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("Ciudades recibidas:", data);
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        ciudadesDisponibles = data.ciudades;
        
        const origenSelect = document.getElementById('origen');
        const destinoSelect = document.getElementById('destino');
        
        origenSelect.innerHTML = '<option value="">Selecciona una ciudad</option>';
        destinoSelect.innerHTML = '<option value="">Selecciona una ciudad</option>';
        
        ciudadesDisponibles.forEach(ciudad => {
            const option1 = document.createElement('option');
            option1.value = ciudad;
            option1.textContent = ciudad;
            origenSelect.appendChild(option1);
            
            const option2 = document.createElement('option');
            option2.value = ciudad;
            option2.textContent = ciudad;
            destinoSelect.appendChild(option2);
        });
        
        console.log("Ciudades cargadas exitosamente");
        
    } catch (error) {
        console.error('Error cargando ciudades:', error);
        mostrarError(`Error al cargar las ciudades: ${error.message}`);
    }
}

// Función para comparar todos los algoritmos
async function compararAlgoritmos(origen, destino) {
    document.getElementById('loadingOverlay').style.display = 'flex';
    
    document.getElementById('bfsResults').style.display = 'none';
    document.getElementById('ucsResults').style.display = 'none';
    document.getElementById('dfsResults').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    
    try {
        console.log(`Comparando ruta de ${origen} a ${destino}`);
        
        const response = await fetch(`${BACKEND_URL}/api/comparar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                origen: origen,
                destino: destino
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("Respuesta del servidor:", data);
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        if (data.success) {
            if (data.resultados.bfs.success) {
                mostrarResultado('bfs', data.resultados.bfs.ruta, data.resultados.bfs.coste, data.resultados.bfs.mensaje);
            } else {
                mostrarErrorAlgoritmo('bfs', data.resultados.bfs.mensaje);
            }
            
            if (data.resultados.ucs.success) {
                mostrarResultado('ucs', data.resultados.ucs.ruta, data.resultados.ucs.coste, data.resultados.ucs.mensaje);
            } else {
                mostrarErrorAlgoritmo('ucs', data.resultados.ucs.mensaje);
            }
            
            if (data.resultados.dfs.success) {
                mostrarResultado('dfs', data.resultados.dfs.ruta, data.resultados.dfs.coste, data.resultados.dfs.mensaje);
            } else {
                mostrarErrorAlgoritmo('dfs', data.resultados.dfs.mensaje);
            }
            
        } else {
            mostrarError(data.mensaje || 'Error al comparar algoritmos');
        }
        
    } catch (error) {
        console.error('Error:', error);
        mostrarError(`Error de conexión: ${error.message}`);
    } finally {
        document.getElementById('loadingOverlay').style.display = 'none';
    }
}

function mostrarResultado(algoritmo, ruta, coste, mensaje) {
    const rutaPath = document.getElementById(`${algoritmo}Ruta`);
    const costeElement = document.getElementById(`${algoritmo}Coste`);
    const mensajeElement = document.getElementById(`${algoritmo}Mensaje`);
    const resultsSection = document.getElementById(`${algoritmo}Results`);
    
    rutaPath.innerHTML = '';
    ruta.forEach((ciudad, index) => {
        const ciudadSpan = document.createElement('span');
        ciudadSpan.className = 'ruta-step';
        ciudadSpan.textContent = ciudad;
        rutaPath.appendChild(ciudadSpan);
        
        if (index < ruta.length - 1) {
            const arrow = document.createElement('span');
            arrow.className = 'ruta-arrow';
            arrow.textContent = ' → ';
            rutaPath.appendChild(arrow);
        }
    });
    
    costeElement.textContent = coste;
    mensajeElement.textContent = mensaje;
    mensajeElement.style.background = '#E8F5F0';
    mensajeElement.style.borderLeft = '3px solid #A8E6CF';
    resultsSection.style.display = 'block';
}

function mostrarErrorAlgoritmo(algoritmo, mensaje) {
    const mensajeElement = document.getElementById(`${algoritmo}Mensaje`);
    const resultsSection = document.getElementById(`${algoritmo}Results`);
    
    mensajeElement.textContent = mensaje;
    mensajeElement.style.background = '#FEF5F5';
    mensajeElement.style.borderLeft = '3px solid #E8B4B8';
    resultsSection.style.display = 'block';
}

function mostrarError(mensaje) {
    const errorMensaje = document.getElementById('errorMensaje');
    errorMensaje.textContent = mensaje;
    document.getElementById('errorSection').style.display = 'block';
    
    document.getElementById('bfsResults').style.display = 'none';
    document.getElementById('ucsResults').style.display = 'none';
    document.getElementById('dfsResults').style.display = 'none';
    
    setTimeout(() => {
        document.getElementById('errorSection').style.display = 'none';
    }, 8000);
}

document.getElementById('origen').addEventListener('change', () => {
    const origen = document.getElementById('origen').value;
    const destino = document.getElementById('destino').value;
    
    if (origen && destino) {
        if (origen === destino) {
            mostrarError('El origen y destino no pueden ser la misma ciudad');
        } else {
            compararAlgoritmos(origen, destino);
        }
    }
});

document.getElementById('destino').addEventListener('change', () => {
    const origen = document.getElementById('origen').value;
    const destino = document.getElementById('destino').value;
    
    if (origen && destino) {
        if (origen === destino) {
            mostrarError('El origen y destino no pueden ser la misma ciudad');
        } else {
            compararAlgoritmos(origen, destino);
        }
    }
});

cargarCiudades();
