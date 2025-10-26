# Guía de Refactorización: De Script a Aplicación Web 3D con Trame y PyVista

Este documento es una guía paso a paso en formato de checklist para transformar el proyecto de análisis modal en una aplicación web interactiva de alto rendimiento usando el framework Trame.

**Tecnologías a usar:**
- **Lógica Principal:** Python
- **Framework Web/UI:** Trame
- **Componentes de UI:** Vuetify (incluido en Trame)
- **Visualización 3D:** PyVista y VTK (integrados con Trame)

---

## Fase 1: Preparación y Entorno

- `[ ]` **Instalar Dependencias:** Abre tu terminal, activa el entorno virtual y ejecuta:
  ```bash
  pip install trame trame-vuetify trame-vtk pyvista
  ```

- `[ ]` **Crear Rama en Git:** Para mantener un historial limpio, crea una rama específica para este desarrollo.
  ```bash
  git checkout -b feature/trame-app
  ```

---

## Fase 2: La Aplicación Trame Mínima

### Paso 1: Crear la Estructura Básica

- `[ ]` **Crear el archivo:** Crea un nuevo archivo en la ruta: `analisis_modal_3d/apps/trame_app.py`.

- `[ ]` **Añadir código inicial:** Pega el siguiente código en el archivo `trame_app.py`.
  ```python
  from trame.app import get_server
  from trame.ui.vuetify import SinglePageLayout
  from trame.widgets import vuetify

  server = get_server(client_type="vue2")
  state, ctrl = server.state, server.controller

  with SinglePageLayout(server) as layout:
      layout.title.set_text("Aplicación de Análisis Estructural")
      with layout.content:
          with vuetify.VContainer():
              vuetify.VCardTitle("Bienvenido a la aplicación con Trame")

  if __name__ == "__main__":
      server.start()
  ```

- `[ ]` **Ejecutar y verificar:** Corre `python analisis_modal_3d/apps/trame_app.py` y abre la URL que aparece en la terminal. Deberías ver el título y el mensaje.

- `[ ]` **Checkpoint 1:** Guarda tu progreso en Git.
  ```bash
  git add analisis_modal_3d/apps/trame_app.py
  git commit -m "feat(trame): Initial Trame app setup with basic layout"
  ```

---

## Fase 3: Integración de Visualización 3D

### Paso 2: Añadir un Visor 3D de PyVista

- `[ ]` **Modificar `trame_app.py`:** Reemplaza el contenido del archivo con el siguiente código para añadir el visor 3D y una esfera de prueba.
  ```python
  from trame.app import get_server
  from trame.ui.vuetify import SinglePageLayout
  from trame.widgets import vuetify, vtk as trame_vtk
  import pyvista as pv

  server = get_server(client_type="vue2")
  state, ctrl = server.state, server.controller

  plotter = pv.Plotter(off_screen=True)
  plotter.add_mesh(pv.Sphere())

  with SinglePageLayout(server) as layout:
      layout.title.set_text("Visor 3D con Trame y PyVista")
      with layout.content:
          with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
              view = trame_vtk.VtkLocalView(plotter.ren_win)
              ctrl.view_mouse_left_button_press = view.mouse_left_button_press
              ctrl.view_mouse_right_button_press = view.mouse_right_button_press
              ctrl.view_mouse_middle_button_press = view.mouse_middle_button_press
              ctrl.view_mouse_wheel = view.mouse_wheel
              ctrl.view_mouse_move = view.mouse_move

  if __name__ == "__main__":
      server.start()
  ```

- `[ ]` **Checkpoint 2:** Reinicia el servidor, refresca el navegador y verifica que puedes interactuar con la esfera 3D. Luego, haz commit.
  ```bash
  git commit -am "feat(trame): Integrate PyVista plotter into the layout"
  ```

---

## Fase 4: Carga y Visualización de Estructuras

### Paso 3: Cargar y Dibujar una Estructura Dinámicamente

