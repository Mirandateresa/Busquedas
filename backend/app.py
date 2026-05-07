from flask import Flask, request, jsonify
from flask_cors import CORS
from .busquedas import Buscador
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Permitir cualquier origen
buscador = Buscador()

@app.route('/api/comparar', methods=['POST'])
def comparar_algoritmos():
    try:
        data = request.json
        origen = data.get('origen')
        destino = data.get('destino')
        
        if not origen or not destino:
            return jsonify({'error': 'Origen y destino son requeridos'}), 400
        
        # Convertir a mayúsculas
        origen = origen.upper()
        destino = destino.upper()
        
        resultados = {}
        
        # Ejecutar BFS
        try:
            nodo_bfs = buscador.buscar_bfs(origen, destino)
            if nodo_bfs:
                ruta_bfs, coste_bfs = buscador.obtener_ruta(nodo_bfs, origen, 'bfs')
                resultados['bfs'] = {
                    'success': True,
                    'ruta': ruta_bfs,
                    'coste': coste_bfs,
                    'mensaje': f'✅ BFS: {len(ruta_bfs)} ciudades, {coste_bfs} conexiones'
                }
            else:
                resultados['bfs'] = {
                    'success': False,
                    'mensaje': f'❌ BFS: No se encontró ruta'
                }
        except Exception as e:
            resultados['bfs'] = {'success': False, 'mensaje': f'❌ BFS: Error'}
        
        # Ejecutar UCS
        try:
            nodo_ucs = buscador.buscar_ucs(origen, destino)
            if nodo_ucs:
                ruta_ucs, coste_ucs = buscador.obtener_ruta(nodo_ucs, origen, 'ucs')
                resultados['ucs'] = {
                    'success': True,
                    'ruta': ruta_ucs,
                    'coste': coste_ucs,
                    'mensaje': f'💰 UCS: {len(ruta_ucs)} ciudades, Coste: {coste_ucs}'
                }
            else:
                resultados['ucs'] = {'success': False, 'mensaje': f'❌ UCS: No se encontró ruta'}
        except Exception as e:
            resultados['ucs'] = {'success': False, 'mensaje': f'❌ UCS: Error'}
        
        # Ejecutar DFS
        try:
            nodo_dfs = buscador.dfs_prof_iter(origen, destino)
            if nodo_dfs:
                ruta_dfs, coste_dfs = buscador.obtener_ruta(nodo_dfs, origen, 'dfs')
                resultados['dfs'] = {
                    'success': True,
                    'ruta': ruta_dfs,
                    'coste': coste_dfs,
                    'mensaje': f'🔍 DFS: {len(ruta_dfs)} ciudades, {coste_dfs} conexiones'
                }
            else:
                resultados['dfs'] = {'success': False, 'mensaje': f'❌ DFS: No se encontró ruta'}
        except Exception as e:
            resultados['dfs'] = {'success': False, 'mensaje': f'❌ DFS: Error'}
        
        return jsonify({
            'success': True,
            'origen': origen,
            'destino': destino,
            'resultados': resultados
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ciudades', methods=['GET'])
def obtener_ciudades():
    try:
        ciudades = list(buscador.conexiones_bfs.keys())
        return jsonify({'ciudades': sorted(ciudades)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)