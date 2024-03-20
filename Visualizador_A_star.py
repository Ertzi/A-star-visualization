import pygame
import numpy as np


# Los siguientes valores se pueden cambiar a voluntad del usuario (para que quepa en la pantalla...):

# Dimensiones de la cuadrícula 
n = 45  # Tamaño de la cuadrícula (nxn)
grid_size = 15  # Tamaño de cada cuadrado en píxeles

# Colores
WHITE = (238,238,210)
BLACK = (186,202,68)
GRID_COLOR = (200, 200, 200) # Color de fondo de la cuadrícula
MARKED_COLOR_START = (0, 0, 139) # Color para las posiciones marcadas
MARKED_COLOR_END = (255, 0, 0) 
TEXT_COLOR = (0,0,0)
BUTTON_COLOR = (100, 100, 100)

# A partir de aqui no tocar nada














# Variables generales:
grid_width, grid_height = n * grid_size, n * grid_size
width = grid_width + 300
height = grid_height

# ---------------------------------------------------------------
# ---------------------INICIO ALGORITMO--------------------------
# ---------------------------------------------------------------
def heuristico(posicion,posicion_final):
    return abs(posicion_final[0]-posicion[0]) + abs(posicion_final[1]-posicion[1])

def calcular_f(c,posicion_final):
    return (len(c)-1) + heuristico(c[-1],posicion_final)

def esta_dentro_del_tablero(posicion,n):
    return ( 0 <= posicion[0] ) and (posicion[0] < n) and ( 0 <= posicion[1] ) and (posicion[1] < n)

def no_choca_con_borde(nuevo_movimiento,mapa):
    x,y = nuevo_movimiento
    return mapa[x][y] != 1

def sucesores(c_min,mapa,visitados,g_visitados,A,f,n,posicion_final,f_sol):
    movimientos = [(1,0),(0,1),(-1,0),(0,-1)]
    x,y = c_min[-1]
    for dx,dy in movimientos:
        nuevo_movimiento = (x+dx,y+dy)
        if esta_dentro_del_tablero(nuevo_movimiento,n) and no_choca_con_borde(nuevo_movimiento,mapa) and nuevo_movimiento not in c_min and nuevo_movimiento not in visitados:
            if calcular_f(c_min + [nuevo_movimiento],posicion_final) <= f_sol:
                A.append(c_min + [nuevo_movimiento])
                visitados.append(nuevo_movimiento)
                g_visitados.append(len(c_min))
                f.append(calcular_f(c_min + [nuevo_movimiento],posicion_final))
        
        elif esta_dentro_del_tablero(nuevo_movimiento,n) and no_choca_con_borde(nuevo_movimiento,mapa) and nuevo_movimiento not in c_min and nuevo_movimiento in visitados:
            indice_visitados = visitados.index(nuevo_movimiento)
            if len(c_min) < g_visitados[indice_visitados] and calcular_f(c_min + [nuevo_movimiento],posicion_final) <= f_sol:
                g_visitados[indice_visitados] = len(c_min)
                A.append(c_min + [nuevo_movimiento])
                f.append(calcular_f(c_min + [nuevo_movimiento],posicion_final))
                
            
def A_star(mapa,n):
    
    # Definir posiciones iniciales y finales: 
    posicion_inicial = (0,0)
    posicion_final = (n-1,n-1)
    for i,fila in enumerate(mapa):
        for j,valor in enumerate(fila):
            if valor == 3:
                posicion_inicial = (i,j)
            elif valor == 4:
                posicion_final = (i,j)

    if posicion_inicial == (0,0):
        mapa[0][0] = 3
    if posicion_final == (n-1,n-1):
        mapa[n-1][n-1] = 4
    print(f"Posicion inicial = {posicion_inicial}")
    print(f"Posicion final = {posicion_final}")

    # Variables necesarias:
    visitados = [posicion_inicial] # Importa el orden
    g_visitados = [0] # Importa el orden
    A = [ [posicion_inicial] ] # Lista de listas (caminos), importa el orden
    f = [ calcular_f(A[0],posicion_final) ]
    sol = None # Solucion temporal
    f_sol = float("inf") # Distancia de la mejor solucion hasta el momento (como no
    # tenemos soluciones lo definiremos como infinito)
    
    while A != []:
        min_index = np.argmin(f)
        c_min = A[min_index]
        f_c_min = f[min_index]
        A.pop(min_index)
        f.pop(min_index)
        if c_min[-1] == posicion_final and f_c_min < f_sol: # Si es una solución mejor a la que ya tenemos
            # Actualizar solucion y coste minimo:
            sol = c_min[:]
            f_sol = f_c_min
            # Podar:
            indices_para_podar = []
            for i,f_i in enumerate(f):
                if f_i > f_sol:
                    indices_para_podar.append(i)
            A = [camino for indice,camino in enumerate(A) if indice not in indices_para_podar]
            f = [valor_f for indice, valor_f in enumerate(f) if indice not in indices_para_podar]

        else: # Si no es solución o es peor que la que ya tenemos
            sucesores(c_min,mapa,visitados,g_visitados,A,f,n,posicion_final,f_sol) # La función modificará las listas A, visitados y g_visitados
    

    # print(f"Visitados = \n{visitados}")
    print(f"Solucion = \n{sol}")
    print(f"Coste = {f_sol}")
    return sol, f_sol,visitados