- `[ ]` **Modificar `trame_app.py`:** Reemplaza de nuevo todo el contenido. Este código añade la lógica para cargar datos, un menú desplegable en la UI y la función para dibujar la estructura seleccionada.
  ```python
  from trame.app import get_server
  from trame.ui.vuetify import SinglePageLayout
  from trame.widgets import vuetify, vtk as trame_vtk
  import pyvista as pv
  import numpy as np
  import sys, os

  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '''..'''', '''..'''')))
  from analisis_modal_3d.structures.structure import Structure
  from analisis_modal_3d.structures.node import Node
  from analisis_modal_3d.structures.element import Element, Material, Section
  from analisis_modal_3d.apps.data.simple_beam_data import get_structure_data as get_simple_beam_data
  from analisis_modal_3d.apps.data.bailey_data import get_structure_data as get_bailey_data

  STRUCTURE_DATA_LOADERS = { "Viga Simple": get_simple_beam_data, "Puente Bailey": get_bailey_data }

  server = get_server(client_type="vue2")
  state, ctrl = server.state, server.controller
  state.selected_structure = "Viga Simple"

  plotter = pv.Plotter(off_screen=True)

  def load_structure(structure_name):
      data = STRUCTURE_DATA_LOADERS[structure_name]()
      s = Structure()
      for n, p in data['''materials'''].items(): s.add_material(Material(n, p['''E'''], p['''G'''], p['''rho''']))
      for n, p in data['''sections'''].items(): s.add_section(Section(n, p['''area'''], p['''Iy'''], p['''Iz'''], p['''Ix''']))
      for nd in data['''nodes''']: s.add_node(Node(nd[0], nd[1], nd[2], nd[3]))
      for ed in data['''elements''']: s.add_element(Element(s.nodes[ed[0]], s.nodes[ed[1]], s.sections[ed[2]], s.materials[ed[3]]))
      return s

  def plot_structure(structure):
      plotter.clear()
      if not structure.nodes: return
      points = np.array([node.coordinates for node in structure.nodes.values()])
      lines = [item for elem in structure.elements.values() for item in [2, elem.n1.id, elem.n2.id]]
      mesh = pv.PolyData(points, lines=np.array(lines))
      plotter.add_mesh(mesh, name="structure_mesh", color='''lightblue''', line_width=5)
      plotter.reset_camera()
      ctrl.view_update()

  @state.change("selected_structure")
  def update_plot(selected_structure, **kwargs):
      plot_structure(load_structure(selected_structure))

  with SinglePageLayout(server) as layout:
      layout.title.set_text("Visor de Estructuras")
      with layout.toolbar:
          vuetify.VSpacer()
          vuetify.VSelect(v_model=("selected_structure",), items=("Object.keys(STRUCTURE_DATA_LOADERS)",), dense=True, hide_details=True)
      with layout.content:
          with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
              view = trame_vtk.VtkLocalView(plotter.ren_win)
              ctrl.view_mouse_left_button_press = view.mouse_left_button_press
              ctrl.view_mouse_right_button_press = view.mouse_right_button_press
              ctrl.view_mouse_middle_button_press = view.mouse_middle_button_press
              ctrl.view_mouse_wheel = view.mouse_wheel
              ctrl.view_mouse_move = view.mouse_move

  if __name__ == "__main__":
      state.STRUCTURE_DATA_LOADERS = STRUCTURE_DATA_LOADERS
      update_plot(state.selected_structure)
      server.start()
  ```

- `[ ]` **Checkpoint 3:** Reinicia el servidor. Verifica que el menú desplegable funciona y cambia la estructura 3D. Luego, haz commit.
  ```bash
  git commit -am "feat(trame): Add structure selection and dynamic plotting"
  ```

---

## Fase 5: Ejecución del Análisis Modal

### Paso 4: Añadir Controles de Análisis y Tabla de Resultados

