import simpy
import random
import flet as ft
vector=[]


def main(page: ft.Page):
    page.title = "Redes interconectadas"
    page.vertical_alignment="center"
    page.horizontal_alignment="center"
    page.bgcolor="white"
    campo = ft.TextField(
        width=1200,
        height=1200,
        bgcolor="blue",
        border_radius=20,
        disabled=False,
        text_align=ft.TextAlign.CENTER,
        content_padding=250,
        multiline=True,
        min_lines=3,
            max_lines=10,
    )

    #esta seria la funcion que seria como la de iniciar_simulacion
    def construir_filas():
        env = simpy.Environment()
        nodos = []
        
    def iniciar_simulacion():
        env.run(until=10)
        print(vector)
        campo.value ="\n".join(str(event) for event in vector)
        print('Simulación finalizada')
        page.update()

    def button_click(e):
        iniciar_simulacion()
        
        
        

    page.add(
        ft.SafeArea(
            ft.Row(
                [
                    ft.Text("Redes interconectadas", 
                    style=ft.TextStyle(size=30, weight="wavy", font_family="italic", color="blue")),
                     ft.Row(
            [
            ft.ElevatedButton(
                text="Construir red de filas",
                
                width=200,
                on_click=button_click,

                
                
                ),
            ],
              alignment=ft.MainAxisAlignment.SPACE_EVENLY,

            ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,

            )

        ),

           
            ft.Row(
            [
            campo,
            ],
             alignment=ft.MainAxisAlignment.CENTER,
            ),
            

    )
    

    
    class Nodo:
        def __init__(self, env, nombre, tasa_servicio):
            self.env = env
            self.nombre = nombre
            self.servidor = simpy.Resource(env, capacity=1)
            self.tasa_servicio = tasa_servicio
            self.cola = simpy.Container(env, init=0)
            self.env.process(self.procesar())

        def procesar(self):
            while True:
                yield self.cola.get(1)
                yield self.env.timeout(random.expovariate(self.tasa_servicio))

    def cliente(env, nombre, nodo_actual, nodos, probabilidad_transicion):
        vector.append(f'{nombre} llega al nodo {nodo_actual.nombre} en el tiempo {env.now}')
        with nodo_actual.servidor.request() as req:
            yield req
            vector.append(f'{nombre} empieza a ser atendido en el nodo {nodo_actual.nombre} en el tiempo {env.now}')
            yield env.timeout(random.expovariate(nodo_actual.tasa_servicio))
            vector.append(f'{nombre} termina de ser atendido en el nodo {nodo_actual.nombre} en el tiempo {env.now}')

        if random.random() < probabilidad_transicion[nodo_actual.nombre]:
            siguiente_nodo = nodos[(nodos.index(nodo_actual) + 1) % len(nodos)]
            siguiente_nodo.cola.put(1)
            env.process(cliente(env, nombre, siguiente_nodo, nodos, probabilidad_transicion))
        else:
            vector.append(f'{nombre} ha salido del sistema en el tiempo {env.now}')

    # Parámetros
    num_nodos = 3
    tasa_llegada = 0.5
    tasa_servicio_nodos = [0.7, 0.6, 0.8]
    probabilidad_transicion = {'Nodo 1': 0.6, 'Nodo 2': 0.8, 'Nodo 3': 0.5}

    env = simpy.Environment()

    # Crear nodos
    nodos = [Nodo(env, f'Nodo {i+1}', tasa_servicio_nodos[i]) for i in range(num_nodos)]

    # Generar clientes 
    for i in range(3):
        env.process(cliente(env, f'Cliente {i+1}', nodos[0], nodos, probabilidad_transicion))

    

ft.app(main)
