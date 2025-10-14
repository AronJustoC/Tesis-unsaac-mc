# Comandos para Ejecutar Ejemplos de Análisis Estructural

Este documento proporciona los comandos de terminal para ejecutar cada uno de los ejemplos de estructuras predefinidas con los diferentes flujos de trabajo de análisis disponibles en el proyecto.

## Antes de Empezar

Es crucial que actives el entorno virtual de Python antes de ejecutar cualquier comando. Utiliza el siguiente comando en tu terminal:

```bash
source venv/bin/activate
```

Si estás utilizando `fish` shell, el comando es:

```fish
source venv/bin/activate.fish
```

## Estructuras de Ejemplo Disponibles (Archivos de Datos)

Los siguientes archivos de datos se encuentran en `analisis_modal_3d/apps/data/`:

*   `bailey_bridge_data.py` (Puente Bailey original)
*   `bailey_data.py` (Puente Bailey)
*   `bailey_escalado_data.py` (Puente Bailey Escalado)
*   `bailey_escalado_pasadores_cp_data.py` (Puente Bailey Escalado con Pasadores - Copia)
*   `bailey_escalado_pernos_data.py` (Puente Bailey Escalado con Pernos)
*   `data_bailey_pasadores.py` (Puente Bailey con Pasadores)
*   `ejemplo_edificio_2d_data.py` (Edificio 2D)
*   `frequency_sweep_example_data.py` (Ejemplo de Barrido de Frecuencia)
*   `one_section_bailey_data.py` (Una Sección de Puente Bailey)
*   `simple_beam_data.py` (Viga Simple)
*   `vacio_data.py` (Pórtico 2D Simple)

## Flujos de Trabajo de Análisis Disponibles

Los flujos de trabajo de análisis se encuentran en `analisis_modal_3d/apps/analysis_workflows/`:

*   `static_analysis.py` (Análisis Estático)
*   `harmonic_analysis.py` (Análisis Armónico / Respuesta en Frecuencia)
*   `modal_analysis.py` (Análisis Modal)

## Comandos de Ejecución

Para ejecutar un análisis, utiliza el siguiente formato general:

```bash
python3 -u analisis_modal_3d/apps/analysis_workflows/<FLUJO_DE_TRABAJO>.py analisis_modal_3d/apps/data/<ARCHIVO_DE_DATOS>.py
```

A continuación, se listan los comandos específicos para cada combinación:

### 1. `bailey_bridge_data.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/bailey_bridge_data.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/bailey_bridge_data.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/bailey_bridge_data.py
    ```

### 2. `bailey_data.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/bailey_data.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/bailey_data.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/bailey_data.py
    ```

### 3. `bailey_escalado_data.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/bailey_escalado_data.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/bailey_escalado_data.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/bailey_escalado_data.py
    ```

### 4. `bailey_escalado_pasadores_cp_data.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/bailey_escalado_pasadores_cp_data.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/bailey_escalado_pasadores_cp_data.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/bailey_escalado_pasadores_cp_data.py
    ```

### 5. `bailey_escalado_pernos_data.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/bailey_escalado_pernos_data.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/bailey_escalado_pernos_data.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/bailey_escalado_pernos_data.py
    ```

### 6. `data_bailey_pasadores.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/data_bailey_pasadores.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/data_bailey_pasadores.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/data_bailey_pasadores.py
    ```

### 7. `ejemplo_edificio_2d_data.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/ejemplo_edificio_2d_data.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/ejemplo_edificio_2d_data.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/ejemplo_edificio_2d_data.py
    ```

### 8. `frequency_sweep_example_data.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/frequency_sweep_example_data.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/frequency_sweep_example_data.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/frequency_sweep_example_data.py
    ```

### 9. `one_section_bailey_data.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/one_section_bailey_data.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/one_section_bailey_data.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/one_section_bailey_data.py
    ```

### 10. `simple_beam_data.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/simple_beam_data.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/simple_beam_data.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/simple_beam_data.py
    ```

### 11. `vacio_data.py`

*   **Análisis Estático:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/static_analysis.py analisis_modal_3d/apps/data/vacio_data.py
    ```
*   **Análisis Armónico:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/harmonic_analysis.py analisis_modal_3d/apps/data/vacio_data.py
    ```
*   **Análisis Modal:**
    ```bash
    python3 -u analisis_modal_3d/apps/analysis_workflows/modal_analysis.py analisis_modal_3d/apps/data/vacio_data.py
    ```

Espero que esta guía detallada te sea de gran utilidad para explorar los diferentes análisis.