# ---------------------------------------------------------------
# ----------------------FINAL ALGORITMO--------------------------
# ---------------------------------------------------------------








# ---------------------------------------------------------------
# --------------------INICIO VISUALIZACION-----------------------
# ---------------------------------------------------------------

class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 24)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)



# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Visualización del algoritmo A estrella")

# Crear matriz para almacenar el estado de la cuadrícula:


def draw_grid(grid,counter,dibujar_nodos_visitados,visitados,sol):
    screen.fill(GRID_COLOR)  # Rellenar el fondo con el color de la cuadrícula

    if dibujar_nodos_visitados and counter[0] < len(visitados): # Expandimos los nodos visitados
        x,y = visitados[counter[0]]
        grid[x][y] = 5
        # Dibujamos el punto inicial y final encima de los nodos visitados:
        x0,y0 = sol[0]
        grid[x0][y0] = 3
        counter[0] += 1
    if dibujar_nodos_visitados and counter[0] == len(visitados) and len(visitados) != 0: # 
        for x,y in sol[1:-1]:
            grid[x][y] = 2
            # Dibujamos el punto inicial y final encima del camino:
        x0,y0 = sol[0]
        grid[x0][y0] = 3
        xn,yn = sol[-1]
        grid[xn][yn] = 4
        counter[0] += 1

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1: # Si es una parte del muro
                color = BLACK
            elif grid[i][j] == 2: # Si es parte de la solucion
                # color = MARKED_COLOR
                color = (100,0,0)
            elif grid[i][j] == 3:
                color = MARKED_COLOR_START
            elif grid[i][j] == 4:
                color = MARKED_COLOR_END
            elif grid[i][j] == 5:
                color = (173,216,230)
            else:
                color = WHITE
            pygame.draw.rect(screen, color, (j * grid_size, i * grid_size, grid_size, grid_size))
            pygame.draw.rect(screen, GRID_COLOR, (j * grid_size, i * grid_size, grid_size, grid_size), 1)