- `[ ]` **Modificar `trame_app.py`:** Reemplaza el contenido del archivo. Este código añade el panel de control, la lógica de análisis y la tabla de resultados.
  ```python
  from trame.app import get_server
  from trame.ui.vuetify import SinglePageLayout
  from trame.widgets import vuetify, vtk as trame_vtk
  import pyvista as pv
  import numpy as np
  import sys, os
  
  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '''..'''', '''..'''')))
  from analisis_modal_3d.structures.structure import Structure
  from analisis_modal_3d.structures.node import Node
  from analisis_modal_3d.structures.element import Element, Material, Section
  from analisis_modal_3d.apps.data.simple_beam_data import get_structure_data as get_simple_beam_data
  from analisis_modal_3d.apps.data.bailey_data import get_structure_data as get_bailey_data
  from analisis_modal_3d.analysis.modal import ModalAnalysis
  import pandas as pd

  STRUCTURE_DATA_LOADERS = { "Viga Simple": get_simple_beam_data, "Puente Bailey": get_bailey_data }

  server = get_server(client_type="vue2")
  state, ctrl = server.state, server.controller
  
  state.selected_structure = "Viga Simple"
  state.num_modes = 5
  state.analysis_results = []
  state.frequencies = []
  state.mode_shapes = None
  state.structure = None

  plotter = pv.Plotter(off_screen=True)

  def load_structure(structure_name):
      data = STRUCTURE_DATA_LOADERS[structure_name]()
      s = Structure()
      for n, p in data['''materials'''].items(): s.add_material(Material(n, p['''E'''], p['''G'''], p['''rho''']))
      for n, p in data['''sections'''].items(): s.add_section(Section(n, p['''area'''], p['''Iy'''], p['''Iz'''], p['''Ix''']))
      for nd in data['''nodes''']: s.add_node(Node(nd[0], nd[1], nd[2], nd[3]))
      for ed in data['''elements''']: s.add_element(Element(s.nodes[ed[0]], s.nodes[ed[1]], s.sections[ed[2]], s.materials[ed[3]]))
      return s

  def plot_structure(structure):
      plotter.clear()
      if not structure.nodes: return
      points = np.array([node.coordinates for node in structure.nodes.values()])
      lines = [item for elem in structure.elements.values() for item in [2, elem.n1.id, elem.n2.id]]
      mesh = pv.PolyData(points, lines=np.array(lines))
      plotter.add_mesh(mesh, name="structure_mesh", color='''lightblue''', line_width=5)
      plotter.reset_camera()
      ctrl.view_update()

  @state.change("selected_structure")
  def update_plot(selected_structure, **kwargs):
      state.structure = load_structure(selected_structure)
      plot_structure(state.structure)
      state.analysis_results = []
      state.frequencies = []
      state.mode_shapes = None

  @ctrl.trigger("run_analysis")
  def run_analysis():
      if not state.structure: return
      analysis = ModalAnalysis(state.structure)
      frequencies, modes, _ = analysis.solve(num_modes=state.num_modes)
      state.frequencies = frequencies.tolist()
      state.mode_shapes = modes.tolist()
      results = [{"mode": i + 1, "frequency_hz": f"{freq:.2f}"} for i, freq in enumerate(frequencies)]
      state.analysis_results = results

  with SinglePageLayout(server) as layout:
      layout.title.set_text("Análisis Modal de Estructuras")
      with layout.toolbar:
          vuetify.VSpacer()
          vuetify.VSelect(v_model=("selected_structure",), items=("Object.keys(STRUCTURE_DATA_LOADERS)",), dense=True, hide_details=True)
      with layout.content:
          with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
              with vuetify.VRow(classes="fill-height"):
                  with vuetify.VCol(cols=3):
                      with vuetify.VCard():
                          vuetify.VCardTitle("Controles de Análisis")
                          with vuetify.VCardText():
                              vuetify.VSlider(label="Número de Modos", v_model=("num_modes", 5), min=1, max=20, step=1, thumb_label=True)
                              vuetify.VBtn("Realizar Análisis Modal", classes="mt-4", click=ctrl.run_analysis)
                          vuetify.VCardTitle("Resultados")
                          with vuetify.VDataTable(v_if="analysis_results.length > 0", headers=("[{text: '''Modo''', value: '''mode'''}, {text: '''Frecuencia (Hz)''', value: '''frequency_hz'''}]",), items=("analysis_results",), item_key="mode", dense=True, hide_default_footer=True, classes="elevation-1"):
                              pass
                  with vuetify.VCol(cols=9):
                      view = trame_vtk.VtkLocalView(plotter.ren_win)
                      ctrl.view_mouse_left_button_press = view.mouse_left_button_press
                      ctrl.view_mouse_right_button_press = view.mouse_right_button_press
                      ctrl.view_mouse_middle_button_press = view.mouse_middle_button_press
                      ctrl.view_mouse_wheel = view.mouse_wheel
                      ctrl.view_mouse_move = view.mouse_move
  
  if __name__ == "__main__":
      state.STRUCTURE_DATA_LOADERS = STRUCTURE_DATA_LOADERS
      update_plot(state.selected_structure)
      server.start()
  ```

- `[ ]` **Checkpoint 4:** Reinicia el servidor. Verifica que el panel de control aparece y que al pulsar el botón se ejecuta el análisis y se llena la tabla. Luego, haz commit.
  ```bash
  git commit -am "feat(trame): Implement modal analysis and display results table"
  ```

---

## Fase 6: Visualización Interactiva de los Modos

### Paso 5: Deformar la Estructura según el Modo Seleccionado

- `[ ]` **Modificar `trame_app.py`:** Reemplaza el contenido por última vez. Este código final añade los sliders de modo/escala y la lógica para deformar la malla 3D en tiempo real.
  ```python
  from trame.app import get_server
  from trame.ui.vuetify import SinglePageLayout
  from trame.widgets import vuetify, vtk as trame_vtk
  import pyvista as pv
  import numpy as np
  import sys, os

  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '''..'''', '''..'''')))
  from analisis_modal_3d.structures.structure import Structure
  from analisis_modal_3d.structures.node import Node
  from analisis_modal_3d.structures.element import Element, Material, Section
  from analisis_modal_3d.apps.data.simple_beam_data import get_structure_data as get_simple_beam_data
  from analisis_modal_3d.apps.data.bailey_data import get_structure_data as get_bailey_data
  from analisis_modal_3d.analysis.modal import ModalAnalysis
  import pandas as pd

  STRUCTURE_DATA_LOADERS = { "Viga Simple": get_simple_beam_data, "Puente Bailey": get_bailey_data }

  server = get_server(client_type="vue2")
  state, ctrl = server.state, server.controller

  state.selected_structure = "Viga Simple"
  state.num_modes = 5
  state.analysis_results = []
  state.frequencies = []
  state.mode_shapes = None
  state.structure = None
  state.selected_mode = 1
  state.scale_factor = 10.0
  state.original_points = None

  plotter = pv.Plotter(off_screen=True)

  def load_structure(structure_name):
      data = STRUCTURE_DATA_LOADERS[structure_name]()
      s = Structure()
      for n, p in data['''materials'''].items(): s.add_material(Material(n, p['''E'''], p['''G'''], p['''rho''']))
      for n, p in data['''sections'''].items(): s.add_section(Section(n, p['''area'''], p['''Iy'''], p['''Iz'''], p['''Ix''']))
      for nd in data['''nodes''']: s.add_node(Node(nd[0], nd[1], nd[2], nd[3]))
      for ed in data['''elements''']: s.add_element(Element(s.nodes[ed[0]], s.nodes[ed[1]], s.sections[ed[2]], s.materials[ed[3]]))
      return s

  def plot_structure(structure):
      plotter.clear()
      if not structure.nodes: return
      points = np.array([node.coordinates for node in structure.nodes.values()])
      lines = [item for elem in structure.elements.values() for item in [2, elem.n1.id, elem.n2.id]]
      mesh = pv.PolyData(points, lines=np.array(lines))
      plotter.add_mesh(mesh, name="structure_mesh", color='''lightblue''', line_width=5)
      plotter.reset_camera()
      ctrl.view_update()

  @state.change("selected_structure")
  def update_plot(selected_structure, **kwargs):
      state.structure = load_structure(selected_structure)
      state.original_points = np.array([node.coordinates for node in state.structure.nodes.values()]).tolist()
      plot_structure(state.structure)
      state.analysis_results = []
      state.frequencies = []
      state.mode_shapes = None

  @ctrl.trigger("run_analysis")
  def run_analysis():
      if not state.structure: return
      analysis = ModalAnalysis(state.structure)
      frequencies, modes, _ = analysis.solve(num_modes=state.num_modes)
      state.frequencies = frequencies.tolist()
      state.mode_shapes = modes.tolist()
      results = [{"mode": i + 1, "frequency_hz": f"{freq:.2f}"} for i, freq in enumerate(frequencies)]
      state.analysis_results = results
      update_mode_shape()

  @state.change("selected_mode", "scale_factor")
  def update_mode_shape(**kwargs):
      if not state.mode_shapes or not state.original_points:
          plotter.remove_actor("deformed_mesh")
          ctrl.view_update()
          return

      mode_index = state.selected_mode - 1
      if mode_index >= len(state.mode_shapes): return

      original_points = np.array(state.original_points)
      mode_shape = np.array(state.mode_shapes[mode_index]).reshape(-1, 6)
      
      displacement = mode_shape[:, :3]
      deformed_points = original_points + displacement * state.scale_factor

      mesh = plotter.mesh.copy()
      mesh.points = deformed_points
      plotter.add_mesh(mesh, name="deformed_mesh", style='''wireframe''', color='''red''', line_width=3)
      
      ctrl.view_update()

  with SinglePageLayout(server) as layout:
      layout.title.set_text("Análisis Modal de Estructuras")
      with layout.toolbar:
          vuetify.VSpacer()
          vuetify.VSelect(v_model=("selected_structure",), items=("Object.keys(STRUCTURE_DATA_LOADERS)",), dense=True, hide_details=True)
      with layout.content:
          with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
              with vuetify.VRow(classes="fill-height"):
                  with vuetify.VCol(cols=3):
                      with vuetify.VCard():
                          vuetify.VCardTitle("Controles de Análisis")
                          with vuetify.VCardText():
                              vuetify.VSlider(label="Número de Modos", v_model=("num_modes", 5), min=1, max=20, step=1, thumb_label=True)
                              vuetify.VBtn("Realizar Análisis Modal", classes="mt-4", click=ctrl.run_analysis)
                          
                          with vuetify.VCardText(v_if="analysis_results.length > 0"):
                              vuetify.VSlider(label="Modo Seleccionado", v_model=("selected_mode", 1), min=1, max=("num_modes", 5), step=1, thumb_label=True)
                              vuetify.VSlider(label="Factor de Escala", v_model=("scale_factor", 10.0), min=0.0, max=100.0, step=0.5, thumb_label=True)

                          vuetify.VCardTitle("Resultados")
                          with vuetify.VDataTable(v_if="analysis_results.length > 0", headers=("[{text: '''Modo''', value: '''mode'''}, {text: '''Frecuencia (Hz)''', value: '''frequency_hz'''}]",), items=("analysis_results",), item_key="mode", dense=True, hide_default_footer=True, classes="elevation-1"):
                              pass
                  with vuetify.VCol(cols=9):
                      view = trame_vtk.VtkLocalView(plotter.ren_win)
                      ctrl.view_mouse_left_button_press = view.mouse_left_button_press
                      ctrl.view_mouse_right_button_press = view.mouse_right_button_press
                      ctrl.view_mouse_middle_button_press = view.mouse_middle_button_press
                      ctrl.view_mouse_wheel = view.mouse_wheel
                      ctrl.view_mouse_move = view.mouse_move

  if __name__ == "__main__":
      state.STRUCTURE_DATA_LOADERS = STRUCTURE_DATA_LOADERS
      update_plot(state.selected_structure)
      server.start()
  ```

- `[ ]` **Checkpoint 5:** Reinicia el servidor. Ejecuta un análisis. Verifica que los nuevos sliders aparecen y que al moverlos se deforma la estructura en la vista 3D. Luego, haz commit.
  ```bash
  git commit -am "feat(trame): Add interactive mode shape visualization"
  ```

---

¡Listo! Ahora tienes una guía completa en formato checklist para construir tu aplicación.