def main():
    mapa = np.zeros((n, n), dtype=int)
    running = True
    drawing = False
    cleaning = False
    timer = 0
    dibujar_nodos_visitados = True
    escribir_coste_algoritmo = False
    counter = [0]
    visitados = []
    sol = []

     # Crear fuente para el texto
    font = pygame.font.Font(None, 15)
    font2 = pygame.font.Font(None, 30)
    font3 = pygame.font.Font(None, 25)
    # Texto de instrucciones
    instructions = [
        "Instrucciones:",
        "- Click izquierdo: dibujar los bordes del mapa",
        "- Click derecho: dibujar posiciones inicial e final",
        "    - Azul: posición inicial",
        "    - Rojo: posición final",
        "- Boton de la rueda del raton: borrar",
        "- Enter: iniciar la visalización"
    ]

    # Renderizar el texto en superficies individuales
    rendered_instructions = [font.render(text, True, TEXT_COLOR) for text in instructions]

    button = Button(width - 295, height - 500, 200, 40, BUTTON_COLOR, "Dibujar nodos visitados")
    button_clear_all = Button(width - 295, height - 400, 200, 40, BUTTON_COLOR, "Limpiar cuadricula")
    button_inicio_algoritmo = Button(width - 295, height - 300, 200, 40, BUTTON_COLOR, "Iniciar algoritmo")
    while running:
        
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            elif keys[pygame.K_RETURN]:
                for x in range(n):
                    for y in range(n):
                        if mapa[x][y] not in [0,1,3,4]:
                            mapa[x][y] = 0
                visitados = []
                counter = [0]
                sol = []
                sol,f,visitados = A_star(mapa,n)
                escribir_coste_algoritmo = True
                if not dibujar_nodos_visitados:
                    for x,y in sol[1:-1]:
                        mapa[x][y] = 2

                    x0,y0 = sol[0]
                    mapa[x0][y0] = 3
                    xn,yn = sol[-1]
                    mapa[xn][yn] = 4
                

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:  # Botón izquierdo del ratón
                    if button.rect.collidepoint(event.pos):
                        dibujar_nodos_visitados = not dibujar_nodos_visitados # Cambiar el estado de visibilidad
                    elif button_clear_all.rect.collidepoint(event.pos):
                        mapa = np.zeros((n, n), dtype=int)
                        counter = [0]
                        visitados = []
                        sol = []
                        escribir_coste_algoritmo = False
                    elif button_inicio_algoritmo.rect.collidepoint(event.pos):
                        for x in range(n):
                            for y in range(n):
                                if mapa[x][y] not in [0,1,3,4]:
                                    mapa[x][y] = 0
                        visitados = []
                        counter = [0]
                        sol = []
                        sol,f,visitados = A_star(mapa,n)
                        escribir_coste_algoritmo = True
                        if not dibujar_nodos_visitados:
                            for x,y in sol[1:-1]:
                                mapa[x][y] = 2

                            x0,y0 = sol[0]
                            mapa[x0][y0] = 3
                            xn,yn = sol[-1]
                            mapa[xn][yn] = 4

                    drawing = True
                    x, y = event.pos
                    col = x // grid_size
                    row = y // grid_size
                    
                    if 0 <= row < n and 0 <= col < n:
                        mapa[row][col] = 1

                elif event.button == 3 and timer == 0: # Boton derecho del raton
                    timer +=1
                    x, y = event.pos
                    col = x // grid_size
                    row = y // grid_size
                    if 0 <= row < n and 0 <= col < n:
                        mapa[row][col] = 3 # == 3 is INITIAL POINT (WHITE)
                    
                elif event.button == 3 and timer == 1:
                    timer -= 1
                    x, y = event.pos
                    col = x // grid_size
                    row = y // grid_size
                    if 0 <= row < n and 0 <= col < n:
                        mapa[row][col] = 4 # == 4 is END POINT (RED)
                
                elif event.button == 2:
                    x, y = event.pos
                    col = x // grid_size
                    row = y // grid_size
                    if 0 <= row < n and 0 <= col < n:
                        mapa[row][col] = 0 # Clean wrong cells
                    cleaning = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Botón izquierdo del ratón
                    drawing = False
                if event.button == 2:
                    cleaning = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    x, y = event.pos
                    col = x // grid_size
                    row = y // grid_size
                    if 0 <= row < n and 0 <= col < n:
                        mapa[row][col] = 1
                if cleaning:
                    x, y = event.pos
                    col = x // grid_size
                    row = y // grid_size
                    if 0 <= row < n and 0 <= col < n:
                        mapa[row][col] = 0

        draw_grid(mapa,counter,dibujar_nodos_visitados,visitados,sol)
        for i, surface in enumerate(rendered_instructions):
            screen.blit(surface, (width -300, i * 20))
        
        if dibujar_nodos_visitados:
            texto = "On"
        else:
            texto = "Off"
        screen.blit(font2.render(f"{texto}",True,TEXT_COLOR),(width - 80, height - 485))
        if escribir_coste_algoritmo:
            screen.blit(font3.render(f"La longitud del camino es: {f}",True,TEXT_COLOR),(width - 295, height - 250))
        button.draw(screen)
        button_clear_all.draw(screen)
        button_inicio_algoritmo.draw(screen)

        pygame.display.flip()

    pygame.quit()


# ---------------------------------------------------------------
# --------------------FINAL VISUALIZACION-----------------------
# ---------------------------------------------------------------






if __name__ == "__main__":
    main()